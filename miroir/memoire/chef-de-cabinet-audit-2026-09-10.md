---
name: chef-de-cabinet-audit-2026-09-10
description: "Ce que l audit du 10 septembre 2026 a tranche pour l agent WhatsApp, ce que Souleman veut dire par proactif, les cartes qu il a retirees, et ce qui attend encore (push Railway, journaux stdout, phase 9)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 86c0bbe9-1496-4b58-b1f9-6186f67887b1
  modified: 2026-09-10T15:25:18.006Z
---

Audit du chef de cabinet (agent WhatsApp) le 10 septembre 2026, session d'abord de questions puis de code. Sur la branche `claude/dazzling-mccarthy-H0YrY`, celle que Railway deploie. Pousses le 10 septembre jusqu'a `f84b13d`. **Seul `f50e6d8`, les disponibilites sur plusieurs semaines, ne l'est pas** : le push echouait sur « Repository not found » au 11 septembre, un probleme d'acces GitHub et non de code. 329 tests verts.

**Ce que « proactif » veut dire pour lui, dans ses mots** : un message vers 8 h qui dit a quoi ressemble la journee et ce qui compte ; le rappeler ; faire des choses sans demander avec l'equipe d'agents ; lui poser des questions avec le contexte ; lui demander comment s'est passee la journee ; le suivre le dimanche (« finalement, tu as tourne ? ») ; l'etudier (ses journees, ce qu'il aime, ses priorites). Ce qui l'agace le plus : le manque d'initiative, et ne pas etre compris. Il ne va pas dans Obsidian : « c'est son monde a lui », l'agent donne le contexte lui-meme.

**Cartes retirees a sa demande** : evenement (meme dicte par lui), modification d'evenement, mise a jour de tache, idee, billet (« j'ai lance X », il dit non), rappel a heure fixe. Il dit « annule » pour defaire. **Cartes gardees** : tache neuve (« mitige »), suppression, tout ce qui part vers un tiers (site en ligne, courriel, facture). La liste vit dans `agent/src/domain/cartes.js`.

**Decisions de conception** : une seule memoire, le coffre (`09 Voix/Lecons de l'agent.md` ecrit par le PC, `profile.json` ne recoit plus rien) ; seul son numero parle a l'agent, Telegram n'est qu'un secours ; les reponses a un message ouvert par l'agent passent par `infrastructure/ouvertures.js` et le type `reponse` ; le journal du soir n'avale plus le message suivant ; question de fond une par soir avec sa section, puis « une autre ? » ; suivis redemandes le dimanche, abandonnes apres deux dimanches sans reponse ; briefing a 8 h, plus leger la fin de semaine.

**Angles morts restes ouverts** : les journaux stdout de Railway n'ont jamais ete lus (le raisonnement du classifier y est) ; le passage de nuit du bibliothecaire a echoue le 10 sur la limite de session Claude et rien ne surveille ce cout ; l'export du coffre porte maintenant `_Bibliothecaire`, verifier au premier passage ; captures.ps1 a quatre types neufs jamais joues en reel (`reponse-note`, `annule-billet`, `lecon`, `correction-biblio`). **La phase 9 attend** que le chemin des reponses ait tourne quelques jours.

**Why:** il a demande que la session conclue et code, et que rien ne soit deploye ni supprime sans le lui montrer.
**How to apply:** avant de toucher a l'agent, relire `agent/src/application/intents/LISEZMOI.md`, section du 10 septembre. Ne pas remettre de carte sur ce qu'il a retire. Ne pas reajouter d'anecdote « Erreur reelle du... » dans le prompt du classifier : les regles y sont sans leur histoire, exprès. Voir [[agent-whatsapp-modules]] et [[sweb-contexte-de-travail]].
