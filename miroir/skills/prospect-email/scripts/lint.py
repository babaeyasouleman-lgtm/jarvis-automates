#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lint.py  ---  les bogues qui ne produisent AUCUNE erreur, seulement un rendu faux.

    python scripts/lint.py "Prospect/teaser/index.html"

Complement de detect.sh, pas un remplacement. detect.sh juge le GOUT (contraste,
tics de gabarit, texte minuscule). lint.py juge la MECANIQUE: une classe qui en
ecrase une autre, une regle CSS absente, un fichier qui n'existe pas.

Ces cinq controles viennent tous d'un bogue reel deja paye, chacun trouve au
rendu apres une capture perdue. A lancer AVANT detect.sh: il coute 0,2 seconde et
il evite un cycle capture-regard complet.

Code de sortie 1 s'il reste une trouvaille GRAVE.
"""
import os
import re
import sys

GRAVE, AVIS = "GRAVE", "avis"

# Proprietes qui deplacent ou dimensionnent. Une collision sur celles-la se voit,
# une collision sur une couleur passe souvent inapercue.
GEO = ("margin", "padding", "display", "position", "width", "height",
       "top", "right", "bottom", "left", "flex", "grid", "gap")


def styles(html):
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))


def regles(css):
    """[(selecteur, corps)] en sautant les at-rules et leur en-tete."""
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    out = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sel = " ".join(m.group(1).split())
        if sel.startswith("@") or not sel:
            continue
        out.append((sel, m.group(2)))
    return out


def classes_html(html):
    """{classe: nombre d'elements qui la portent}"""
    n = {}
    for attr in re.findall(r'class="([^"]*)"', html):
        for c in attr.split():
            n[c] = n.get(c, 0) + 1
    return n


def controles(chemin):
    html = open(chemin, encoding="utf-8").read()
    css = styles(html)
    rs = regles(css)
    porte = classes_html(html)
    trouvailles = []

    # ---- 1. COLLISION DE NOM DE CLASSE ------------------------------------
    # Le bogue Qualite d'air: .act{margin-top:28px} pour le bouton du heros
    # ecrasait aussi .lang span.act, la bascule FR, qui sortait a 4px de haut.
    #
    # La regle doit distinguer la collision du CSS parent-enfant ORDINAIRE.
    # .nav{...} plus .nav .in{...} est sain: .nav y est l'ANCETRE.
    # .act{...} plus .lang span.act{...} est la collision: .act est le SUJET
    # des deux, une fois seul et une fois qualifie par un ancetre etranger.
    # Premiere version sans cette distinction: 11 faux positifs pour 1 vrai.
    nue, sujet_qualifie = {}, {}
    for sel, corps in rs:
        for morceau in sel.split(","):
            morceau = morceau.strip()
            if not morceau:
                continue
            parts = re.split(r"\s*[ >+~]\s*", morceau)
            dernier = parts[-1]                      # le sujet du selecteur
            for c in re.findall(r"\.([A-Za-z_][\w-]*)", dernier):
                if len(parts) == 1 and re.fullmatch(r"\.%s(:[\w-]+)?" % re.escape(c), morceau):
                    nue.setdefault(c, []).append(corps)
                elif len(parts) > 1:                 # sujet, mais sous un ancetre
                    sujet_qualifie.setdefault(c, []).append(morceau)
    for c in sorted(set(nue) & set(sujet_qualifie)):
        if any(p in " ".join(nue[c]) for p in GEO):
            trouvailles.append((GRAVE, "collision-de-classe",
                ".%s a une regle nue qui pose de la geometrie ET sert de sujet dans %s. "
                "La regle nue s'applique aux deux, en silence."
                % (c, ", ".join(sorted(set(sujet_qualifie[c]))[:3]))))

    # ---- 2. CLASSE PORTEE MAIS JAMAIS STYLEE ------------------------------
    # Le bogue .nbr: la classe existait dans le HTML, sa regle CSS avait ete
    # oubliee en reportant la feuille. Aucune erreur, telephone coupe en deux.
    # Ici on veut TOUTE classe citee quelque part dans un selecteur, ancetres
    # compris, pas seulement les sujets du controle 1.
    stylees = set()
    for sel, _ in rs:
        stylees.update(re.findall(r"\.([A-Za-z_][\w-]*)", sel))
    for c in sorted(porte):
        if c not in stylees:
            trouvailles.append((GRAVE, "classe-sans-regle",
                ".%s est portee par %d element(s) et n'a aucune regle CSS."
                % (c, porte[c])))

    # ---- 3. REGLE ECRITE POUR RIEN ----------------------------------------
    for c in sorted(stylees - set(porte)):
        trouvailles.append((AVIS, "regle-orpheline",
            ".%s est stylee et aucun element ne la porte. Renommage a moitie fait?" % c))

    # ---- 4. FICHIER REFERENCE MAIS ABSENT ---------------------------------
    # Une image cassee dans l'image du courriel, c'est le courriel mort.
    base = os.path.dirname(os.path.abspath(chemin))
    refs = re.findall(r'(?:src|href)="([^"]+)"', html)
    refs += re.findall(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", css)
    for r in refs:
        if r.startswith(("http:", "https:", "data:", "#", "tel:", "mailto:")):
            continue
        if not os.path.exists(os.path.join(base, r.split("?")[0])):
            trouvailles.append((GRAVE, "fichier-absent", "%s n'existe pas sur le disque." % r))

    # ---- 5. COLONNE 1fr SANS minmax(0,...) --------------------------------
    # Piege mesure le 2026-08-19: une colonne en 1fr ne descend jamais sous la
    # largeur min-content de son contenu, le texte deborde et overflow-x le coupe.
    # Chaque colonne se juge SEULE. Premiere version fausse: elle sautait toute
    # la declaration des qu'une seule colonne portait minmax, donc
    # "1fr minmax(0,530px)", exactement le cas a attraper, passait au travers.
    def colonnes(v):
        out, cour, prof = [], "", 0
        for ch in v.strip():
            if ch == "(":
                prof += 1
            elif ch == ")":
                prof -= 1
            if ch.isspace() and prof == 0:
                if cour:
                    out.append(cour)
                cour = ""
            else:
                cour += ch
        if cour:
            out.append(cour)
        return out

    for sel, corps in rs:
        for g in re.findall(r"grid-template-columns:([^;}]+)", corps):
            for col in colonnes(g):
                if re.fullmatch(r"[\d.]*fr", col):
                    trouvailles.append((GRAVE, "1fr-sans-minmax",
                        "%s a une colonne '%s' nue. Ecrire minmax(0,%s)."
                        % (sel.strip(), col, col)))
    return trouvailles


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python scripts/lint.py <fichier.html>")
    total_graves = 0
    for chemin in sys.argv[1:]:
        t = controles(chemin)
        print("\n%s" % os.path.abspath(chemin))
        if not t:
            print("  rien a signaler.")
            continue
        for niveau, code, texte in sorted(t, key=lambda x: x[0] != GRAVE):
            marque = "GRAVE" if niveau == GRAVE else "  .  "
            print("  [%s] %-20s %s" % (marque, code, texte))
        g = sum(1 for n, _, _ in t if n == GRAVE)
        total_graves += g
        print("  %d trouvaille(s), dont %d grave(s)." % (len(t), g))
    sys.exit(1 if total_graves else 0)


if __name__ == "__main__":
    main()
