---
name: coffre-automatisations
description: "Les tâches planifiées qui entretiennent le coffre Obsidian, et les deux pièges Windows qui les font échouer silencieusement."
metadata: 
  node_type: memory
  type: project
  originSessionId: c9bcd99a-89d8-4a22-acae-a16e2f7c91d9
  modified: 2026-08-28T23:18:54.807Z
---

Deux tâches Windows entretiennent `C:\Obsidian\Second Brain`. Ne pas les reconstruire, elles existent.

**Filet, phase 1 du [[Plan Jarvis]].** `C:\Obsidian\filet\commit-horaire.ps1`, tâche « Filet coffre Obsidian », toutes les heures. Commit et pousse vers le dépôt privé `babaeyasouleman-lgtm/second-brain`.

**Bibliothécaire, phase 2, en place le 2026-08-28.** `C:\Obsidian\bibliothecaire\`, tâche « Bibliothecaire du coffre », tous les jours à 3 h avec rattrapage au démarrage puisque le PC de Souleman est éteint la nuit. Il vide `00 Inbox`, met les notes à jour sans empiler d'historique, déplace les captures vers `99 Archives/Inbox rangé`, et écrit un journal hebdomadaire dans `_Bibliothécaire/AAAA-Sxx.md`. Son comportement se change dans `consigne.md`, jamais dans le script.

**Deux pièges Windows, découverts en testant, coûteux à redécouvrir.**

1. Une tâche planifiée ne démarre pas quand le portable est sur batterie. `DisallowStartIfOnBatteries` est vrai par défaut. Il faut `-AllowStartIfOnBatteries -DontStopIfGoingOnBatteries`.
2. Une longue consigne passée en argument à `claude -p` est tronquée par Windows dès qu'elle contient des guillemets. La consigne doit vivre dans un fichier `.md` que Claude lit lui-même, et la ligne de commande reste courte et sans accent. Pour la même raison, aucun accent dans les `.ps1` : PowerShell 5.1 les lit en ANSI.

**Pourquoi le bibliothécaire reste sur le PC et pas sur Railway.** Git et Obsidian Sync sont deux tuyaux qui ne se croisent que sur le PC. Un bibliothécaire sur Railway rangerait dans GitHub, et l'iPhone ne verrait rien avant le prochain allumage du PC. Le déménagement devient utile à la phase 4, quand l'agent WhatsApp lira le cerveau depuis git.

Voir [[second-brain-obsidian]] pour la structure du coffre.
