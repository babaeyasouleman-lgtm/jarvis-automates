#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
polices.py  ---  cache local de polices Google, et fonts.css encode en base64.

    python scripts/polices.py --titre "Radio Canada Big" --corps "IBM Plex Mono" \
                              --out "Prospect/teaser/assets/fonts.css"

Le premier appel pour un appairage telecharge le sous-ensemble latin depuis
fonts.gstatic.com et le range dans contenu/polices/. Tous les appels suivants,
pour ce prospect ou pour un autre, ne touchent plus au reseau.

Pourquoi le sous-ensemble latin seulement: c'est le bloc U+0000 de la reponse de
Google Fonts. Le latin-ext, le cyrillique et le grec triplent le poids et aucun
prospect de l'Outaouais n'en a besoin.

Les noms de famille sortent du banc libre de ../prospect-site/DIRECTIONS.md,
axe 4. Ce script ne choisit rien, il execute.
"""
import argparse
import base64
import os
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

ICI = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ICI, "..", "contenu", "polices")

# Plage de graisses demandee a Google par famille. Une variable couvre toute la
# plage en un seul fichier, ce qui est toujours plus leger que trois statiques.
PLAGE = {
    "Radio Canada Big": "wght@400..700",
    "IBM Plex Mono":    "wght@400;500;600",
    "Geist":            "wght@400..700",
    "Geist Mono":       "wght@400..600",
    "Anybody":          "wght@400..800",
    "Antonio":          "wght@400..700",
    "Zilla Slab":       "wght@400;500;600;700",
    "Bitter":           "wght@400..700",
    "Vollkorn":         "wght@400..700",
    "Marcellus":        "",
}
DEFAUT = "wght@400..700"


def slug(nom):
    return re.sub(r"[^a-z0-9]+", "-", nom.lower()).strip("-")


def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=45).read()


def latin(nom):
    """Retourne [(graisse, octets woff2)] du sous-ensemble latin de base.

    La plage `wght@400..700` ne vaut que pour une police VARIABLE. Sur une
    statique (Amiri, Marcellus, Lustria), Google repond 400 Bad Request sans
    rien expliquer, et le build s'arrete sur une trace urllib illisible. On
    redescend donc tout seul: plage variable, puis graisses discretes, puis
    aucune specification. Le premier essai qui passe gagne."""
    essais = []
    plage = PLAGE.get(nom, DEFAUT)
    if plage:
        essais.append(plage)
    for repli in ("wght@400;700", ""):
        if repli not in essais:
            essais.append(repli)

    css, dernier = None, None
    for i, p in enumerate(essais):
        fam = nom.replace(" ", "+") + (":" + p if p else "")
        try:
            css = http("https://fonts.googleapis.com/css2?family=%s&display=block" % fam).decode("utf-8")
            if i:
                print("  repli       %-42s %s" % (nom, p or "aucune graisse demandee"))
            break
        except Exception as e:
            dernier = e
    if css is None:
        raise SystemExit("polices.py: Google refuse '%s' sur les %d essais de graisse (%s).\n"
                         "Verifier l'orthographe exacte du nom sur fonts.google.com."
                         % (nom, len(essais), dernier))
    blocs = []
    motif = (r"font-weight:\s*([^;]+);.*?src:\s*url\((https[^)]+\.woff2)\)"
             r".*?unicode-range:\s*([^;]+);")
    for m in re.finditer(motif, css, re.S):
        if "U+0000" not in m.group(3):          # latin de base seulement
            continue
        blocs.append((m.group(1).strip(), m.group(2)))
    if not blocs:
        raise SystemExit("polices.py: aucun sous-ensemble latin pour '%s'.\n"
                         "Verifier l'orthographe exacte du nom sur fonts.google.com." % nom)
    return blocs


def fichiers(nom):
    """Telecharge si absent, retourne [(graisse, chemin local)]."""
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)
    sortie = []
    for i, (poids, url) in enumerate(latin(nom)):
        # le poids entre dans le nom: '400 700' d'une variable != '500' d'une statique
        dest = os.path.join(CACHE, "%s__%s.woff2" % (slug(nom), slug(poids)))
        if not os.path.exists(dest):
            data = http(url)
            open(dest, "wb").write(data)
            print("  telecharge  %-42s %5d octets" % (os.path.basename(dest), len(data)))
        else:
            print("  en cache    %-42s %5d octets" % (os.path.basename(dest),
                                                      os.path.getsize(dest)))
        sortie.append((poids, dest))
    return sortie


def face(alias, poids, chemin):
    b = base64.b64encode(open(chemin, "rb").read()).decode()
    return ("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) "
            "format('woff2');font-weight:%s;font-display:block}\n" % (alias, b, poids))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--titre", required=True, help="famille de titrage, nom exact Google Fonts")
    ap.add_argument("--corps", required=True, help="famille de corps, nom exact Google Fonts")
    ap.add_argument("--out", required=True, help="chemin du fonts.css a ecrire")
    ap.add_argument("--alias-titre", default="Titre")
    ap.add_argument("--alias-corps", default="Corps")
    a = ap.parse_args()

    css = ""
    total = 0
    for nom, alias in ((a.titre, a.alias_titre), (a.corps, a.alias_corps)):
        print("%s  ->  '%s'" % (nom, alias))
        for poids, chemin in fichiers(nom):
            css += face(alias, poids, chemin)
            total += os.path.getsize(chemin)

    d = os.path.dirname(os.path.abspath(a.out))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    open(a.out, "w", encoding="utf-8").write(css)

    print("\n%s ecrit, %d Ko de woff2 pour %d Ko de base64"
          % (a.out, total // 1024, os.path.getsize(a.out) // 1024))
    if total > 110 * 1024:
        print("ATTENTION: au-dela de ~110 Ko de woff2, retirer une graisse.", file=sys.stderr)


if __name__ == "__main__":
    main()
