---
name: agent-whatsapp-modules
description: "La forme de l'agent WhatsApp openwa-agent depuis le découpage du 7 septembre 2026 : un routeur de 321 lignes, des modules d'intention découverts par un registre, où le cloner, et l'état inhabituel de son dépôt."
metadata: 
  node_type: memory
  type: project
  originSessionId: 0da1055e-dea4-4c4e-880a-db763a81c851
  modified: 2026-09-07T23:54:06.033Z
---

L'agent WhatsApp de Souleman, dépôt privé `babaeyasouleman-lgtm/openwa-agent`, tourne sur Railway et lui parle tous les jours. Cloné sur le PC dans `C:\Projets\openwa-agent`, hors OneDrive et hors coffre, depuis le 2026-09-07. Ne pas le recloner ailleurs.

**Phase 5 du [[Plan Jarvis]], faite le 2026-09-07.** `handleIncomingMessage.js` est passé de 862 lignes à 321. Il ne fait plus que router. Chaque capacité vit dans son fichier sous `agent/src/application/intents/`, et un registre les découvre au démarrage. **Ajouter une intention est un fichier neuf, jamais une ligne dans le routeur.** C'est ce que les phases 6, 7 et 8 exigent, elles en ajoutent chacune une.

**Le contrat est écrit dans `agent/src/application/intents/LISEZMOI.md`**, c'est là qu'il faut aller avant d'ajouter quoi que ce soit, pas dans le routeur. Un module déclare `type` avec `handle(result, ctx)`, ou `sessionTypes` avec `resume(session, ctx)`, ou les deux. 16 modules couvrent 13 types du classifier et 11 dialogues.

**Le fall-through, la subtilité qui coûte cher à redécouvrir.** Quand Souleman ne répond pas à une carte de validation et passe à autre chose, la session est abandonnée et son message repart en classification normale. `resume()` retourne donc `HANDLED` ou `FALLTHROUGH`. Un module qui l'oublie enferme Souleman dans un dialogue sans sortie.

**L'ordre du bloc session est déclaré par les modules, pas codé dans le routeur.** `avantAnnulation` pour `external_pending`, qui passe même devant « Annule » parce que tout ce que Souleman écrit part alors vers l'inconnu. `avantConfirmation` pour `pick_task` et `pick_slot`, parce qu'un « OK » sur une liste de créneaux veut dire « le premier » et non « je valide la carte ».

**Un bug préexistant, vu le 2026-09-07 et volontairement non corrigé.** Après l'abandon d'une liste, le `isConfirmation` global est encore évalué avec la session effacée mais toujours en mémoire : un « ok » au mauvais moment peut valider une session `pick_task`. Un commentaire le signale à l'endroit exact du routeur. La règle « un découpage ne corrige pas » a tenu, mais c'est à traiter un jour.

**L'état du dépôt, inhabituel.** La branche par défaut est `claude/dazzling-mccarthy-H0YrY`, pas `main`, resté au 17 juin et 51 commits en arrière. C'est de cette branche que Railway déploie. `refactor/clean-architecture` est déjà fusionnée. Le dépôt n'avait pas bougé du 31 juillet au 7 septembre.

**Tests.** `cd agent && node --test`. 144 verts au 2026-09-07, dont 23 neufs sur le registre et le routage, qui tournent sans réseau ni Notion ni Google ni classifier. **Quatre tests sont rouges depuis avant le découpage**, tous dans `dates.test.js` sur les fuseaux Toronto : c'est la référence, ni plus ni moins après un changement. `npm install` est nécessaire sur un clone frais, sinon trois fichiers échouent faute de `@anthropic-ai/sdk`.

**Ce qui ne se touche pas.** `infrastructure/classifier.js` est réglé pour Haiku 4.5 avec prompt caching. La règle du plan dit que l'appel au modèle reste isolé dans ce seul fichier, c'est ce qui permettra de changer de fournisseur sans réécriture.

**Le compte GitHub du PC, à surveiller.** Le 2026-09-07, `gh` s'était retrouvé authentifié sous `swebagencyca-agence`, qui n'a accès à aucun dépôt de Souleman : coffre bloqué à 14 commits en attente, clone de l'agent impossible, avec un « Repository not found » trompeur. Réglé par `gh auth login --web`, code à huit caractères autorisé depuis le téléphone, jeton écrit dans le trousseau sans passer par la conversation. Les deux comptes coexistent dans `gh`, `gh auth switch` bascule.

Voir [[coffre-automatisations]] pour les cinq automates du coffre.
