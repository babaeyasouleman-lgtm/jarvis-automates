#!/usr/bin/env python3
"""moisson.py - remplit FILE-ATTENTE.tsv depuis Google Maps, sans partenaire.

    python moisson.py "salon de coiffure" --ville "Gatineau QC"
    python moisson.py "toiture" --ville "Ottawa ON" --metier toiture --max 25
    python moisson.py --requetes lots/aout.txt --seuil 2
    python moisson.py --rejouer resultats/2026-08-21-coiffure.csv

Le binaire vient de https://github.com/gosom/google-maps-scraper (MIT).
Aucune cle API. Il pilote un Chrome sans interface, donc il est lent:
compter environ 2 minutes par requete a --profondeur 1, et le double avec
--courriels qui va crawler chaque site pour y trouver une adresse.

Ecrit dans le meme FILE-ATTENTE.tsv que lot.py, avec les memes dix colonnes.
Ne remplace jamais une fiche existante et n'ecrit jamais de statut.
"""
import argparse
import csv
import datetime
import io
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lot  # noqa: E402  meme dossier, meme format, une seule source de verite

BIN = Path(os.environ.get("GMAPS_BIN", Path.home() / ".local" / "bin" / "gmaps.exe"))
BRUT = lot.BASE / "moisson"

# Un site sur une de ces plateformes est un site faible: c'est le prospect ideal.
PLATEFORMES = (
    "facebook.com", "instagram.com", "linktr.ee", "business.site", "wixsite.com",
    "squarespace.com", "godaddysites.com", "wordpress.com", "weebly.com",
    "jimdosite.com", "e-monsite.com", "webnode", "site123", "yolasite.com",
    "myshopify.com", "square.site", "sites.google.com", "wix.com",
)

# Les chaines n'achetent pas un site a un pigiste. Le siege social decide.
CHAINES = (
    "great clips", "first choice", "fantastic sams", "supercuts", "sport clips",
    "tim hortons", "mcdonald", "subway", "a&w", "pizza pizza", "dairy queen",
    "jean coutu", "pharmaprix", "shoppers drug", "uniprix", "familiprix",
    "canadian tire", "home depot", "rona", "walmart", "costco", "ikea",
    "desjardins", "banque", "scotiabank", "rbc ", "cibc", "bmo ",
)


def sansaccents(s):
    n = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in n if not unicodedata.combining(c))


def slug(s, n=28):
    s = sansaccents(s).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:n].strip("-")


def ville_de(adresse, defaut):
    """Google ecrit 'rue, Ville, QC J8Y 3Y8'. La ville est l'avant-derniere case."""
    cases = [c.strip() for c in (adresse or "").split(",") if c.strip()]
    if len(cases) >= 2:
        v = cases[-2]
        if v and not re.fullmatch(r"[A-Z]{2}\s*[A-Z0-9 ]{0,8}", v):
            return v
    return defaut


def domaine(url):
    m = re.match(r"https?://([^/]+)", (url or "").strip(), re.I)
    return m.group(1).lower().lstrip("www.") if m else ""


def force(site):
    """0 = aucun site, 1 = site sur plateforme, 2 = domaine a eux. Plus bas = meilleur."""
    if not (site or "").strip():
        return 0
    d = domaine(site)
    return 1 if any(p in d for p in PLATEFORMES) else 2


def nombre(v):
    try:
        return int(float(str(v).replace(",", "").strip() or 0))
    except ValueError:
        return 0


def note(v):
    try:
        return float(str(v).replace(",", ".").strip() or 0)
    except ValueError:
        return 0.0


def score(r):
    """Ce qui fait un bon prospect: du monde qui rentre, et rien en ligne pour l'accueillir."""
    f = force(r.get("website"))
    s = {0: 5, 1: 4, 2: 1}[f]
    avis = nombre(r.get("review_count"))
    if avis >= 200:
        s += 3
    elif avis >= 60:
        s += 2
    elif avis >= 20:
        s += 1
    if note(r.get("review_rating")) >= 4.5:
        s += 1
    if not (r.get("phone") or "").strip() and not (r.get("emails") or "").strip():
        s -= 4          # injoignable, il ne sert a rien de le garder
    return s


def raison(r):
    f = force(r.get("website"))
    if f == 0:
        return "aucun site, %s avis" % nombre(r.get("review_count"))
    if f == 1:
        return "site sur %s, %s avis" % (domaine(r.get("website")), nombre(r.get("review_count")))
    return "site a refaire (%s), %s avis" % (domaine(r.get("website")), nombre(r.get("review_count")))


def chaine(nom):
    n = sansaccents(nom).lower()
    return any(c in n for c in CHAINES)


# Adresses techniques que le crawl ramene des pages, jamais un contact.
POUBELLE = ("sentry", "wixpress", "example.com", "domain.com", "email.com",
            "yourdomain", "godaddy", "squarespace.com", "sentry.io", "wordpress.org",
            "no-reply", "noreply", "donotreply")


def premier_courriel(v):
    """La premiere adresse humaine du lot.

    Le crawl ramene des adresses de telemetrie qui ressemblent a des courriels:
    Wix expose 605a7baede844d278b89dc95ae0a9123@sentry-next.wixpress.com sur
    chaque page. Un envoi la-dessus est perdu, et pire, il salit le domaine
    expediteur pour rien.
    """
    for e in re.split(r"[,;\s]+", (v or "").strip()):
        e = e.strip().strip(".").lower()
        if "@" not in e or len(e) >= 80:
            continue
        local, _, dom = e.partition("@")
        if "." not in dom or not re.fullmatch(r"[a-z0-9._%+-]+", local):
            continue
        if any(p in e for p in POUBELLE):
            continue
        if re.fullmatch(r"[0-9a-f]{16,}", local):   # identifiant, pas un nom
            continue
        if dom.rsplit(".", 1)[-1] in ("png", "jpg", "jpeg", "webp", "svg", "gif"):
            continue
        return e
    return ""


def lancer(requetes, sortie, profondeur, courriels, langue):
    if not BIN.exists():
        sys.exit(
            "binaire absent: %s\n"
            "  curl -sL -o \"%s\" \\\n"
            "    https://github.com/gosom/google-maps-scraper/releases/download/"
            "v1.17.3/google_maps_scraper-1.17.3-windows-amd64.exe" % (BIN, BIN))
    BRUT.mkdir(parents=True, exist_ok=True)
    qf = BRUT / "requetes.txt"
    qf.write_text("\n".join(requetes) + "\n", encoding="utf-8")
    cmd = [str(BIN), "-input", str(qf), "-results", str(sortie),
           "-depth", str(profondeur), "-c", "1", "-lang", langue,
           "-exit-on-inactivity", "3m"]
    if courriels:
        cmd.append("-email")
    print("moisson: %d requete(s), profondeur %d%s"
          % (len(requetes), profondeur, ", avec courriels" if courriels else ""))
    print("  patience, environ %d min" % (len(requetes) * (4 if courriels else 2)))
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if r.returncode != 0 or not sortie.exists():
        sys.exit("le scraper a echoue (code %s). Relancer sans -results pour voir le journal."
                 % r.returncode)
    return sortie


BUREAU = Path(r"C:\Users\Administrator\OneDrive\Bureau")
BUILT = Path(__file__).resolve().parent.parent.parent / "prospect-site" / "BUILT.tsv"


# Ces mots ne distinguent personne: la moitie des commerces du coin les portent.
GENERIQUES = {
    "clinique", "clinic", "centre", "center", "salon", "studio", "groupe", "group",
    "medical", "medicale", "medico", "medecine", "aesthetic", "aesthetics",
    "esthetique", "esthetics", "beaute", "beauty", "spa", "medispa", "medspa",
    "coiffure", "barbier", "barber", "hair", "nails", "ongles", "laser", "skin",
    "gatineau", "ottawa", "aylmer", "hull", "buckingham", "outaouais", "quebec",
    "canada", "inc", "enr", "ltee", "ltd", "services", "service", "solutions",
    "construction", "renovation", "toiture", "roofing", "plomberie", "plumbing",
    "electrique", "electric", "dentaire", "dental", "tattoo", "photo", "web",
}


# Ses propres dossiers de travail. Leurs noms ne designent aucun prospect et
# fabriqueraient des faux positifs sur des mots courants.
NON_PROSPECTS = {
    "prospection", "processus", "communication", "devis", "navigateurs",
    "suite office", "assets", "archives", "factures", "contrats", "logos",
}


def jetons(nom):
    """Les mots qui identifient vraiment une entreprise, le bruit enleve.

    Le CamelCase est coupe avant tout: le dossier s'appelle PoseTaPierre et
    Google ecrit Pose ta Pierre. Sans la coupe, aucun mot commun.
    """
    n = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", nom or "")
    mots = re.split(r"[^a-z0-9]+", sansaccents(n).lower())
    return {m for m in mots if len(m) >= 4 and m not in GENERIQUES}


def deja_batis():
    """Les prospects pour qui une demo existe deja. Deux sources, aucune n'est propre.

    Les dossiers du Bureau portent un nom court et fiable. La colonne nom de
    BUILT.tsv est du texte libre ou le nom vient en tete, avant la premiere
    virgule ou parenthese.

    Le rapprochement se fait sur les mots distinctifs et non sur le nom entier:
    le dossier dit "Clinique-Infinium", Google dit "INFINIUM Medecine Esthetique
    | Aesthetic Medicine". Aucun prefixe commun, un seul mot qui compte. Sans ce
    garde-fou, Infinium est ressortie comme prospect neuf alors que sa demo etait
    deja livree.
    """
    vus = []
    noms = [d.name for d in BUREAU.glob("*/")
            if d.is_dir() and not d.name.startswith((".", "$"))]
    # Il livre aussi des demos en fichier unique a la racine: <Nom>-demo.html
    noms += [re.sub(r"[-_](demo|fonds|site|v\d+).*$", "", f.stem, flags=re.I)
             for f in BUREAU.glob("*.html")]
    for n in noms:
        if n.strip().lower() in NON_PROSPECTS:
            continue
        j = jetons(n)
        if j:
            vus.append(j)
    if BUILT.exists():
        for r in lot.lire(BUILT, ["date", "nom"]):
            tete = re.split(r"[,(]", r.get("nom") or "", 1)[0]
            j = jetons(tete)
            if j:
                vus.append(j)
    return vus


def deja_bati(nom, vus):
    j = jetons(nom)
    if not j:
        return False
    return any(j & v for v in vus)


def deja_connus():
    """Telephones, domaines et courriels deja dans la file ou deja contactes."""
    tel, dom, mail = set(), set(), set()
    for r in lot.lire(lot.FILE, lot.COLS):
        t = re.sub(r"\D", "", r.get("telephone") or "")
        if len(t) >= 10:
            tel.add(t[-10:])
        if r.get("site"):
            dom.add(domaine(r["site"]))
        if r.get("courriel"):
            mail.add(r["courriel"].strip().lower())
    for r in lot.lire(lot.SENT, lot.SENT_COLS):
        if r.get("courriel"):
            mail.add(r["courriel"].strip().lower())
    return tel, dom, mail


def moissonner(csv_path, metier_defaut, ville_defaut, seuil, plafond):
    tel_vus, dom_vus, mail_vus = deja_connus()
    stop = lot.stops()
    batis = deja_batis()
    ids = {r.get("id") for r in lot.lire(lot.FILE, lot.COLS)}
    gardes, rejets = [], {"chaine": 0, "doublon": 0, "faible": 0,
                          "injoignable": 0, "deja bati": 0}

    with io.open(csv_path, encoding="utf-8", newline="") as f:
        brut = list(csv.DictReader(f))

    for r in sorted(brut, key=score, reverse=True):
        nom = (r.get("title") or "").strip()
        if not nom:
            continue
        if chaine(nom):
            rejets["chaine"] += 1
            continue
        if deja_bati(nom, batis):
            rejets["deja bati"] += 1
            continue

        t = re.sub(r"\D", "", r.get("phone") or "")
        t10 = t[-10:] if len(t) >= 10 else ""
        d = domaine(r.get("website"))
        mail = premier_courriel(r.get("emails"))

        if (t10 and t10 in tel_vus) or (d and d in dom_vus) or (mail and mail in mail_vus):
            rejets["doublon"] += 1
            continue
        if mail and (mail in stop or mail.split("@", 1)[1] in stop):
            rejets["doublon"] += 1
            continue
        if not t10 and not mail:
            rejets["injoignable"] += 1
            continue

        s = score(r)
        if s < seuil:
            rejets["faible"] += 1
            continue

        ville = ville_de(r.get("address"), ville_defaut)
        base = "%s-%s" % (slug(ville, 3), slug(nom))
        pid, n = base, 2
        while pid in ids:
            pid, n = "%s-%d" % (base, n), n + 1
        ids.add(pid)

        gardes.append({
            "id": pid,
            "nom": nom,
            "ville": ville,
            "metier": metier_defaut or (r.get("category") or "").strip(),
            "site": (r.get("website") or "").strip(),
            "courriel": mail,
            "decideur": "",
            "telephone": (r.get("phone") or "").strip(),
            "statut": "",
            "note": "moisson %s, score %d, %s" % (datetime.date.today().isoformat(), s, raison(r)),
        })
        if t10:
            tel_vus.add(t10)
        if d:
            dom_vus.add(d)
        if mail:
            mail_vus.add(mail)
        if plafond and len(gardes) >= plafond:
            break

    return brut, gardes, rejets


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("metier", nargs="?", help='ex: "salon de coiffure"')
    p.add_argument("--ville", default="Gatineau QC")
    p.add_argument("--requetes", help="fichier, une requete par ligne")
    p.add_argument("--rejouer", help="retrier un CSV deja moissonne, sans rappeler Google")
    p.add_argument("--metier", dest="etiquette", default="",
                   help="ce qui va dans la colonne metier (defaut: la categorie Google)")
    p.add_argument("--profondeur", type=int, default=1, help="pages de defilement (defaut 1)")
    p.add_argument("--seuil", type=int, default=4,
                   help="score minimum. 4 garde les sites faibles, 6 uniquement les sans-site")
    p.add_argument("--max", type=int, default=0, dest="plafond")
    p.add_argument("--courriels", action="store_true",
                   help="crawler chaque site pour trouver une adresse. Deux fois plus lent.")
    p.add_argument("--langue", default="fr")
    p.add_argument("--essai", action="store_true", help="afficher sans rien ecrire")
    a = p.parse_args()

    if a.rejouer:
        chemin = Path(a.rejouer)
    else:
        if a.requetes:
            requetes = [l.strip() for l in Path(a.requetes).read_text(encoding="utf-8").splitlines()
                        if l.strip() and not l.startswith("#")]
        elif a.metier:
            requetes = ["%s %s" % (a.metier, a.ville)]
        else:
            p.error("donner un metier, --requetes ou --rejouer")
        BRUT.mkdir(parents=True, exist_ok=True)
        chemin = BRUT / ("%s-%s.csv" % (datetime.date.today().isoformat(),
                                        slug(a.metier or Path(a.requetes).stem)))
        lancer(requetes, chemin, a.profondeur, a.courriels, a.langue)

    brut, gardes, rejets = moissonner(chemin, a.etiquette, a.ville, a.seuil, a.plafond)

    print("\n%d fiches ramenees, %d gardees" % (len(brut), len(gardes)))
    print("  ecartees: %d chaine, %d deja bati, %d doublon, %d injoignable, %d sous le seuil"
          % (rejets["chaine"], rejets["deja bati"], rejets["doublon"],
             rejets["injoignable"], rejets["faible"]))
    print("  brut conserve: %s\n" % chemin)
    for g in gardes:
        print("  %-26s %-12s %-22s %s" % (g["id"][:26], g["ville"][:12],
                                          (g["courriel"] or g["telephone"])[:22], g["note"]))
    if a.essai:
        print("\n--essai: rien ecrit.")
        return
    if not gardes:
        print("\nrien a ajouter.")
        return

    lot.BASE.mkdir(parents=True, exist_ok=True)
    for g in gardes:
        lot.ajouter(lot.FILE, lot.COLS, g)
    print("\n%d fiche(s) ajoutee(s) a %s" % (len(gardes), lot.FILE))
    print("Verifier avant d'envoyer:  python lot.py suivants 3")


if __name__ == "__main__":
    main()
