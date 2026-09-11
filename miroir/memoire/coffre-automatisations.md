---
name: coffre-automatisations
description: "Ou vit la verite sur les automates du coffre Obsidian, et ce qui n'est ecrit qu'ici : les cinq pieges Windows qui font echouer un automate en silence, la ligne mesure de passage.ps1, et pourquoi les automates restent sur le PC."
metadata: 
  node_type: memory
  type: project
  originSessionId: eee27d88-f723-4809-8264-1500fd32fce5
  modified: 2026-09-11T03:43:42.668Z
---

Reduit le 10 septembre 2026 de 27 Ko a ceci. L'ancienne version est dans le git de `C:\Obsidian`, sous `miroir\memoire\`, et dans `memory-avant-2026-09-10\` a cote de ce dossier. Tout ce qu'elle racontait vit dans le plan, dans les consigne.md ou dans les en-tetes des .ps1.

**Ou aller.** `C:\Obsidian\ENTREE.md` donne la carte : un dossier par automate sous `C:\Obsidian`, chacun avec consigne.md, un .ps1 et journal.log. Quatre taches Windows : Filet coffre Obsidian, Filet automates, Bibliothecaire du coffre, Preneur de billets. Le comportement vit dans la consigne, la mecanique dans le .ps1, et l'en-tete de chaque .ps1 dit pourquoi il est fait ainsi.

**Les cinq pieges Windows, ecrits nulle part ailleurs.**
1. Une tache planifiee ne demarre pas sur batterie sans `-AllowStartIfOnBatteries -DontStopIfGoingOnBatteries`.
2. Une longue consigne passee en argument a `claude -p` est tronquee des qu'elle contient des guillemets. La consigne vit dans un .md que Claude lit lui-meme. Aucun accent dans un .ps1, PowerShell 5.1 lit en ANSI.
3. `Set-Content -Encoding utf8` en PowerShell 5.1 ajoute un BOM que Python lit comme un caractere. Les marqueurs et compteurs s'ecrivent en ascii.
4. `Compare-Object` refuse un tableau vide. Pour comparer deux `git status --porcelain`, passer par `Where-Object { $avant -notcontains $_ }`.
5. Une consigne qui nomme `journal.log` invite le modele a y ecrire lui-meme. Dire noir sur blanc que le resume va dans la reponse et que le lanceur seul ecrit le journal.

**Mesurer un passage.** `passage.ps1` appelle `claude -p --output-format json` et ecrit une ligne `mesure` dans son journal : tours, tokens, equivalent en dollars. Repere : 24 tours et 197 s pour une nuit ordinaire depuis l'index, 71 tours sur un gros lot avant. La meme ligne manque a `matin.ps1` et `extraction.ps1`.

**Pourquoi les automates restent sur le PC.** Git et Obsidian Sync ne se croisent que la. Le demenagement est la phase 9, premier pas du palier 2.

**Why:** quatre sessions ont lu ce fichier, jusqu'a 27 Ko d'un coup, pour des faits deja dans les .ps1 et le plan.
**How to apply:** lire ENTREE.md, puis la consigne et l'en-tete du seul automate touche. Voir [[agent-whatsapp-modules]], [[second-brain-obsidian]] et [[jarvis-cout-des-sessions]].
