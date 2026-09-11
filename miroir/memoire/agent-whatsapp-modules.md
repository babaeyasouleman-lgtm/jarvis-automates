---
name: agent-whatsapp-modules
description: "Ou vit la verite sur l'agent WhatsApp openwa-agent, et les trois faits qui ne sont ecrits nulle part ailleurs : le prompt du classifier en quatre familles, les trois pieces qui ecrivent des messages avec leur ton dans voix.js, et les brides de spontane.js."
metadata: 
  node_type: memory
  type: project
  originSessionId: eee27d88-f723-4809-8264-1500fd32fce5
  modified: 2026-09-11T03:43:29.077Z
---

Reduit le 10 septembre 2026 de 25 Ko a ceci. L'ancienne version est dans le git de `C:\Obsidian`, sous `miroir\memoire\`, et dans `memory-avant-2026-09-10\` a cote de ce dossier. Tout ce qu'elle racontait vit dans le plan, dans LISEZMOI.md ou dans les en-tetes des fichiers source.

**Ou aller.** L'entree de toute session Jarvis est `C:\Obsidian\ENTREE.md` : etat, carte des fichiers, pieges payes, ce qui reste ouvert. Le contrat pour ajouter une capacite est `agent\src\application\intents\LISEZMOI.md`. L'histoire de chaque piece est dans l'en-tete de son fichier. Les recits de phase sont dans `02 Projets\Plan Jarvis.md`, par grep.

**Ce qui n'est ecrit qu'ici.**
- Le prompt du classifier fait environ 4 870 tokens et s'ouvre sur quatre familles : faire, donner, garder, ne pas savoir. Le champ reasoning demande d'abord « qu'est-ce qu'il attend de moi », parce que c'est la decision qui rate le plus. Ne pas le rallonger sans raison : le cout d'un prompt long n'est pas l'argent, il est en cache, c'est l'attention.
- Trois pieces ecrivent des messages : matin.js le briefing de 8 h 30, journal.js le journal de 22 h 30, spontane.js les messages de la journee. Leurs regles de ton vivent dans `domain/voix.js`, a un seul endroit. N'en recopier aucune dans une consigne.
- Les brides de spontane.js portent sur le ton et l'espacement, jamais sur la frequence : quatre-vingt-dix minutes entre deux messages, aucun jugement, aucune duree transmise au redacteur. Souleman a coupe deux fois une bride qui jugeait.
- Le jugement du modele ne se verifie pas sur le PC : aucune cle API locale. Les tests de comprehension.test.js jouent des reponses enregistrees.

**Why:** deux sessions ont lu ce fichier en entier, 25 Ko a chaque fois, pour des faits qui etaient deja dans le plan.
**How to apply:** lire ENTREE.md, puis LISEZMOI.md seulement si la phase touche une intention. Voir [[coffre-automatisations]] et [[jarvis-cout-des-sessions]].
