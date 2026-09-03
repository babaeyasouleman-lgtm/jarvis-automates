# -*- coding: utf-8 -*-
"""Selectionne un monde dans le catalogue etendu sans jamais lire l'index en entier.

Le catalogue vit dans `mondes/`: 152 fichiers `<slug>.css` plus `MONDES.tsv`.
Ne JAMAIS faire `cat MONDES.tsv`, c'est 36 Ko. Ce script filtre et n'imprime
que les candidats, une dizaine de lignes.

  python scripts/monde.py --fond clair --temp chaud
  python scripts/monde.py --titre serif --sans-repet
  python scripts/monde.py --slug cafe --css > monde.css
  python scripts/monde.py --slug cafe --adn

Par defaut les 91 paquets de MARQUE sont exclus: poser l'identite de Ferrari ou
de Stripe sur la page d'un plombier de Gatineau est un probleme de marque, pas
une direction visuelle. `--marques` les rouvre quand il le demande.
"""
import argparse, os, re, sys

# La console Windows est en cp1252 et ferait planter le point median de la
# ligne d'ADN. On force l'UTF-8 en sortie plutot que d'appauvrir le format.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
INDEX = os.path.join(RACINE, "mondes", "MONDES.tsv")
BUILT = os.path.join(RACINE, "BUILT.tsv")

COLS = ["slug", "nom", "categorie", "usage", "fond", "temperature", "accent", "bg", "fg",
        "classe_titre", "police_titre", "classe_corps", "police_corps",
        "titre_px", "corps_px", "rayon_px", "section_y_px", "conteneur_px", "allure"]


def lire_index():
    with open(INDEX, encoding="utf-8") as f:
        entete = f.readline().rstrip("\n").split("\t")
        for l in f:
            v = l.rstrip("\n").split("\t")
            if len(v) == len(entete):
                yield dict(zip(entete, v))


def creme(bg):
    """detect.sh signale `cream-palette` sur un fond chaud tres clair: c'est la
    surface par defaut ou tout le monde retombe. Le savoir AVANT de batir evite
    une trouvaille cuite dans l'image du courriel."""
    if not bg or len(bg) != 7:
        return False
    try:
        import colorsys
        r, g, b = (int(bg[i:i+2], 16)/255 for i in (1, 3, 5))
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return l > 0.90 and 0.04 < s and 0.03 < h < 0.20
    except Exception:
        return False


def recents(n):
    """Le texte brut des n derniers builds. Sert a la regle du non-repete."""
    if not os.path.isfile(BUILT):
        return ""
    with open(BUILT, encoding="utf-8", errors="replace") as f:
        lignes = f.readlines()
    return " ".join(lignes[-n:]).lower()


def deja_vu(m, blob):
    """Le monde entre-t-il en collision avec les builds recents.
    Deux axes verifiables mecaniquement: la police de titrage et l'accent."""
    causes = []
    p = (m["police_titre"] or "").lower()
    if len(p) >= 4 and p in blob:
        causes.append("typo " + m["police_titre"])
    a = (m["accent"] or "").lower()
    if len(a) == 7 and a in blob:
        causes.append("accent " + m["accent"])
    return causes


def main():
    ap = argparse.ArgumentParser(description="Selection de monde, catalogue etendu")
    ap.add_argument("--slug", help="cible un monde precis")
    ap.add_argument("--css", action="store_true", help="imprime son tokens.css")
    ap.add_argument("--adn", action="store_true", help="imprime la ligne d'ADN pre-remplie")
    ap.add_argument("--fond", choices=["clair", "sombre"])
    ap.add_argument("--temp", help="neutre chaud or rouge vert cyan froid violet rose, separees par des virgules")
    ap.add_argument("--titre", help="classe de la police de titre: serif grotesque geometrique condense mono sans")
    ap.add_argument("--cherche", help="motif libre cherche dans le nom, la categorie et l'allure")
    ap.add_argument("--marques", action="store_true", help="inclut les 91 paquets de marque")
    ap.add_argument("--sans-repet", action="store_true", help="ecarte les collisions avec les 5 derniers builds")
    ap.add_argument("--fenetre", type=int, default=5, help="nombre de builds regardes pour le non-repete")
    ap.add_argument("-n", type=int, default=14, help="nombre de candidats imprimes")
    a = ap.parse_args()

    if not os.path.isfile(INDEX):
        sys.exit("index absent: " + INDEX)

    tous = list(lire_index())

    if a.slug:
        m = next((x for x in tous if x["slug"] == a.slug), None)
        if not m:
            sys.exit("monde inconnu: " + a.slug)
        chemin = os.path.join(RACINE, "mondes", a.slug + ".css")
        if a.css:
            sys.stdout.write(open(chemin, encoding="utf-8").read())
            return
        if a.adn:
            print("MONDE %s · HEROS <forme> · ETIQUETTE <traitement> · TYPO %s + %s"
                  % (m["nom"], m["police_titre"], m["police_corps"]))
            print("ACCENT %s %s · RYTHME conteneur %spx, section %spx, corps %spx, titre %spx"
                  % (m["nom"], m["accent"], m["conteneur_px"], m["section_y_px"],
                     m["corps_px"], m["titre_px"]))
            print("SIGNATURE <l'objet du metier>   [rayon %spx, fond %s]"
                  % (m["rayon_px"], m["fond"]))
            print()
            print("tokens: mondes/%s.css" % a.slug)
            print("allure: " + m["allure"])
            return
        for c in COLS:
            print("%-14s %s" % (c, m[c]))
        print("%-14s %s" % ("fichier", "mondes/" + a.slug + ".css"))
        return

    sel = tous
    if not a.marques:
        sel = [m for m in sel if m["usage"] != "MARQUE"]
    if a.fond:
        sel = [m for m in sel if m["fond"] == a.fond]
    if a.temp:
        veut = {t.strip() for t in a.temp.split(",")}
        sel = [m for m in sel if m["temperature"] in veut]
    if a.titre:
        veut = {t.strip() for t in a.titre.split(",")}
        sel = [m for m in sel if m["classe_titre"] in veut]
    if a.cherche:
        r = re.compile(a.cherche, re.I)
        sel = [m for m in sel if r.search(m["nom"] + " " + m["categorie"] + " " + m["allure"])]

    ecartes = []
    if a.sans_repet:
        blob = recents(a.fenetre)
        garde = []
        for m in sel:
            c = deja_vu(m, blob)
            (ecartes if c else garde).append((m, c))
        sel = [m for m, _ in garde]

    print("%d monde(s) sur %d apres filtre%s"
          % (len(sel), len(tous), "" if a.marques else ", marques exclues"))
    print()
    print("%-17s %-7s %-7s %-8s %-6s %-13s %-6s %s"
          % ("slug", "fond", "temp", "accent", "rayon", "titre", "creme", "allure"))
    for m in sel[:a.n]:
        print("%-17s %-7s %-7s %-8s %-6s %-13s %-6s %s"
              % (m["slug"], m["fond"], m["temperature"], m["accent"],
                 m["rayon_px"], m["police_titre"][:13],
                 "creme" if creme(m["bg"]) else "", m["allure"][:56]))
    if len(sel) > a.n:
        print("... %d autres, affiner le filtre ou monter -n" % (len(sel) - a.n))
    if any(creme(m["bg"]) for m in sel[:a.n]):
        print()
        print("creme = detect.sh signalera `cream-palette` sur ce fond. Ce n'est pas")
        print("un defaut, c'est le fond par defaut de l'industrie. Assumer ou eviter.")
    if ecartes:
        print()
        print("ecartes par la regle du non-repete (%d derniers builds):" % a.fenetre)
        for m, c in ecartes[:8]:
            print("  %-17s %s" % (m["slug"], ", ".join(c)))


if __name__ == "__main__":
    main()
