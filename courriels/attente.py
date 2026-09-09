# -*- coding: utf-8 -*-
r"""
Qui attend une reponse de Souleman. 9 septembre 2026.

La phase 4 repond deja a une question : qu'est-ce qui est ARRIVE et qui merite
d'entrer dans le coffre. Elle depose dans 00 Inbox et le bibliothecaire range.

Celui-ci repond a l'autre moitie, celle qui manquait : dans quels fils
quelqu'un a parle en dernier, et depuis combien de temps. C'est le meme trou
que la note de Patrick Renaud decrivait avant nous, « il suit ce qu'on envoie,
jamais ce qu'on recoit », mais pris par l'autre bout : ici ce n'est pas une
reponse qui dort, c'est une absence de reponse que personne ne compte.

----- Il ne decide RIEN, et c'est le point le plus important -------------

Il n'ecrit AUCUNE cle relance: dans 06 Personnes. Souleman l'a coupe net le
8 septembre quand la premiere version des relances balayait ses vingt-quatre
contacts : « ce n'est pas tout le monde qui a besoin de relance, ce n'est pas
super important ». Une relance est une decision qu'il prend sur quelqu'un qui
compte, jamais un balayage.

Ce script produit donc une LISTE, et rien d'autre. La question du soir y pioche
et lui demande. S'il dit oui, la cle se pose. S'il ne dit rien, il ne se passe
rien, et c'est le bon comportement par defaut.

----- Ce qu'il lit, et ce qu'il ignore -----------------------------------

Il ne regarde que les fils ou Souleman a REELLEMENT ecrit. Un fil ou il n'a
jamais parle n'attend rien de lui, meme si l'expediteur est connu du coffre.

Il ignore ensuite tout ce que courriels.py ignore deja, en reutilisant la meme
regle : un no-reply reste un no-reply, une infolettre n'attend pas de reponse.

Et il ne garde que les correspondants que le coffre connait, personnes de
06 Personnes ou clients du pipeline S-WEB. Un inconnu qui n'a pas eu de reponse
n'est pas une relance en attente, c'est peut-etre un refus poli.

----- Ou va le resultat --------------------------------------------------

Dans 10 Questions/Sans reponse.md, un fichier ENTIEREMENT REGENERE a chaque
passage. C'est un etat, pas un journal : ce qui a recu une reponse depuis hier
doit disparaitre tout seul, sinon la liste ne se vide jamais et on retombe sur
le mur de rappels que le message du matin vient d'abandonner.

10 Questions est dans la liste blanche de l'export, donc l'agent WhatsApp le
lit. Le bibliothecaire, lui, a interdiction d'y ecrire.

Aucun accent dans les .ps1 du projet, mais celui-ci est un .py lu en UTF-8 :
les accents y sont permis dans les chaines, comme dans courriels.py.

Usage :
    python attente.py <dossier_base> <coffre> [--sec] [--jours N]

    --sec    affiche le detail et n'ecrit pas le fichier du coffre.
    --jours  a partir de combien de jours de silence une ligne compte.
             Defaut 5. En dessous, ce n'est pas un silence, c'est un delai.
"""

import glob
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

RACINE = "C:/Obsidian"
API = "https://gmail.googleapis.com/gmail/v1/users/me"
JETON = "https://oauth2.googleapis.com/token"
DELAI = 30

# Au-dela, ce n'est plus une relance en attente, c'est de l'histoire. Un fil
# mort depuis six mois ne se relance pas, il se recommence.
JOURS_MAX = 120
# Le silence en dessous duquel on ne dit rien. Trois jours, c'est un week-end.
JOURS_MIN_DEFAUT = 5
# Assez pour couvrir quatre mois d'echanges sans faire exploser l'appel.
PLAFOND = 400

# Ce qui n'attend jamais de reponse, meme dans un fil ou Souleman a ecrit.
BRUIT = re.compile(
    r"no[-_.]?reply|ne[-_.]?pas[-_.]?repondre|donotreply|notifications?@|"
    r"newsletter|mailer|bounce|postmaster|support@|billing@|invoice@|"
    r"calendar-notification|automated|noreply",
    re.I)


def sans_accent(s):
    return (s.replace("é", "e").replace("è", "e").replace("ê", "e")
             .replace("à", "a").replace("â", "a").replace("ç", "c")
             .replace("î", "i").replace("ï", "i").replace("ô", "o")
             .replace("û", "u").replace("ù", "u").replace("ë", "e"))


def norme(s):
    return re.sub(r"\s+", " ", sans_accent((s or "").lower())).strip()


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


def get(url, jeton):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + jeton})
    with urllib.request.urlopen(req, timeout=DELAI) as r:
        return json.loads(r.read().decode("utf-8"))


def lister(q, jeton, plafond):
    sortie, page = [], ""
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


def adresse_de(valeur):
    m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", valeur or "")
    return m.group(0).lower() if m else ""


def nom_de(valeur):
    v = (valeur or "").strip()
    m = re.match(r'^\s*"?([^"<]+?)"?\s*<', v)
    return m.group(1).strip() if m else v.split("@")[0]


def repertoire(coffre):
    """Qui compte, lu dans le coffre. Meme source que courriels.py."""
    gens = []
    for chemin in sorted(glob.glob(os.path.join(coffre, "06 Personnes", "*.md"))):
        nom = os.path.basename(chemin)[:-3]
        try:
            with open(chemin, encoding="utf-8", errors="replace") as f:
                txt = f.read()
        except Exception:
            continue
        alias = []
        for a in re.findall(r"^aliases?:\s*(.+)$", txt, re.M | re.I):
            alias += [x.strip(" []\"'") for x in a.split(",") if x.strip(" []\"'")]
        courriels = set(m.lower() for m in re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", txt))
        gens.append({
            "nom": nom,
            "noms": [norme(nom)] + [norme(a) for a in alias],
            "courriels": courriels,
        })
    return gens


def reconnait(adresse, nom_affiche, gens):
    """La personne du coffre derriere une adresse, ou None.

    L'adresse d'abord, parce qu'elle ne ment pas. Le nom ensuite, et seulement
    s'il correspond ENTIEREMENT a un nom connu : un prenom seul rattacherait
    trois Marie a la meme note.
    """
    a = (adresse or "").lower()
    for p in gens:
        if a and a in p["courriels"]:
            return p
    n = norme(nom_affiche)
    if not n or len(n) < 4:
        return None
    for p in gens:
        for candidat in p["noms"]:
            if candidat and (n == candidat or n.startswith(candidat + " ")
                             or n.endswith(" " + candidat)):
                return p
    return None


def entetes(msg):
    return {h["name"].lower(): h["value"]
            for h in msg.get("payload", {}).get("headers", [])}


def principal():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sec = "--sec" in sys.argv
    jours_min = JOURS_MIN_DEFAUT
    if "--jours" in sys.argv:
        i = sys.argv.index("--jours")
        if i + 1 < len(sys.argv):
            jours_min = int(sys.argv[i + 1])
    if len(args) < 2:
        print("usage: attente.py <dossier_base> <coffre> [--sec] [--jours N]")
        return 2
    base, coffre = args[0], args[1]

    c, _ = identifiants(base)
    if not c:
        print("ECHEC, google.local.json introuvable")
        return 1
    jeton = acces(c)

    profil = get(API + "/profile", jeton)
    boite = (profil.get("emailAddress") or "").lower()
    miennes = set([boite])
    for v in (c.get("identites") or {}).values():
        a = adresse_de(v)
        if a:
            miennes.add(a)

    gens = repertoire(coffre)
    if not gens:
        print("ECHEC, aucune personne dans 06 Personnes")
        return 1

    # Les fils ou Souleman a ecrit, sur la fenetre qui nous interesse. On part
    # de SES messages : un fil ou il n'a jamais parle n'attend rien de lui.
    depuis = (datetime.now() - timedelta(days=JOURS_MAX)).strftime("%Y/%m/%d")
    envoyes = lister("in:sent after:%s" % depuis, jeton, PLAFOND)
    fils = []
    vus = set()
    for m in envoyes:
        t = m.get("threadId")
        if t and t not in vus:
            vus.add(t)
            fils.append(t)

    maintenant = datetime.now()
    attentes = {}
    for t in fils:
        try:
            fil = get(API + "/threads/" + t + "?format=metadata", jeton)
        except Exception:
            continue
        msgs = fil.get("messages", [])
        if not msgs:
            continue
        dernier = msgs[-1]
        h = entetes(dernier)
        de = h.get("from", "")
        adresse = adresse_de(de)

        # Souleman a parle en dernier ? Alors c'est LUI qu'on attend, pas
        # l'inverse. C'est exactement le cas qu'on cherche.
        if adresse in miennes:
            attend_lui = True
        else:
            continue

        if BRUIT.search(de) or BRUIT.search(h.get("to", "")):
            continue

        # A qui a-t-il ecrit ? TOUS les destinataires du dernier message, pas
        # seulement le premier.
        #
        # Le defaut, vu au premier passage reel du 9 septembre 2026 : le fil
        # de la proposition Declic portait « Sylla, Fatouma (Auguste, Tatiana) »
        # dans son en-tete To. En ne lisant que la premiere adresse, on
        # rattachait le fil a l'elue et on perdait Tatiana, qui est justement
        # la personne du coffre. Une virgule dans un nom d'affichage suffisait.
        #
        # On extrait donc toutes les adresses de l'en-tete et on cherche la
        # PREMIERE que le coffre reconnait.
        entete_to = h.get("to", "") + ", " + h.get("cc", "")
        adresses = [a for a in re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", entete_to)]
        adresses = [a.lower() for a in adresses if a.lower() not in miennes]
        if not adresses:
            continue

        qui = None
        for a in adresses:
            qui = reconnait(a, nom_de(entete_to), gens)
            if qui:
                break
        if not qui:
            # Personne du coffre derriere ce fil. On le compte quand meme :
            # trente fils sans reponse dont aucun correspondant n'a de note
            # n'est pas un silence, c'est un coffre incomplet, et ca se dit.
            inconnus.append({"adresse": adresses[0], "quand": dernier.get("internalDate", 0)})
            continue

        try:
            envoye = datetime.fromtimestamp(int(dernier.get("internalDate", 0)) / 1000)
        except Exception:
            continue
        silence = (maintenant - envoye).days
        if silence < jours_min or silence > JOURS_MAX:
            continue

        # Une personne, une ligne : le fil le plus ancien sans reponse. C'est
        # celui qui compte, les autres se regleront avec lui.
        ancien = attentes.get(qui["nom"])
        if ancien and ancien["silence"] >= silence:
            continue
        attentes[qui["nom"]] = {
            "nom": qui["nom"],
            "silence": silence,
            "date": envoye.strftime("%Y-%m-%d"),
            "sujet": (h.get("subject", "") or "(sans objet)").strip()[:90],
        }

    liste = sorted(attentes.values(), key=lambda x: -x["silence"])

    if sec:
        print("fils ou Souleman a ecrit : %d" % len(fils))
        print("en attente de reponse (%d jours ou plus) : %d" % (jours_min, len(liste)))
        for a in liste:
            print("  %-24s %3d j   %s   %s" % (a["nom"][:24], a["silence"], a["date"], a["sujet"][:50]))
        return 0

    dossier = os.path.join(coffre, "10 Questions")
    if not os.path.isdir(dossier):
        os.makedirs(dossier)
    chemin = os.path.join(dossier, "Sans reponse.md")

    lignes = [
        "---",
        "type: ressource",
        "domaine: Personnel",
        "genere: " + maintenant.strftime("%Y-%m-%d %H:%M"),
        "---",
        "",
        "# Sans reponse",
        "",
        "Les gens du coffre a qui Souleman a ecrit en dernier, et qui n'ont pas",
        "repondu depuis au moins %d jours." % jours_min,
        "",
        "**Ce fichier est regenere en entier a chaque passage.** C'est un etat,",
        "pas un journal : ce qui recoit une reponse disparait tout seul. Ne pas",
        "l'editer a la main, et ne pas s'en servir comme d'une liste de taches.",
        "",
        "**Personne n'est mis en relance automatiquement.** Une relance est une",
        "decision, pas un balayage. La question du soir pioche ici et demande.",
        "",
    ]
    if not liste:
        lignes.append("Personne n'attend de reponse en ce moment.")
    else:
        for a in liste:
            lignes.append("- [[%s]] : %d jours de silence, ecrit le %s, sujet %s"
                          % (a["nom"], a["silence"], a["date"], a["sujet"]))
    lignes.append("")

    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes))
    print("ecrit %s, %d personne(s)" % (chemin, len(liste)))
    return 0


if __name__ == "__main__":
    sys.exit(principal())
