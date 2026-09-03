#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
recolte.py  ---  Un seul appel reseau sur le site d'un prospect, puis tout ce dont
l'assemblage a besoin: identite, contenu, logo, couleurs echantillonnees, photos
utilisables, et les signaux mesurables qui declenchent l'accroche du courriel.

    python recolte.py --url plomberielalonde.com --out prospect.json
    python recolte.py --url x.ca --nom "Plomberie Lalonde" --tel "819-663-6330"

Sortie: un JSON. Aucun jugement, que des mesures. Ce qui n'a pas ete trouve vaut null
et le champ "manques" le nomme, pour que la sonde puisse refuser le prospect au lieu
d'envoyer une image trouee.
"""
import argparse
import base64
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import warnings
from collections import Counter

warnings.filterwarnings("ignore", category=DeprecationWarning)
from html import unescape
from urllib.parse import urljoin, urlparse

from PIL import Image, ImageChops

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

ICONE = re.compile(r"(icon|favicon|sprite|arrow|fleche|clock|award|feedback|star|"
                   r"badge|placeholder|spinner|loader|pixel|blank|spacer)", re.I)
LOGO = re.compile(r"logo|wordmark|brand", re.I)


# ---------------------------------------------------------------- reseau

def fetch(url, binaire=False, timeout=25):
    """curl, parce qu'il traverse ce que urllib refuse (TLS ancien, redirections)."""
    cmd = ["curl", "-sL", "--max-time", str(timeout), "-A", UA,
           "-w", "\n@@HTTP@@%{http_code}@@%{url_effective}@@", url]
    r = subprocess.run(cmd, capture_output=True)
    brut = r.stdout
    m = re.search(rb"\n@@HTTP@@(\d+)@@(.*?)@@$", brut, re.S)
    code, final = 0, url
    if m:
        code = int(m.group(1))
        final = m.group(2).decode("utf-8", "replace")
        brut = brut[:m.start()]
    if binaire:
        return brut, code, final
    return decode(brut), code, final


def decode(octets):
    """Le charset annonce d'abord. Les sites WordPress anciens sont souvent en 1252."""
    tete = octets[:3000].decode("ascii", "replace")
    m = re.search(r'charset=["\']?([\w-]+)', tete, re.I)
    ordre = [m.group(1)] if m else []
    ordre += ["utf-8", "cp1252", "latin-1"]
    for enc in ordre:
        try:
            return octets.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return octets.decode("utf-8", "replace")


# ---------------------------------------------------------------- texte

def sans_balises(html):
    t = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", html)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = unescape(t)
    return re.sub(r"[ \t\xa0]+", " ", t)


def lignes_utiles(texte, mini=3):
    vues, out = set(), []
    for l in texte.splitlines():
        l = l.strip()
        if len(l) >= mini and l.lower() not in vues:
            vues.add(l.lower())
            out.append(l)
    return out


# ---------------------------------------------------------------- identite

def telephones(html):
    tels = re.findall(r'href=["\']tel:([^"\']+)["\']', html, re.I)
    tels += re.findall(r"\b(?:\+?1[\s.-]?)?\(?([2-9]\d{2})\)?[\s.-]?(\d{3})[\s.-]?(\d{4})\b",
                       sans_balises(html))
    norm = []
    for t in tels:
        chiffres = re.sub(r"\D", "", "".join(t) if isinstance(t, tuple) else t)
        if len(chiffres) == 11 and chiffres[0] == "1":
            chiffres = chiffres[1:]
        if len(chiffres) == 10:
            norm.append("%s-%s-%s" % (chiffres[:3], chiffres[3:6], chiffres[6:]))
    return [t for t, _ in Counter(norm).most_common()]


def courriels(html, hote):
    out = re.findall(r'mailto:([^"\'?>\s]+@[^"\'?>\s]+)', html, re.I)
    out += re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", sans_balises(html))
    # WordPress masque souvent: dEmail('service','domaine.com','','')
    for u, d in re.findall(r"""[dD]Email\(\s*['"]([^'"]+)['"]\s*,\s*['"]([^'"]+)['"]""", html):
        out.append("%s@%s" % (u, d))
    vus, prop = set(), []
    for e in out:
        e = e.strip().lower().rstrip(".,;")
        if e in vus or e.endswith((".png", ".jpg", ".gif", ".webp")):
            continue
        vus.add(e)
        prop.append(e)
    prop.sort(key=lambda e: (hote not in e.split("@")[-1], len(e)))
    return prop


ARRET = re.compile(r"\b(courriel|t[eé]l[eé]phone|t[eé]l|email|fax|heures|hours|ouvert|"
                   r"open|lundi|monday|canada|qu[eé]bec|ontario)\b|[A-Z]\d[A-Z]\s?\d[A-Z]\d",
                   re.I)


def adresse(texte):
    """Numero + type de voie + trois mots au plus. Sans borne, la capture avale le code
    postal et les libelles suivants: vu sur Lalonde, ou elle rendait
    '1680 Rue Routhier Gatineau J8R 3Y7 Courriel Teleph'."""
    m = re.search(r"\b(\d{2,5})\s+((?:rue|boul(?:evard)?|av(?:enue)?|ch(?:emin)?|"
                  r"route|street|st\.|ave?\.|road|rd\.|drive|dr\.|way|place|prom(?:enade)?)"
                  r"[^,\n]{2,60})", texte, re.I)
    if not m:
        return None
    voie = m.group(2)
    coupe = ARRET.search(voie)
    if coupe:
        voie = voie[:coupe.start()]
    mots = voie.split()
    if len(mots) < 2:
        return None
    return ("%s %s" % (m.group(1), " ".join(mots[:4]))).strip(" .,-")


def langue(html, final):
    m = re.search(r'<html[^>]+lang=["\']([a-zA-Z-]+)', html)
    principale = (m.group(1)[:2].lower() if m else None)
    if not principale:
        principale = "fr" if re.search(r"/fr(/|$)", final) else "en"
    autre = bool(re.search(r'href=["\'][^"\']*/(en|fr)(/|["\'])', html, re.I)) or \
        bool(re.search(r">\s*(English|Fran[cç]ais)\s*<", html, re.I))
    return principale, autre


# ---------------------------------------------------------------- images

def images(html, base):
    srcs = re.findall(r'(?:src|data-src|href|content)=["\']([^"\']+\.(?:png|jpe?g|webp|svg))', html, re.I)
    srcs += [m for m in re.findall(r"url\(\s*['\"]?([^)'\"]+\.(?:png|jpe?g|webp))", html, re.I)]
    vus, out = set(), []
    for s in srcs:
        u = urljoin(base, unescape(s.strip()))
        if u not in vus:
            vus.add(u)
            out.append(u)
    return out


def dimensions(octets):
    try:
        im = Image.open(io.BytesIO(octets))
        return im.size, im
    except Exception:
        return None, None


def couleurs(im, pas=12):
    """Dominantes du logo, plus l'accent: la plus saturee qui n'est ni fond ni encre."""
    im = im.convert("RGBA")
    if max(im.size) > 400:
        im.thumbnail((400, 400))
    px = [p for p in im.getdata() if p[3] > 150]
    if not px:
        return [], None, False
    c = Counter((r // pas * pas, g // pas * pas, b // pas * pas) for r, g, b, a in px)
    dom = [("#%02x%02x%02x" % k, round(100.0 * v / len(px))) for k, v in c.most_common(8)]

    def sat(h):
        r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
        mx, mn = max(r, g, b), min(r, g, b)
        return 0 if mx == 0 else (mx - mn) / float(mx), mx
    accent = None
    for h, part in dom:
        s, v = sat(h)
        if s > .35 and v > 40 and part >= 3:
            accent = h
            break
    # Un logo dessine en clair pour fond sombre disparait sur une barre claire.
    # Vu sur Alictro: texte blanc, seul le E vert restait visible.
    clair = sum(.299 * r + .587 * g + .114 * b for r, g, b, a in px) / len(px) > 165
    return dom, accent, clair


def rogne_et_reduit(octets, im, url, cote=640):
    """Deux corrections mesurees sur Alictro, dont le fichier fait 4500x3872.

    1. Le vide autour du logo est rogne. Un logo pose au centre d'une grande toile
       transparente s'affiche minuscule dans une barre de 34px: c'est la toile qui
       occupe la hauteur, pas le dessin.
    2. Ce qui reste est ramene a 640px. Un fichier de 4500px pese vingt fois trop.

    Rend (octets, largeur, hauteur) du dessin reel, pas du fichier d'origine.
    """
    if url.lower().endswith(".svg"):
        return octets, im.size[0], im.size[1]
    try:
        im2 = im.convert("RGBA")
        fond = im2.split()[3]
        if fond.getextrema()[0] == 255:          # opaque partout: bordure unie
            gris = im2.convert("L")
            coin = Image.new("L", im2.size, gris.getpixel((0, 0)))
            boite = ImageChops.difference(gris, coin).point(lambda v: 255 if v > 14 else 0).getbbox()
        else:
            boite = fond.getbbox()
        if boite:
            larg, haut = boite[2] - boite[0], boite[3] - boite[1]
            if larg > 8 and haut > 8 and larg * haut < im2.size[0] * im2.size[1] * .98:
                im2 = im2.crop(boite)
        if max(im2.size) > cote:
            im2.thumbnail((cote, cote))
        buf = io.BytesIO()
        im2.save(buf, "PNG", optimize=True)
        return buf.getvalue(), im2.size[0], im2.size[1]
    except Exception:
        return octets, im.size[0], im.size[1]


def analyse_images(urls, base_hote):
    logo, photos, echecs = None, [], 0
    cands = [u for u in urls if not ICONE.search(u)]
    tries = sorted(cands, key=lambda u: (not LOGO.search(u), len(u)))
    for u in tries[:14]:
        octets, code, _ = fetch(u, binaire=True, timeout=15)
        if code != 200 or len(octets) < 400:
            echecs += 1
            continue
        taille, im = dimensions(octets)
        if not taille:
            continue
        w, h = taille
        est_logo = bool(LOGO.search(u)) or (w <= 520 and h <= 260 and w / float(h or 1) > 1.4)
        if est_logo and logo is None and im is not None:
            dom, accent, clair = couleurs(im)
            octets, lw, lh = rogne_et_reduit(octets, im, u)
            logo = {"url": u, "w_fichier": w, "h_fichier": h, "w": lw, "h": lh,
                    "rogne": (lw, lh) != (w, h),
                    "rapport": round(lw / float(lh or 1), 2),
                    "empile": (lw / float(lh or 1)) < 1.5,
                    "dominantes": dom, "accent": accent, "clair": clair,
                    "b64": base64.b64encode(octets).decode("ascii") if len(octets) < 400000 else None}
        elif w >= 700 and h >= 400:
            photos.append({"url": u, "w": w, "h": h, "ratio": round(w / float(h), 2),
                           "paysage": w > h, "assez_grande_pour_heros": w >= 1600})
    photos.sort(key=lambda p: -(p["w"] * p["h"]))
    return logo, photos, echecs


# ---------------------------------------------------------------- signaux

def signaux(html, final, tels, photos, principale, bilingue, texte):
    s = {}
    s["pas_https"] = not final.lower().startswith("https")
    s["pas_viewport"] = not re.search(r'<meta[^>]+name=["\']viewport', html, re.I)
    s["tel_pas_cliquable"] = (not re.search(r'href=["\']tel:', html, re.I)) and bool(tels)
    s["aucune_photo_a_eux"] = len(photos) == 0
    s["pas_bilingue"] = not bilingue
    s["pas_de_lien_avis"] = not re.search(r"(google\.com/maps|g\.page|goo\.gl/maps|search\?.*lrd=)",
                                          html, re.I)
    an = [int(a) for a in re.findall(r"(?:©|&copy;|copyright)[^0-9]{0,18}(20[0-2]\d)", html, re.I)]
    s["annee_copyright"] = max(an) if an else None
    s["pas_de_formulaire"] = not re.search(r"<form", html, re.I)
    s["poids_html_ko"] = round(len(html.encode("utf-8", "replace")) / 1024.0)
    s["mots"] = len(texte.split())
    return s


ACCROCHES = [
    ("aucune_photo_a_eux", True,
     "Il n'y a pas une seule photo de vos realisations sur votre site.",
     "There is not a single photo of your own work on your site."),
    ("pas_viewport", True,
     "Sur un telephone, votre site oblige a zoomer pour vous lire.",
     "On a phone, your site forces the reader to zoom in."),
    ("pas_https", True,
     "Les navigateurs affichent Non securise juste devant le nom de votre entreprise.",
     "Browsers now show Not secure right in front of your business name."),
    ("tel_pas_cliquable", True,
     "Sur un telephone, votre numero ne se compose pas d'un doigt, il faut le recopier.",
     "On a phone, your number cannot be tapped to call, it has to be copied out."),
    ("pas_bilingue", True,
     "Votre site n'existe que dans une langue, dans une region ou la moitie des clients cherche dans l'autre.",
     "Your site exists in one language only, in a region where half the customers search in the other."),
    ("pas_de_lien_avis", True,
     "Vos avis Google ne sont nulle part sur votre site.",
     "Your Google reviews appear nowhere on your own site."),
    ("pas_de_formulaire", True,
     "Il n'y a aucun formulaire: tout passe par un appel, sinon le client s'en va.",
     "There is no form anywhere: it is a phone call or nothing."),
]


def accroche(sig):
    for cle, attendu, fr, en in ACCROCHES:
        if sig.get(cle) == attendu:
            return {"signal": cle, "fr": fr, "en": en}
    an = sig.get("annee_copyright")
    if an and an <= 2023:
        return {"signal": "annee_copyright",
                "fr": "Le pied de page de votre site s'arrete a %d." % an,
                "en": "The footer of your site still reads %d." % an}
    return None


GENERIQUE = re.compile(r"^(home|accueil|welcome|bienvenue|index|site officiel|"
                       r"official site|page d'accueil)$", re.I)


def nom_propre(titre):
    """Le nom d'entreprise dans un <title>. Il est presque toujours en dernier."""
    parts = [p.strip(" 	–—-") for p in re.split(r"[|–—·]|\s-\s", titre)]
    parts = [p for p in parts if p and not GENERIQUE.match(p)]
    if not parts:
        return titre.strip() or None
    return parts[-1]


# ---------------------------------------------------------------- principal

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--nom")
    p.add_argument("--tel")
    p.add_argument("--out")
    a = p.parse_args()

    url = a.url if "://" in a.url else "https://" + a.url
    html, code, final = fetch(url)
    if code != 200 or len(html) < 500:
        print(json.dumps({"erreur": "fetch", "code": code, "url": url}, ensure_ascii=False))
        return 2

    hote = urlparse(final).netloc.replace("www.", "")
    texte = sans_balises(html)
    lignes = lignes_utiles(texte)
    tels = telephones(html)
    principale, bilingue = langue(html, final)
    logo, photos, echecs = analyse_images(images(html, final), hote)
    sig = signaux(html, final, tels, photos, principale, bilingue, texte)

    titre = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
    desc = re.search(r'(?is)<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html)

    d = {
        "url": final,
        "hote": hote,
        "nom": a.nom or nom_propre(unescape(titre.group(1))) if titre else a.nom,
        "titre_page": unescape(titre.group(1)).strip() if titre else None,
        "description": unescape(desc.group(1)).strip() if desc else None,
        "telephones": tels,
        "telephone": a.tel or (tels[0] if tels else None),
        "courriels": courriels(html, hote),
        "adresse": adresse(texte),
        "langue_principale": principale,
        "bilingue": bilingue,
        "logo": logo,
        "photos": photos[:8],
        "nb_photos": len(photos),
        "signaux": sig,
        "accroche": accroche(sig),
        "extraits": lignes[:60],
        "images_illisibles": echecs,
    }

    manques = [c for c in ("nom", "telephone", "logo") if not d.get(c)]
    if not d["courriels"]:
        manques.append("courriel")
    if logo and not logo.get("accent"):
        manques.append("accent_couleur")
    d["manques"] = manques
    d["utilisable"] = not [m for m in manques if m in ("nom", "telephone", "logo")]

    sortie = json.dumps(d, ensure_ascii=False, indent=1)
    if a.out:
        with io.open(a.out, "w", encoding="utf-8") as f:
            f.write(sortie)
        acc = d["accroche"]["signal"] if d["accroche"] else "AUCUNE"
        print("%-26s tel=%s  photos=%d  logo=%s  accent=%s" % (
            d["nom"] or "?", d["telephone"], d["nb_photos"],
            "oui" if logo else "NON", (logo or {}).get("accent") or "-"))
        print("  accroche=%s  manques=%s  utilisable=%s" % (
            acc, ",".join(manques) or "-", d["utilisable"]))
    else:
        print(sortie)
    return 0


if __name__ == "__main__":
    sys.exit(main())
