# -*- coding: utf-8 -*-
"""
Collecteur des courriels entrants. Phase 4 du Plan Jarvis.

Deterministe, aucun appel a un modele. Il interroge l'API Gmail depuis un
marqueur d'horodatage, jette tout ce qui ne compte pas, et ecrit un fichier
de travail lisible par fil retenu. Le modele ne recoit que ce qui demande
un jugement. C'est ce qui tient le cout, et c'est la regle du plan.

Meme forme que prefiltre.py des transcriptions et que agenda.py de la note
du matin : il lit, il ne modifie rien, et il ne plante jamais sans le dire.

Il ne touche jamais a Gmail autrement qu'en lecture. Aucun envoi, aucun
marquage lu, aucune suppression, aucun classement. Le seul script qui ecrit
dans Gmail est brouillon.py, et il ne cree que des brouillons.

Ce qui compte, dans l'ordre ou les regles s'appliquent :

  1. Le bruit part en premier. Infolettre, notification, publicite, robot,
     reponse d'agenda, spam, corbeille. Une exclusion l'emporte toujours
     sur une inclusion : un no-reply qui ecrit dans un fil ou j'ai parle
     reste un no-reply.
  2. Ce qui survit est retenu s'il est une reponse dans un fil ou Souleman
     a envoye un message, ou si l'expediteur a une note dans 06 Personnes
     ou une ligne dans Pipeline clients S-WEB.
  3. Le reste est jete, avec son motif, lisible dans travail/rejets.txt.

Identifiants dans google.local.json, cherche a la racine C:/Obsidian/
d'abord, puis a cote de ce fichier. Une seule identite Google pour tous les
automates, un seul fichier, jamais une copie par automate.

Usage :
    python courriels.py <dossier_base> <coffre> [--sec] [--jours N]

    --sec    ecrit tout et affiche le detail du tri, sans rien changer
             d'autre. Le marqueur n'est de toute facon jamais avance ici,
             c'est le lanceur qui le fait, et seulement si le passage a
             reussi.
    --jours  fenetre du tout premier passage, quand aucun marqueur
             n'existe. Defaut 7.
"""

import base64
import glob
from concurrent import futures
import json
import os
import random
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

RACINE = "C:/Obsidian"
JETON = "https://oauth2.googleapis.com/token"
API = "https://gmail.googleapis.com/gmail/v1/users/me"
DELAI = 30

DEFAUT_JOURS = 7        # fenetre du premier passage, sans marqueur
MAX_MESSAGES = 400      # plafond de messages examines en un passage
MAX_FILS = 25           # plafond de fils retenus, le reste attend la suite
MAX_CAR = 1200          # extrait d'un message ancien du fil
MAX_CAR_DERNIER = 3000  # extrait du dernier message entrant

# Un expediteur qui porte un de ces mots dans sa partie locale n'attend pas
# de reponse. La liste est volontairement courte et litterale.
ROBOTS = (
    "no-reply", "noreply", "no_reply", "donotreply", "do-not-reply",
    "mailer-daemon", "postmaster", "bounce", "bounces", "notification",
    "notifications", "newsletter", "mailer", "automated", "autoreply",
)

# Mots trop communs pour identifier une entreprise a eux seuls.
VIDES = set("""la le les de du des and the inc enr ltee ltd corp clinique
groupe group spa esthetique esthetic style medical aesthetics services
service centre center agency agence""".split())


def sans_accent(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c))


def norme(s):
    """Minuscules, sans accent, espaces tasses. Pour comparer des noms."""
    s = sans_accent(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def ecrire(chemin, texte):
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)


# ------------------------------------------------------------------ Google

def identifiants(dossier):
    for c in (os.path.join(RACINE, "google.local.json"),
              os.path.join(dossier, "google.local.json")):
        if os.path.exists(c):
            with open(c, encoding="utf-8") as f:
                return json.load(f), c
    return None, ""


def acces(c):
    corps = urllib.parse.urlencode({
        "client_id": c["client_id"],
        "client_secret": c["client_secret"],
        "refresh_token": c["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request(JETON, data=corps, method="POST")
    with urllib.request.urlopen(req, timeout=DELAI) as r:
        return json.loads(r.read().decode("utf-8"))["access_token"]


def get(url, jeton, essais=6):
    """Une lecture, avec patience.

    Gmail repond 403 rateLimitExceeded ou 429 quand on lit trop vite. Vu le
    7 septembre 2026 sur un premier passage de 30 jours : 69 fils perdus,
    silencieusement jetes comme illisibles. Une limite de debit n'est pas
    une erreur de lecture, elle se traite en attendant.
    """
    attente = 1.0
    for essai in range(essais):
        try:
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + jeton})
            with urllib.request.urlopen(req, timeout=DELAI) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503) and essai < essais - 1:
                # Le hasard evite que six lectures refusees ensemble
                # reviennent toutes frapper a la meme seconde.
                time.sleep(attente + random.random())
                attente *= 2
                continue
            raise
        except Exception:
            if essai < essais - 1:
                time.sleep(attente + random.random())
                attente *= 2
                continue
            raise
    raise RuntimeError("lecture impossible apres %d essais" % essais)


def lister(q, jeton, plafond):
    """Les identifiants d'une recherche Gmail. Une page vaut 100 messages,
    et chaque entree porte deja son numero de fil : de quoi savoir dans
    quels fils Souleman a ecrit sans ouvrir un seul message."""
    sortie = []
    page = ""
    while len(sortie) < plafond:
        p = {"q": q, "maxResults": "100", "includeSpamTrash": "false"}
        if page:
            p["pageToken"] = page
        r = get(API + "/messages?" + urllib.parse.urlencode(p), jeton)
        sortie += r.get("messages", [])
        page = r.get("nextPageToken", "")
        if not page:
            break
    return sortie[:plafond]


# ------------------------------------------------------- le coffre decide

def repertoire(coffre):
    """Qui compte, lu dans le coffre. Personnes, clients, adresses."""
    personnes = []
    adresses = set()
    clients = []

    dossier = os.path.join(coffre, "06 Personnes")
    for chemin in sorted(glob.glob(os.path.join(dossier, "*.md"))):
        nom = os.path.basename(chemin)[:-3]
        alias = []
        try:
            with open(chemin, encoding="utf-8", errors="replace") as f:
                txt = f.read()
        except Exception:
            txt = ""
        for a in re.findall(r"^aliases?:\s*(.+)$", txt, re.M | re.I):
            alias += [x.strip(" []\"'") for x in a.split(",") if x.strip(" []\"'")]
        for m in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", txt):
            adresses.add(m.lower())
        personnes.append({
            "nom": nom,
            "note": "06 Personnes/" + nom + ".md",
            "noms": [norme(nom)] + [norme(a) for a in alias],
        })

    pipeline = os.path.join(coffre, "03 Domaines", "S-WEB", "Pipeline clients S-WEB.md")
    if os.path.exists(pipeline):
        with open(pipeline, encoding="utf-8", errors="replace") as f:
            for ligne in f:
                if not ligne.startswith("|"):
                    continue
                cols = [c.strip() for c in ligne.strip().strip("|").split("|")]
                if len(cols) < 2 or not re.match(r"^\d{4}-\d{3}$", cols[0]):
                    continue
                client = cols[1]
                if client and client not in [c["nom"] for c in clients]:
                    clients.append({
                        "nom": client,
                        "note": "03 Domaines/S-WEB/Pipeline clients S-WEB.md",
                        "cle": norme(client),
                        "mots": [m for m in norme(client).split()
                                 if len(m) >= 5 and m not in VIDES],
                    })
        with open(pipeline, encoding="utf-8", errors="replace") as f:
            for m in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                                f.read()):
                adresses.add(m.lower())

    return personnes, clients, adresses


def reconnait(nom_affiche, adresse, personnes, clients, adresses, miennes):
    """Retourne (motif, qui, note) ou (None, '', '')."""
    a = (adresse or "").lower()
    if a in miennes:
        return None, "", ""
    if a in adresses:
        return "adresse-connue", a, ""

    na = norme(nom_affiche)
    domaine = a.split("@")[-1] if "@" in a else ""
    dom = norme(domaine).replace(" ", "")

    for p in personnes:
        for cle in p["noms"]:
            if not cle:
                continue
            mots = cle.split()
            if len(mots) >= 2:
                # Prenom et nom, tous les deux presents. Un seul ne suffit pas.
                if all(m in na.split() for m in mots):
                    return "personne-connue", p["nom"], p["note"]
            elif na == cle:
                # Note a un seul mot : egalite stricte. Un prenom seul
                # n'identifie personne, et un homonyme coute plus qu'il ne
                # rapporte. Le cas est ecrit dans rejets.txt.
                return "personne-connue", p["nom"], p["note"]

    for c in clients:
        if c["cle"] and c["cle"].replace(" ", "") in na.replace(" ", ""):
            return "client-connu", c["nom"], c["note"]
        for m in c["mots"]:
            if m in dom:
                return "client-connu", c["nom"], c["note"]

    return None, "", ""


# ------------------------------------------------------- lecture d'un message

def entetes(msg):
    return {h["name"].lower(): h["value"]
            for h in msg.get("payload", {}).get("headers", [])}


def adresse_de(valeur):
    m = re.search(r"<([^>]+)>", valeur or "")
    if m:
        return m.group(1).strip().lower()
    v = (valeur or "").strip()
    return v.lower() if "@" in v else ""


def nom_de(valeur):
    v = (valeur or "").strip()
    m = re.match(r"^\s*(.*?)\s*<", v)
    nom = m.group(1) if m else v
    return nom.strip().strip('"').strip()


def pieces(payload, noms=None):
    """Noms des pieces jointes. Un message sans texte en a souvent une."""
    if noms is None:
        noms = []
    n = payload.get("filename") or ""
    if n:
        noms.append(n)
    for p in payload.get("parts", []) or []:
        pieces(p, noms)
    return noms


def types(payload, vus):
    vus.add(payload.get("mimeType", ""))
    for p in payload.get("parts", []) or []:
        types(p, vus)
    return vus


def decode(donnees):
    try:
        return base64.urlsafe_b64decode(donnees.encode("ascii")).decode("utf-8", "replace")
    except Exception:
        return ""


def texte_de(payload):
    """Le corps en texte. text/plain d'abord, sinon le html degrossi."""
    plain, html = [], []

    def marche(p):
        t = p.get("mimeType", "")
        d = p.get("body", {}).get("data")
        if d and t == "text/plain":
            plain.append(decode(d))
        elif d and t == "text/html":
            html.append(decode(d))
        for sp in p.get("parts", []) or []:
            marche(sp)

    marche(payload)
    if plain:
        return "\n".join(plain)
    if html:
        h = "\n".join(html)
        h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)
        h = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", h)
        h = re.sub(r"<[^>]+>", " ", h)
        h = h.replace("&nbsp;", " ").replace("&amp;", "&")
        h = h.replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'")
        h = h.replace("&quot;", '"')
        return h
    return ""


COUPURES = [
    re.compile(r"^\s*-{2,}\s*(Original Message|Message d'origine|Forwarded message)", re.I),
    re.compile(r"^\s*(Le|On)\s.{0,80}(a . crit|wrote)\s*:\s*$", re.I),
    re.compile(r"^\s*De\s*:\s.+$", re.I),
    re.compile(r"^\s*From\s*:\s.+$", re.I),
]


def propre(txt, maxi):
    """Retire la citation du message precedent et tasse les blancs."""
    lignes = []
    for l in (txt or "").replace("\r", "").split("\n"):
        if any(c.search(l) for c in COUPURES):
            break
        if l.lstrip().startswith(">"):
            continue
        lignes.append(l.rstrip())
    t = "\n".join(lignes)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    if len(t) > maxi:
        t = t[:maxi].rstrip() + "\n[...]"
    return t


def horloge(ms):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(int(ms) / 1000.0))


# ------------------------------------------------------------------ le tri

def bruit(msg, ent):
    """Retourne le motif de rejet, ou une chaine vide si le message survit."""
    lab = msg.get("labelIds", []) or []
    for mauvais, motif in (("SPAM", "spam"), ("TRASH", "corbeille"),
                           ("DRAFT", "brouillon"), ("CHAT", "chat")):
        if mauvais in lab:
            return motif
    for cat, motif in (("CATEGORY_PROMOTIONS", "publicite"),
                       ("CATEGORY_SOCIAL", "reseau social"),
                       ("CATEGORY_FORUMS", "forum")):
        if cat in lab:
            return motif
    if "list-unsubscribe" in ent or "list-id" in ent:
        return "infolettre, en-tete de desabonnement"
    if ent.get("precedence", "").lower() in ("bulk", "list", "junk", "auto_reply"):
        return "envoi en masse, en-tete Precedence"
    auto = ent.get("auto-submitted", "").lower()
    if auto and auto != "no":
        return "message automatique, en-tete Auto-Submitted"
    if "x-autoreply" in ent or "x-autorespond" in ent:
        return "reponse automatique"
    # Une invitation Google porte le From de l'organisateur et le Sender de
    # l'agenda. Le From seul ferait passer l'invitation pour un message de
    # cette personne. Vu le 7 septembre 2026 sur une invitation de
    # Franck-Maleek, retenue a tort parce qu'il a une note dans le coffre.
    if "calendar-notification@google.com" in (ent.get("sender", "") or "").lower():
        return "notification d'agenda"
    # Les parts n'existent qu'en lecture complete. Ce test attrape les
    # reponses d'invitation venues d'ailleurs, au moment ou le fil retenu
    # est charge en entier.
    if "text/calendar" in types(msg.get("payload", {}), set()):
        return "notification d'agenda"
    exp = adresse_de(ent.get("from", ""))
    local = exp.split("@")[0]
    for r in ROBOTS:
        if r in local:
            return "robot, expediteur en " + r
    return ""


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 3:
        print("usage: courriels.py <dossier_base> <coffre> [--sec] [--jours N]")
        return 2

    base = sys.argv[1]
    coffre = sys.argv[2]
    sec = "--sec" in sys.argv
    jours = DEFAUT_JOURS
    if "--jours" in sys.argv:
        try:
            jours = int(sys.argv[sys.argv.index("--jours") + 1])
        except Exception:
            jours = DEFAUT_JOURS

    travail = os.path.join(base, "travail")
    os.makedirs(travail, exist_ok=True)
    for f in glob.glob(os.path.join(travail, "*.md")):
        os.remove(f)                     # copies derivees, regenerables
    for nom in ("rejets.txt", "candidats.txt", "repertoire.txt"):
        p = os.path.join(travail, nom)
        if os.path.exists(p):
            os.remove(p)

    resultat = os.path.join(travail, "resultat.txt")

    def sortir(champs, detail=""):
        ecrire(resultat, "".join("%s=%s\n" % (k, v) for k, v in champs))
        if detail:
            print(detail)
        return 0

    # 1. Le marqueur. Millisecondes epoch du message le plus recent traite.
    marqueur = os.path.join(base, "marqueur.txt")
    depuis = 0
    if os.path.exists(marqueur):
        try:
            with open(marqueur, encoding="utf-8-sig") as f:
                depuis = int(f.read().strip() or 0)
        except Exception:
            depuis = 0
    if not depuis:
        depuis = int((time.time() - jours * 86400) * 1000)
        premier = True
    else:
        premier = False

    # 2. Ce qui a deja ete depose, pour ne jamais doubler une capture.
    # Le lanceur n'ajoute une ligne ici qu'une fois le passage reussi.
    deja = set()
    chemin_deposes = os.path.join(base, "deposes.txt")
    if os.path.exists(chemin_deposes):
        with open(chemin_deposes, encoding="utf-8-sig") as f:
            for l in f:
                p = l.split()
                if len(p) >= 2:
                    deja.add((p[0], p[1]))

    # 3. Les identifiants
    conf, ou = identifiants(base)
    if not conf:
        return sortir([("statut", "indisponible"),
                       ("raison", "google.local.json absent de la racine et du dossier"),
                       ("fils", 0)])
    manque = [k for k in ("client_id", "client_secret", "refresh_token") if not conf.get(k)]
    if manque:
        return sortir([("statut", "indisponible"),
                       ("raison", "champs manquants, " + ", ".join(manque)),
                       ("fils", 0)])
    try:
        jeton = acces(conf)
    except urllib.error.HTTPError as e:
        try:
            motif = json.loads(e.read().decode("utf-8")).get("error", "")
        except Exception:
            motif = ""
        return sortir([("statut", "indisponible"),
                       ("raison", "Google a refuse le refresh token, HTTP %s %s" % (e.code, motif)),
                       ("fils", 0)])
    except Exception as e:
        return sortir([("statut", "indisponible"),
                       ("raison", "echange du jeton impossible, %s" % e),
                       ("fils", 0)])

    try:
        profil = get(API + "/profile", jeton)
        boite = profil.get("emailAddress", "").lower()
    except Exception as e:
        return sortir([("statut", "indisponible"),
                       ("raison", "profil Gmail illisible, %s" % e), ("fils", 0)])

    identites = conf.get("identites") or {}
    miennes = set([boite])
    for v in identites.values():
        a = adresse_de(v)
        if a:
            miennes.add(a)
    adresse_sweb = adresse_de(identites.get("sweb", ""))

    # Le numero du libelle S-WEB, resolu par son nom. Il dit sous quelle
    # identite un fil est arrive, plus surement que les destinataires.
    label_sweb = ""
    try:
        for l in get(API + "/labels", jeton).get("labels", []):
            if l.get("name", "").strip().upper() == "S-WEB":
                label_sweb = l.get("id", "")
    except Exception:
        label_sweb = ""

    # 4. Qui compte, lu dans le coffre
    personnes, clients, adresses = repertoire(coffre)
    ecrire(os.path.join(travail, "repertoire.txt"),
           "personnes=%d\nclients=%d\nadresses=%d\n\n" % (len(personnes), len(clients), len(adresses))
           + "".join("personne: %s\n" % p["nom"] for p in personnes)
           + "".join("client: %s\n" % c["nom"] for c in clients)
           + "".join("adresse: %s\n" % a for a in sorted(adresses)))

    # 5. Les messages depuis le marqueur.
    # Les trois categories que Gmail range lui-meme, publicite, reseaux et
    # forums, sont ecartees par la requete plutot que lues une par une :
    # elles ne contiennent jamais de reponse et chaque lecture coute une
    # part du debit autorise. Elles sont comptees a part, pour que le mode
    # sec dise quand meme combien il en a ecarte.
    borne = max(0, depuis // 1000 - 60)   # une minute de marge, le tri est refait plus bas
    hors = "-category:promotions -category:social -category:forums"
    dedans = "{category:promotions category:social category:forums}"  # accolades, le OR de Gmail
    rejets = []
    try:
        entrees = lister("after:%d -in:chats %s" % (borne, hors), jeton, MAX_MESSAGES)
        ranges = lister("after:%d -in:chats %s" % (borne, dedans), jeton, MAX_MESSAGES)
    except Exception as e:
        return sortir([("statut", "indisponible"),
                       ("raison", "liste Gmail illisible, %s" % e), ("fils", 0)])
    if ranges:
        rejets.append(("Gmail", "%d message(s)" % len(ranges),
                       "publicite, reseau social ou forum, ecarte par la categorie Gmail"))

    # 5 bis. Les fils ou Souleman a ecrit lui-meme. La liste des envois
    # donne le numero de fil sans ouvrir un seul message. Sans cela, il
    # faudrait charger chaque fil entier pour savoir s'il y a parle, et
    # c'est ce qui a fait tomber le premier essai sur la limite de debit.
    try:
        miens = set(m.get("threadId") for m in lister("in:sent newer_than:1y", jeton, 1500))
    except Exception:
        miens = set()

    # 6. Un passage par message, en metadonnees, plusieurs de front. Le
    # corps ne sera lu que pour les fils retenus.
    entrants = []      # ce qui survit au bruit
    maxi = depuis
    lus = 0

    entetes_demandes = ("?format=metadata"
              "&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Subject"
              "&metadataHeaders=Date&metadataHeaders=List-Unsubscribe"
              "&metadataHeaders=List-Id&metadataHeaders=Precedence"
              "&metadataHeaders=Auto-Submitted&metadataHeaders=X-Autoreply"
              "&metadataHeaders=Sender")

    def charger(e):
        try:
            return get(API + "/messages/" + e["id"] + entetes_demandes, jeton)
        except Exception as ex:
            return {"_echec": str(ex), "id": e["id"]}

    with futures.ThreadPoolExecutor(max_workers=4) as pool:
        messages = list(pool.map(charger, entrees))

    echecs = 0
    for m in messages:
        if "_echec" in m:
            echecs += 1
            rejets.append(("?", m.get("id", ""), "lecture impossible, %s" % m["_echec"]))
            continue
        mid = m["id"]
        lus += 1
        interne = int(m.get("internalDate", "0"))
        if interne > maxi:
            maxi = interne
        if interne <= depuis:
            continue                      # deja traite, la marge de la requete
        ent = entetes(m)
        exp = adresse_de(ent.get("from", ""))
        sujet = (ent.get("subject", "") or "sans objet").strip()
        if "SENT" in (m.get("labelIds", []) or []) or exp in miennes:
            continue                      # ce que j'envoie n'est pas une reponse
        motif = bruit(m, ent)
        if motif:
            rejets.append((ent.get("from", ""), sujet, motif))
            continue
        entrants.append({"id": mid, "fil": m.get("threadId"), "date": interne,
                         "de": ent.get("from", ""), "exp": exp, "sujet": sujet,
                         "labels": m.get("labelIds", []) or []})

    # 7. Un fil, une decision. Le fil complet dit si Souleman y a parle.
    fils = {}
    for e in entrants:
        fils.setdefault(e["fil"], []).append(e)

    # La decision se prend sans reseau : le coffre dit qui compte, et la
    # liste des envois dit ou Souleman a parle. Le fil complet n'est charge
    # que pour ce qui est retenu.
    retenus = []
    for fid, msgs in fils.items():
        msgs.sort(key=lambda x: x["date"])
        dernier = msgs[-1]
        motif, qui, note = reconnait(nom_de(dernier["de"]), dernier["exp"],
                                     personnes, clients, adresses, miennes)
        if not motif and fid in miens:
            motif, qui, note = "reponse-a-moi", nom_de(dernier["de"]) or dernier["exp"], ""
        if not motif:
            rejets.append((dernier["de"], dernier["sujet"],
                           "inconnu du coffre, et aucun message de moi dans le fil"))
            continue
        if (fid, dernier["id"]) in deja:
            rejets.append((dernier["de"], dernier["sujet"], "deja depose a un passage precedent"))
            continue
        retenus.append({"fil": fid, "dernier": dernier, "motif": motif,
                        "qui": qui, "note": note,
                        "deja": any(f == fid for f, _ in deja)})

    retenus.sort(key=lambda r: r["dernier"]["date"])
    coupe = False
    if len(retenus) > MAX_FILS:
        retenus = retenus[:MAX_FILS]
        coupe = True
        # Le marqueur ne depasse pas ce qui a ete traite, sinon les fils
        # laisses de cote seraient perdus au lieu d'etre relus.
        maxi = retenus[-1]["dernier"]["date"]

    # 8. Les fichiers de travail, un par fil. C'est seulement ici que le
    # fil entier est charge, corps compris. Un fil illisible se signale et
    # ne fait pas tomber le passage.
    candidats = []
    complets = []
    for r in retenus:
        try:
            r["msgs"] = get(API + "/threads/" + r["fil"] + "?format=full",
                            jeton).get("messages", [])
        except Exception as e:
            rejets.append((r["dernier"]["de"], r["dernier"]["sujet"],
                           "fil illisible, %s" % e))
            continue
        # Deuxieme passe du tri du bruit, avec les parts sous les yeux :
        # une reponse d'invitation venue d'un autre service que Google ne
        # se reconnait qu'ici.
        dernier_complet = None
        for m in r["msgs"]:
            if m["id"] == r["dernier"]["id"]:
                dernier_complet = m
        if dernier_complet is not None:
            motif = bruit(dernier_complet, entetes(dernier_complet))
            if motif:
                rejets.append((r["dernier"]["de"], r["dernier"]["sujet"], motif))
                continue
        complets.append(r)
    retenus = complets

    for i, r in enumerate(retenus, 1):
        d = r["dernier"]
        # Sous quelle identite repondre. Le libelle S-WEB est pose par le
        # filtre sur deliveredto, c'est la source la plus sure. Son numero
        # est propre a la boite, il est resolu plus haut par son nom. En
        # repli, l'adresse S-WEB citee dans les destinataires du message.
        ent_d = {}
        for m in r["msgs"]:
            if m["id"] == d["id"]:
                ent_d = entetes(m)
        dest = " ".join([ent_d.get("to", ""), ent_d.get("cc", ""),
                         ent_d.get("delivered-to", "")]).lower()
        identite = "principal"
        if label_sweb and label_sweb in d["labels"]:
            identite = "sweb"
        elif adresse_sweb and adresse_sweb in dest:
            identite = "sweb"

        corps = []
        for m in r["msgs"]:
            e = entetes(m)
            de = e.get("from", "")
            a = adresse_de(de)
            qui = "Souleman" if (a in miennes or "SENT" in (m.get("labelIds", []) or [])) else (nom_de(de) or a)
            maxc = MAX_CAR_DERNIER if m["id"] == d["id"] else MAX_CAR
            t = propre(texte_de(m.get("payload", {})), maxc)
            jointes = [j for j in pieces(m.get("payload", {})) if j]
            if not t:
                t = "(aucun texte dans ce message)"
            if jointes:
                t += "\n[pieces jointes : " + ", ".join(jointes[:6]) + "]"
            corps.append("--- %s, %s ---\n%s\n" % (qui, horloge(m.get("internalDate", 0)), t))

        tete = [
            "fil: " + r["fil"],
            "sujet: " + d["sujet"],
            "interlocuteur: " + d["de"],
            "motif: " + r["motif"],
            "reconnu: " + (r["qui"] or "personne, c'est une reponse a un courriel envoye"),
            "note: " + (r["note"] or "aucune"),
            "identite: " + identite,
            "repondre_a: " + d["exp"],
            "repondre_a_id: " + d["id"],
            "date: " + horloge(d["date"]),
            "messages: %d" % len(r["msgs"]),
            "deja_capture: " + ("oui" if r["deja"] else "non"),
            "",
        ]
        nom = "fil-%02d %s.md" % (i, re.sub(r'[<>:"/\\|?*]', " ", d["sujet"])[:60].strip())
        ecrire(os.path.join(travail, nom), "\n".join(tete) + "\n".join(corps))
        candidats.append("%s %s %s" % (r["fil"], d["id"], horloge(d["date"]).replace(" ", "T")))

    ecrire(os.path.join(travail, "candidats.txt"),
           "".join(c + "\n" for c in candidats))
    ecrire(os.path.join(travail, "rejets.txt"),
           "".join("%s | %s | %s\n" % (a, b, c) for a, b, c in rejets))

    # Un message qu'on n'a pas pu lire est peut-etre celui qui comptait. Le
    # marqueur ne doit donc pas le franchir : le lanceur le laisse en place
    # quand ce compteur n'est pas nul, et le passage suivant relit la meme
    # fenetre. deposes.txt empeche le doublon.
    champs = [("statut", "ok"),
              ("fils", len(retenus)),
              ("messages_lus", lus),
              ("entrants", len(entrants)),
              ("echecs", echecs),
              ("jetes", len(rejets)),
              ("depuis", horloge(depuis) if not premier else horloge(depuis) + " (premier passage, %d jours)" % jours),
              ("maxi", maxi),
              ("coupe", "oui" if coupe else "non"),
              ("boite", boite),
              ("identifiants", ou)]

    if sec:
        detail = ["", "RETENUS (%d)" % len(retenus)]
        for r in retenus:
            detail.append("  %s | %s | %s | %s"
                          % (r["dernier"]["de"][:44], r["dernier"]["sujet"][:44],
                             r["motif"], r["qui"] or "-"))
        detail.append("")
        detail.append("JETES (%d)" % len(rejets))
        motifs = {}
        for a, b, c in rejets:
            cle = c.split(",")[0]
            # La ligne des categories Gmail compte pour tous les messages
            # qu'elle represente, pas pour une.
            n = len(ranges) if a == "Gmail" else 1
            motifs[cle] = motifs.get(cle, 0) + n
        for cle in sorted(motifs, key=lambda x: -motifs[x]):
            detail.append("  %-42s %d" % (cle, motifs[cle]))
        detail.append("")
        detail.append("le detail des jetes est dans travail/rejets.txt")
        return sortir(champs, "\n".join(detail))

    return sortir(champs, "fils=%d lus=%d jetes=%d maxi=%s" % (len(retenus), lus, len(rejets), maxi))


if __name__ == "__main__":
    sys.exit(main())
