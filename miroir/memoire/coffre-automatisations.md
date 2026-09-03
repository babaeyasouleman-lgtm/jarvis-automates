---
name: coffre-automatisations
description: "Les tâches Windows qui entretiennent le coffre Obsidian et sauvegardent les automates, les modèles qu'elles utilisent, et les pièges Windows qui les font échouer en silence."
metadata:
  node_type: memory
  type: project
  originSessionId: c9bcd99a-89d8-4a22-acae-a16e2f7c91d9
  modified: 2026-09-03T19:24:54.353Z
---

Trois tâches Windows tournent sur le PC de Souleman. Ne pas les reconstruire, elles existent. Le plan complet est `C:\Obsidian\Second Brain\02 Projets\Plan Jarvis.md`, restructuré par paliers le 2026-09-03.

**Filet, phase 1 du [[Plan Jarvis]].** `C:\Obsidian\filet\commit-horaire.ps1`, tâche « Filet coffre Obsidian », toutes les heures. Commit et pousse le coffre vers le dépôt privé `babaeyasouleman-lgtm/second-brain`.

**Bibliothécaire et extracteur, phases 2 et 2 bis.** Une seule tâche, « Bibliothecaire du coffre », déclenchée à 3 h avec réessai toutes les 30 minutes, rattrapage au démarrage puisque le PC est éteint la nuit. `passage.ps1` appelle d'abord `C:\Obsidian\transcriptions\extraction.ps1`, qui lit les sessions Claude Code depuis un marqueur et dépose dans `00 Inbox`, puis range. Si Obsidian est ouvert, le rangement attend, et après six refus il range quand même. Le comportement de chacun se change dans son `consigne.md`, jamais dans le script. Journal hebdomadaire partagé dans `_Bibliothécaire/AAAA-Sxx.md`.

**Modèles.** Bibliothécaire sur `opus`. Extracteur sur `sonnet` depuis le 2026-09-03, décision prise à l'audit après mesure : une nuit valait 2 à 4 $ d'équivalent Opus pour un travail qui ne demande pas de connaître le coffre. Version d'avant gardée en `extraction.ps1.avant-sonnet`. Le 2026-09-03 à 0 h 03, l'extracteur a été refusé pour limite de session pendant que Souleman travaillait : les automates et lui partagent le même quota.

**Filet des automates, ajouté le 2026-09-03.** `C:\Obsidian\filet\commit-automates.ps1`, tâche « Filet automates », toutes les heures. Dépôt git à la racine `C:\Obsidian`, qui suit `bibliothecaire`, `transcriptions`, `filet`, et un dossier `miroir` copié par robocopy depuis les skills maison, `agent-vocal`, `devis`, `prospect-site`, `prospect-email`, `no-ai-slop`, les tâches planifiées de l'app et ce dossier de mémoire. `Second Brain/`, `node_modules`, journaux, `travail` et fichiers `*.local.*` sont exclus. Remote `babaeyasouleman-lgtm/jarvis-automates`, à créer sur GitHub par Souleman : tant qu'il n'existe pas, la poussée échoue et se retente à l'heure suivante. `gh` n'est pas installé sur ce PC, le push passe par Git Credential Manager en HTTPS.

**Ce qui n'a jamais tourné.** `note-du-matin` et `lot-prospection-courriel` sont enregistrés dans les tâches planifiées de l'app Claude, désactivés, à heure fixe. Le PC est éteint à ces heures et l'app ne rattrape pas. Ils doivent passer par une tâche Windows ou par `passage.ps1`. C'est la phase 3 du plan pour la note du matin.

**Pièges Windows, découverts en testant, coûteux à redécouvrir.**

1. Une tâche planifiée ne démarre pas sur batterie sans `-AllowStartIfOnBatteries -DontStopIfGoingOnBatteries`.
2. Une longue consigne passée en argument à `claude -p` est tronquée dès qu'elle contient des guillemets. La consigne vit dans un `.md` que Claude lit lui-même, la ligne de commande reste courte et sans accent. Aucun accent dans les `.ps1`, PowerShell 5.1 les lit en ANSI.
3. `Set-Content -Encoding utf8` en PowerShell 5.1 ajoute un BOM que Python lit comme un caractère. Les marqueurs et compteurs s'écrivent en ascii.

**Pourquoi les automates restent sur le PC.** Git et Obsidian Sync ne se croisent que sur le PC. Le déménagement sur un serveur est la phase 9 du plan, premier pas du palier 2, quand des employés ne pourront plus dépendre du PC.

Voir [[second-brain-obsidian]] pour la structure du coffre.
