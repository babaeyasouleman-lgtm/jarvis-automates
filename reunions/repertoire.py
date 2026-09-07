# -*- coding: utf-8 -*-
"""
Qui compte, lu dans le coffre. Phase 4 bis du Plan Jarvis.

Deterministe, aucun appel a un modele, zero token depense. Il liste les
personnes de 06 Personnes, les clients de Pipeline clients S-WEB, et les
adresses courriel trouvees dans ces notes, puis ecrit repertoire.txt.

Meme role que index.py pour le bibliothecaire : repondre sans reseau a la
question qui couterait des tours d'outils. Ici, celle-ci : est-ce que ce
participant existe dans le coffre ?

Le collecteur des reunions passe par le connecteur Fathom, donc c'est le
modele qui appelle l'outil. Tout ce qui peut se calculer avant se calcule
ici. C'est la part deterministe de cette phase.

Il ne modifie rien dans le coffre. Il ne lit que.

Usage :
    python repertoire.py <coffre> <sortie.txt>
"""

import glob
import os
import re
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 3:
        print("usage: repertoire.py <coffre> <sortie.txt>")
        return 2
    coffre = sys.argv[1]
    sortie = sys.argv[2]

    personnes = []
    clients = []
    adresses = set()

    for chemin in sorted(glob.glob(os.path.join(coffre, "06 Personnes", "*.md"))):
        nom = os.path.basename(chemin)[:-3]
        try:
            with open(chemin, encoding="utf-8", errors="replace") as f:
                txt = f.read()
        except Exception:
            txt = ""
        alias = []
        for a in re.findall(r"^aliases?:\s*(.+)$", txt, re.M | re.I):
            alias += [x.strip(" []\"'") for x in a.split(",") if x.strip(" []\"'")]
        for m in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", txt):
            adresses.add(m.lower())
        ligne = nom
        if alias:
            ligne += " (aussi " + ", ".join(alias) + ")"
        personnes.append(ligne)

    pipeline = os.path.join(coffre, "03 Domaines", "S-WEB", "Pipeline clients S-WEB.md")
    if os.path.exists(pipeline):
        with open(pipeline, encoding="utf-8", errors="replace") as f:
            contenu = f.read()
        for ligne in contenu.split("\n"):
            if not ligne.startswith("|"):
                continue
            cols = [c.strip() for c in ligne.strip().strip("|").split("|")]
            if len(cols) < 2 or not re.match(r"^\d{4}-\d{3}$", cols[0]):
                continue
            if cols[1] and cols[1] not in clients:
                clients.append(cols[1])
        for m in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", contenu):
            adresses.add(m.lower())

    lignes = ["personnes=%d" % len(personnes),
              "clients=%d" % len(clients),
              "adresses=%d" % len(adresses),
              ""]
    lignes += ["personne: " + p for p in personnes]
    lignes += ["client: " + c for c in clients]
    lignes += ["adresse: " + a for a in sorted(adresses)]

    with open(sortie, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lignes) + "\n")
    print("personnes=%d clients=%d adresses=%d" % (len(personnes), len(clients), len(adresses)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
