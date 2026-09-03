#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
assemble.py  ---  JSON de recolte.py + gabarit  ->  index.html rempli.

    python assemble.py --json prospect.json --gabarit ../gabarits/batiment.html \
                       --out sortie/index.html --ville Gatineau

Deterministe, aucun jugement. La variete vient de trois sources independantes:
la palette echantillonnee sur LEUR logo, l'appairage de polices tire du banc, et
leur contenu. Deux prospects du meme metier ne recoivent jamais la meme typo le
meme mois: l'index de typo est derive du nom, pas tire au hasard.
"""
import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import unicodedata

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# ------------------------------------------------------------------ couleur

def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexa(t):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in t)


def lum(h):
    def c(v):
        v /= 255.0
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = rgb(h)
    return .2126 * c(r) + .7152 * c(g) + .0722 * c(b)


def contraste(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + .05) / (min(la, lb) + .05)


def melange(a, b, t):
    ra, rb = rgb(a), rgb(b)
    return hexa([ra[i] + (rb[i] - ra[i]) * t for i in range(3)])


def lisible_sur(fond):
    """Noir ou blanc, celui qui passe. Jamais un gris a l'aveugle."""
    return "#ffffff" if contraste("#ffffff", fond) >= contraste("#111111", fond) else "#111111"


def eclaircir_jusqu_a(couleur, fond, cible=4.5):
    """Monte la couleur vers le blanc jusqu'a atteindre le contraste demande."""
    c = couleur
    for i in range(1, 21):
        if contraste(c, fond) >= cible:
            return c
        c = melange(couleur, "#ffffff", i * .05)
    return c


ACCENT_DEFAUT = {"batiment": "#2E6FD4", "soin": "#9A6B58",
                 "pro": "#2F5E52", "entretien": "#1F7A5A"}


def palette(accent, famille):
    remplace = False
    if not accent:
        accent, remplace = ACCENT_DEFAUT.get(famille, "#2E6FD4"), True
    champ = melange("#15171A", accent, .07)
    return {
        "ACCENT": accent,
        "SUR_ACCENT": lisible_sur(accent),
        "SUR_ACCENT_DOUX": melange(lisible_sur(accent), accent, .35),
        "ACCENT_CLAIR": eclaircir_jusqu_a(accent, champ, 4.5),
        "CHAMP": champ,
        "CHAMP_2": melange(champ, "#ffffff", .06),
        "HALO": melange(champ, accent, .55),
        "PAPIER": "#F2F1EE",
        "ENCRE": "#16181B",
        "GRIS": "#71757B",
        "FILET": "#DCDAD5",
    }, remplace


MONDES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "prospect-site", "mondes")


def applique_monde(pal, slug):
    """Remplace les quatre constantes de papier par celles d'un monde du
    catalogue etendu. L'ACCENT ne bouge pas: il vient de LEUR logo, c'est la
    regle. Sans ce drapeau, les quatre valeurs sont les memes a chaque build,
    et deux prospects du meme metier la meme semaine se ressemblent.

    Rend (palette, note). Leve SystemExit si le monde ne tient pas au contraste:
    l'image du courriel est recompressee en JPEG sous 500 Ko et lue dehors sur
    un telephone, le plancher est donc plus haut qu'a l'ecran."""
    chemin = os.path.join(MONDES, slug + ".css")
    if not os.path.isfile(chemin):
        sys.exit("monde inconnu: %s (voir prospect-site/scripts/monde.py)" % slug)
    with io.open(chemin, encoding="utf-8") as f:
        css = re.sub(r"/\*.*?\*/", "", f.read(), flags=re.S)
    bloc = re.search(r":root\s*\{(.*?)\}", css, re.S)
    t = {}
    for k, v in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", bloc.group(1) if bloc else css):
        t.setdefault(k, v.strip())

    def h(*cles):
        for c in cles:
            m = re.search(r"#([0-9A-Fa-f]{6})\b", t.get(c, ""))
            if m:
                return "#" + m.group(1).lower()
        return ""

    papier, encre = h("--bg", "--surface"), h("--fg", "--text")
    gris, filet = h("--muted", "--fg-2"), h("--border", "--border-soft")
    if not (papier and encre):
        sys.exit("monde %s: pas de --bg/--fg lisibles en hex, palette inchangee" % slug)
    if lum(papier) < .35:
        sys.exit("monde %s: fond sombre, le gabarit suppose un papier clair" % slug)

    c = contraste(encre, papier)
    if c < 7:
        sys.exit("monde %s refuse: encre sur papier a %.1f:1, plancher 7:1" % (slug, c))
    pal["PAPIER"], pal["ENCRE"] = papier, encre
    if gris and contraste(gris, papier) >= 4.5:
        pal["GRIS"] = gris
    if filet:
        pal["FILET"] = filet
    return pal, "monde=%s papier=%s encre=%s (%.1f:1)" % (slug, papier, encre, c)


# ------------------------------------------------------------------ typo

BANC_TYPO = [
    ("Schibsted Grotesk", "Onest", "Schibsted+Grotesk:wght@500;600;700|Onest:wght@400;500;600"),
    ("Familjen Grotesk", "Inter Tight", "Familjen+Grotesk:wght@500;600;700|Inter+Tight:wght@400;500;600"),
    ("Manrope", "Public Sans", "Manrope:wght@500;600;800|Public+Sans:wght@400;500;600"),
    ("Bricolage Grotesque", "Inter", "Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700|Inter:wght@400;500;600"),
    ("Outfit", "Instrument Sans", "Outfit:wght@500;600;700|Instrument+Sans:wght@400;500;600"),
    ("Archivo", "Karla", "Archivo:wght@500;600;700|Karla:wght@400;500;600"),
    ("Darker Grotesque", "Hanken Grotesk", "Darker+Grotesque:wght@600;700;800|Hanken+Grotesk:wght@400;500;600"),
    ("Sora", "Rubik", "Sora:wght@500;600;700|Rubik:wght@400;500;600"),
]


def typo(nom, forcee=None):
    i = forcee if forcee is not None else sum(ord(c) * (k + 3) for k, c in enumerate(nom)) % len(BANC_TYPO)
    t, c, q = BANC_TYPO[i % len(BANC_TYPO)]
    return {"FONT_TITRE": t, "FONT_CORPS": c,
            "FONT_Q": "&family=".join(q.split("|"))}, i % len(BANC_TYPO)


# ------------------------------------------------------------------ contenu

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "contenu", "metiers.json"), encoding="utf-8") as f:
    METIERS = json.load(f)


def sans_accent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def metier(d):
    foin = sans_accent(" ".join(filter(None, [
        d.get("titre_page") or "", d.get("description") or "",
        d.get("nom") or "", " ".join(d.get("extraits", [])[:25])])))
    meilleur, score = None, 0
    for cle, fiche in METIERS.items():
        if cle.startswith("_"):
            continue
        n = sum(foin.count(m) for m in fiche["mots"])
        if n > score:
            meilleur, score = cle, n
    return (meilleur or "_defaut"), score


# ------------------------------------------------------------------ images

def telecharge(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "20", "-A", UA, url],
                       capture_output=True)
    return r.stdout


def data_uri(octets, url):
    ext = (url.rsplit(".", 1)[-1] or "png").lower().split("?")[0]
    mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp",
            "svg": "svg+xml"}.get(ext, "png")
    return "data:image/%s;base64,%s" % (mime, base64.b64encode(octets).decode("ascii"))


def choisir_photo(photos):
    """Paysage, 1600px ou plus. Sinon rien: on bascule sur la variante sans photo."""
    for p in photos:
        if p.get("paysage") and p["w"] >= 1600:
            return p
    for p in photos:
        if p.get("paysage") and p["w"] >= 1200 and p["ratio"] >= 1.5:
            return p
    return None


# ------------------------------------------------------------------ montage

def echappe(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bloc_conditionnel(gab, nom, garder):
    d, f = "<!--SI_%s-->" % nom, "<!--/SI_%s-->" % nom
    while d in gab and f in gab:
        i, j = gab.index(d), gab.index(f)
        dedans = gab[i + len(d):j]
        gab = gab[:i] + (dedans if garder else "") + gab[j + len(f):]
    return gab


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--json", required=True)
    p.add_argument("--gabarit", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--ville", default="")
    p.add_argument("--typo", type=int)
    p.add_argument("--langue", choices=["fr", "en"])
    p.add_argument("--monde", help="slug du catalogue etendu, ex: cafe. "
                                   "Remplace le papier, jamais l'accent du logo")
    a = p.parse_args()

    with io.open(a.json, encoding="utf-8") as f:
        d = json.load(f)
    with io.open(a.gabarit, encoding="utf-8") as f:
        gab = f.read()

    cle, score = metier(d)
    fiche = METIERS[cle]
    lg = a.langue or (d.get("langue_principale") or "fr")
    lg = lg if lg in ("fr", "en") else "fr"
    txt = fiche[lg]
    ville = a.ville or "votre secteur" if lg == "fr" else (a.ville or "your area")

    pal, accent_remplace = palette((d.get("logo") or {}).get("accent"), fiche["famille"])
    note_monde = ""
    if a.monde:
        pal, note_monde = applique_monde(pal, a.monde)
    tf, itypo = typo(d.get("nom") or "x", a.typo)

    photo = choisir_photo(d.get("photos") or [])
    variante = "photo" if photo else "sans"

    nom = d.get("nom") or ""
    tel = d.get("telephone") or ""
    tel_brut = re.sub(r"\D", "", tel)

    # titre: nom geant sur la photo, titre bicolore sans photo
    if photo:
        titre = '<div class="nomgeant">%s</div>' % echappe(nom)
        h1vw, h1max = 5.4, 74
    else:
        titre = '<h1><span>%s</span> %s</h1>' % (
            echappe(txt["titre_gris"]), echappe(txt["titre_plein"]))
        n = len(txt["titre_gris"]) + len(txt["titre_plein"])
        h1vw, h1max = (4.9, 66) if n > 46 else (5.6, 78)

    # logo, ou mot-symbole en repli
    lg_o = d.get("logo") or {}
    if lg_o.get("b64"):
        marque = '<img src="%s" alt="%s">' % (
            data_uri(base64.b64decode(lg_o["b64"]), lg_o["url"]), echappe(nom))
    else:
        marque = "<b>%s</b>" % echappe(nom)

    fond = ""
    if photo:
        oct_ = telecharge(photo["url"])
        if oct_ and len(oct_) > 2000:
            fond = '<img class="fond" src="%s" alt="">' % data_uri(oct_, photo["url"])
        else:
            variante, titre = "sans", '<h1><span>%s</span> %s</h1>' % (
                echappe(txt["titre_gris"]), echappe(txt["titre_plein"]))

    # un logo empile (rapport sous 1.5) disparait a 34px de haut: vu sur Alictro, 4500x3872
    logo_h = 48 if lg_o.get("empile") else 34
    preuve = d.get("adresse") or txt["preuve_repli"]
    l_preuve = txt["l_preuve"] if d.get("adresse") else txt["l_preuve_repli"]
    l1, l2 = ("FR", "EN") if lg == "fr" else ("EN", "FR")

    val = {
        "LANG": lg, "NOM": echappe(nom), "MARQUE": marque,
        "TEL": echappe(tel), "TEL_BRUT": tel_brut,
        "NAV": "".join('<a href="#">%s</a>' % echappe(x) for x in txt["nav"]),
        "L1": l1, "L2": l2,
        "VARIANTE": variante, "FOND": fond, "TITRE": titre,
        "H1_VW": h1vw, "H1_MAX": h1max,
        "CASSE_NOM": "uppercase" if len(nom) <= 22 else "none",
        "ETIQUETTE": echappe(txt["etiquette"]),
        "LOGO_H": logo_h, "MARK_CHIP": "chip" if lg_o.get("clair") else "",
        "L_APPEL": echappe(txt["l_appel"]), "L_PREUVE": echappe(l_preuve),
        "PREUVE": echappe(preuve),
        "SOUS": echappe(txt["sous"].replace("{ville}", ville)),
        "CTA1": echappe(txt["cta1"]), "CTA2": echappe(txt["cta2"]),
        "ETIQ2": echappe(txt["etiq2"]),
        "TITRE2A": echappe(txt["titre2a"]), "TITRE2B": echappe(txt["titre2b"]),
        "PUCES": "".join("<s>%s</s>" % echappe(x) for x in txt["puces"][:3]) +
                 '<em>+%d</em>' % max(0, len(txt["puces"]) - 3),
    }
    val.update(pal)
    val.update(tf)

    gab = bloc_conditionnel(gab, "PHOTO", bool(photo))
    gab = bloc_conditionnel(gab, "SANS_PHOTO", not photo)
    for k, v in val.items():
        gab = gab.replace("{{%s}}" % k, str(v))

    restants = re.findall(r"\{\{([A-Z0-9_]+)\}\}", gab)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    with io.open(a.out, "w", encoding="utf-8") as f:
        f.write(gab)

    print("%-24s metier=%-11s(%d) variante=%-5s typo=%d %s+%s accent=%s%s" % (
        nom[:24], cle, score, variante, itypo, tf["FONT_TITRE"], tf["FONT_CORPS"],
        pal["ACCENT"], " REPLI" if accent_remplace else ""))
    if note_monde:
        print("  " + note_monde)
    if restants:
        print("  JETONS NON REMPLIS: %s" % ", ".join(sorted(set(restants))))
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
