---
name: coffre-automatisations
description: "Les tâches Windows qui entretiennent le coffre Obsidian et sauvegardent les automates, les trois automates que passage.ps1 enchaîne, les modèles qu'elles utilisent, et les pièges Windows qui les font échouer en silence."
metadata:
  node_type: memory
  type: project
  originSessionId: c9bcd99a-89d8-4a22-acae-a16e2f7c91d9
  modified: 2026-09-03T19:24:54.353Z
---

Trois tâches Windows tournent sur le PC de Souleman, et une seule d'entre elles enchaîne les trois automates du coffre. Ne pas les reconstruire, elles existent. Le plan complet est `C:\Obsidian\Second Brain\02 Projets\Plan Jarvis.md`, restructuré par paliers le 2026-09-03.

**Filet, phase 1 du [[Plan Jarvis]].** `C:\Obsidian\filet\commit-horaire.ps1`, tâche « Filet coffre Obsidian », toutes les heures. Commit et pousse le coffre vers le dépôt privé `babaeyasouleman-lgtm/second-brain`.

**L'enchaînement du passage, phases 3, 2 et 2 bis.** Une seule tâche, « Bibliothecaire du coffre », déclenchée à 3 h avec réessai toutes les 30 minutes, rattrapage au démarrage puisque le PC est éteint la nuit. `passage.ps1` enchaîne dans cet ordre : `C:\Obsidian\matin\matin.ps1`, puis `C:\Obsidian\transcriptions\extraction.ps1`, qui lit les sessions Claude Code depuis un marqueur et dépose dans `00 Inbox`, puis le rangement. Si Obsidian est ouvert, le rangement attend, et après six refus il range quand même. Le comportement de chacun se change dans son `consigne.md`, jamais dans le script. Journal hebdomadaire partagé dans `_Bibliothécaire/AAAA-Sxx.md`.

**Note du matin, en service depuis le 2026-09-03.** `C:\Obsidian\matin\`, avec `consigne.md`, `matin.ps1` et `journal.log`. Elle écrit `01 Journal/AAAA-MM-JJ.md` à partir du coffre : agenda, veille, décisions à revoir, relances dues, prochaine action de chaque projet actif, deux questions de `À confirmer`. Elle passe **en premier**, avant l'extraction et avant les deux gardes, parce qu'une note du matin qui attend trois heures qu'Obsidian se ferme n'est plus une note du matin. Marqueur `dernier-jour.txt` en ascii, un seul commit `Note du matin, <date>` qui ne contient que la note du jour, sans poussée. Si la note existe déjà avec du texte de Souleman, elle insère sa section après le titre H1 et ne réécrit rien.

**Les connecteurs de l'app Claude n'existent pas en mode `claude -p`.** Vérifié le 2026-09-03 : ni Google Agenda, ni Gmail. `claude mcp list` ne montre que les serveurs enregistrés dans le CLI. La note du matin écrit donc « Agenda indisponible ce matin » et continue. À vérifier avant d'écrire tout automate qui compte sur un connecteur, la phase 4 sur Gmail en dépend.

**Modèles.** Bibliothécaire sur `opus`. Note du matin sur `sonnet`, elle assemble et ne juge pas. Extracteur sur `sonnet` depuis le 2026-09-03, décision prise à l'audit après mesure : une nuit valait 2 à 4 $ d'équivalent Opus pour un travail qui ne demande pas de connaître le coffre. Version d'avant gardée en `extraction.ps1.avant-sonnet`. Le 2026-09-03 à 0 h 03, l'extracteur a été refusé pour limite de session pendant que Souleman travaillait : les automates et lui partagent le même quota.

**Filet des automates, ajouté le 2026-09-03.** `C:\Obsidian\filet\commit-automates.ps1`, tâche « Filet automates », toutes les heures. Dépôt git à la racine `C:\Obsidian`, qui suit `bibliothecaire`, `transcriptions`, `filet`, et un dossier `miroir` copié par robocopy depuis les skills maison, `agent-vocal`, `devis`, `prospect-site`, `prospect-email`, `no-ai-slop`, les tâches planifiées de l'app et ce dossier de mémoire. `Second Brain/`, `node_modules`, journaux, `travail` et fichiers `*.local.*` sont exclus. Remote `babaeyasouleman-lgtm/jarvis-automates`, à créer sur GitHub par Souleman : tant qu'il n'existe pas, la poussée échoue et se retente à l'heure suivante. `gh` n'est pas installé sur ce PC, le push passe par Git Credential Manager en HTTPS.

**Ce qui n'a jamais tourné.** `lot-prospection-courriel` reste enregistré dans les tâches planifiées de l'app Claude, désactivé, mardi et jeudi à 12 h 05. Le PC est éteint à cette heure et l'app ne rattrape pas. Il devra passer par une tâche Windows ou par `passage.ps1`, comme la note du matin. La tâche d'app `note-du-matin` a été supprimée le 2026-09-03 pour qu'il n'y ait qu'un seul déclencheur ; son `SKILL.md` reste sur le disque, c'est l'origine de la consigne.

**Pièges Windows, découverts en testant, coûteux à redécouvrir.**

1. Une tâche planifiée ne démarre pas sur batterie sans `-AllowStartIfOnBatteries -DontStopIfGoingOnBatteries`.
2. Une longue consigne passée en argument à `claude -p` est tronquée dès qu'elle contient des guillemets. La consigne vit dans un `.md` que Claude lit lui-même, la ligne de commande reste courte et sans accent. Aucun accent dans les `.ps1`, PowerShell 5.1 les lit en ANSI.
3. `Set-Content -Encoding utf8` en PowerShell 5.1 ajoute un BOM que Python lit comme un caractère. Les marqueurs et compteurs s'écrivent en ascii.
4. `Compare-Object` en PowerShell 5.1 refuse un tableau vide. Pour comparer deux `git status --porcelain`, passer par `Where-Object { $avant -notcontains $_ }`.
5. Une consigne qui nomme le fichier `journal.log` invite le modèle à y écrire lui-même, sans horodatage, en double du lanceur. Écrire noir sur blanc que le résumé va dans la réponse et que le lanceur seul écrit dans le journal.

**Pourquoi les automates restent sur le PC.** Git et Obsidian Sync ne se croisent que sur le PC. Le déménagement sur un serveur est la phase 9 du plan, premier pas du palier 2, quand des employés ne pourront plus dépendre du PC.

Voir [[second-brain-obsidian]] pour la structure du coffre.
