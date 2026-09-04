# -*- coding: utf-8 -*-
"""
Index du coffre. Entretien du Plan Jarvis, point 4.

Deterministe, aucun appel a un modele. Il liste toutes les notes du coffre
avec leur premiere ligne de contenu, et le bibliothecaire lit ce fichier au
lieu de fouiller le coffre a coups de recherches.

Pourquoi il existe : mesure le 3 septembre 2026, le bibliothecaire faisait
40 tours d'outils pour deux ou trois captures et 71 sur un gros lot, dont
une grande partie de recherches pour savoir si une note existe deja. Plus
de neuf dixiemes de ses tokens etaient de la relecture de contexte, parce
que chaque tour relit tout ce qui precede. L'index repond a cette question
en une lecture, et il se calcule en une seconde sans depenser un token.

Il ne modifie ni ne supprime aucune note. Il ne fait que lire.

Sortie, une ligne par note, triee par chemin :
    chemin relatif | premiere ligne de contenu, 90 caracteres au plus

L'en-tete YAML, les titres et les citations ne comptent pas comme premiere
ligne. Ce qu'on veut, c'est la phrase qui dit de quoi parle la note.

99 Archives est inclus volontairement : le bibliothecaire en a besoin pour
reperer une collision de nom au moment d'archiver une capture.

Le fichier est ecrit en UTF-8 sans BOM. Les noms de notes ont des accents,
et Set-Content -Encoding utf8 de PowerShell 5.1 ajouterait un BOM que le
modele lirait comme un caractere de plus.

Usage :
    python index.py <coffre> <fichier de sortie>
"""

import os
import sys

IGNORES = {".obsidian", ".git", "_Modeles", "_Modèles"}
LARGEUR = 90


def premiere_ligne(chemin):
    """La premiere ligne qui dit quelque chose, hors YAML, titres et citations."""
    try:
        with open(chemin, encoding="utf-8-sig", errors="replace") as fh:
            lignes = fh.read().split("\n")
    except Exception:
        return ""

    i = 0
    # L'en-tete YAML, seulement s'il ouvre le fichier.
    if lignes and lignes[0].strip() == "---":
        i = 1
        while i < len(lignes) and lignes[i].strip() != "---":
            i += 1
        i += 1

    for ligne in lignes[i:]:
        t = ligne.strip()
        if not t:
            continue
        if t.startswith("#"):          # titre
            continue
        if t.startswith(">"):          # citation, callout
            continue
        if set(t) <= set("-*_ "):      # separateur horizontal
            continue
        t = " ".join(t.split())        # ecraser les espaces multiples
        if len(t) > LARGEUR:
            t = t[:LARGEUR - 1].rstrip() + "\u2026"
        return t
    return ""


def main():
    if len(sys.argv) < 3:
        print("usage: index.py <coffre> <sortie>")
        return 2
    coffre = sys.argv[1]
    sortie = sys.argv[2]

    if not os.path.isdir(coffre):
        print("ECHEC: coffre introuvable, " + coffre)
        return 1

    lignes = []
    for racine, dossiers, fichiers in os.walk(coffre):
        dossiers[:] = [d for d in dossiers if d not in IGNORES]
        for f in fichiers:
            if not f.endswith(".md"):
                continue
            complet = os.path.join(racine, f)
            rel = os.path.relpath(complet, coffre).replace(os.sep, "/")
            lignes.append((rel, premiere_ligne(complet)))

    lignes.sort(key=lambda x: x[0])

    with open(sortie, "w", encoding="utf-8", newline="\n") as fh:
        for rel, tete in lignes:
            fh.write(rel + " | " + tete + "\n")

    print("lignes=%d" % len(lignes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
