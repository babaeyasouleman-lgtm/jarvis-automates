---
name: agent-whatsapp-modules
description: "La forme de l'agent WhatsApp openwa-agent : un routeur de 321 lignes, des modules d'intention découverts par un registre, le second point de contact obligatoire dans le classifier, la lecture du cerveau en deux temps, et l'état inhabituel de son dépôt."
metadata: 
  node_type: memory
  type: project
  originSessionId: 0da1055e-dea4-4c4e-880a-db763a81c851
  modified: 2026-09-07T23:54:06.033Z
---

L'agent WhatsApp de Souleman, dépôt privé `babaeyasouleman-lgtm/openwa-agent`, tourne sur Railway et lui parle tous les jours. Cloné sur le PC dans `C:\Projets\openwa-agent`, hors OneDrive et hors coffre, depuis le 2026-09-07. Ne pas le recloner ailleurs.

**Phase 5 du [[Plan Jarvis]], faite le 2026-09-07.** `handleIncomingMessage.js` est passé de 862 lignes à 321. Il ne fait plus que router. Chaque capacité vit dans son fichier sous `agent/src/application/intents/`, et un registre les découvre au démarrage. **Ajouter une intention est un fichier neuf, jamais une ligne dans le routeur.** C'est ce que les phases 6, 7 et 8 exigent, elles en ajoutent chacune une.

**Ajouter une capacité, c'est DEUX fichiers, pas un.** Découvert à la phase 6, le 2026-09-08. Le module dans `intents/`, que le registre trouve seul, **et** `infrastructure/classifier.js` à trois endroits : le type dans l'`enum`, sa ligne numérotée dans le prompt, et un bloc `Format pour "<type>"`. Le classifier ne peut pas produire un type qu'il ne connaît pas. Le routeur, lui, ne change toujours pas. Rendre ça déclaratif a été écarté : le prompt du classifier porte des distinctions écrites à la main après des erreurs réelles, et le générer le rendrait moins relisible pour gagner deux endroits tous les six mois. La liste `TYPES_CLASSIFIER` de `intents.test.js` doit rester alignée sur l'`enum`.

**Phase 6 du [[Plan Jarvis]], faite le 2026-09-08 : `query_brain`.** Un fichier neuf, `intents/queryBrain.js`, zéro ligne dans le routeur. Il lit un clone en lecture seule de l'export du coffre, dans `/data/brain` sur le volume Railway, tiré chaque heure plus une fois au démarrage. `infrastructure/brain.js` porte l'accès, `config.brain` les réglages, `BRAIN_REPO_URL` doit porter un jeton **en lecture seule**. Récupération en deux temps : la table des matières seule au premier appel, 3 326 tokens, le modèle choisit 3 à 5 notes ; ces notes en entier au second. Mesuré : 5 664 tokens d'entrée contre 86 391 pour le cerveau complet, soit 15 fois moins, environ 0,008 $ la question.

**Le garde des chemins est la pièce qui protège la vie privée, pas le prompt.** `brain.lireNotes()` refuse tout chemin absent de `index.txt` et tout chemin qui remonte hors du clone. C'est ce qui fait que l'agent dit « je ne sais pas » sur `03 Domaines/Moi` au lieu d'inventer. Vérifié en réel : sur la question du prix TriS, le modèle a demandé `05 Décisions/Validation terrain Libreville.md`, qui est en fait dans `02 Projets`, et le chemin a été refusé au lieu d'être deviné. Zéro note retenue veut dire aucun second appel : le refus est aussi le chemin le moins cher.

**La fraîcheur s'ajoute en code, jamais par le modèle.** `_cerveau à jour d'il y a 40 minutes_` est collé après la réponse, à partir de `fraicheur.txt` du clone et non de la date d'un commit. Un modèle qui l'oublie une fois sur dix présente une décision périmée comme actuelle.

**Le contrat est écrit dans `agent/src/application/intents/LISEZMOI.md`**, c'est là qu'il faut aller avant d'ajouter quoi que ce soit, pas dans le routeur. Un module déclare `type` avec `handle(result, ctx)`, ou `sessionTypes` avec `resume(session, ctx)`, ou les deux. 17 modules couvrent 14 types du classifier et 11 dialogues depuis le 2026-09-08.

**Le fall-through, la subtilité qui coûte cher à redécouvrir.** Quand Souleman ne répond pas à une carte de validation et passe à autre chose, la session est abandonnée et son message repart en classification normale. `resume()` retourne donc `HANDLED` ou `FALLTHROUGH`. Un module qui l'oublie enferme Souleman dans un dialogue sans sortie.

**L'ordre du bloc session est déclaré par les modules, pas codé dans le routeur.** `avantAnnulation` pour `external_pending`, qui passe même devant « Annule » parce que tout ce que Souleman écrit part alors vers l'inconnu. `avantConfirmation` pour `pick_task` et `pick_slot`, parce qu'un « OK » sur une liste de créneaux veut dire « le premier » et non « je valide la carte ».

**Un bug préexistant, vu le 2026-09-07 et volontairement non corrigé.** Après l'abandon d'une liste, le `isConfirmation` global est encore évalué avec la session effacée mais toujours en mémoire : un « ok » au mauvais moment peut valider une session `pick_task`. Un commentaire le signale à l'endroit exact du routeur. La règle « un découpage ne corrige pas » a tenu, mais c'est à traiter un jour.

**L'état du dépôt, inhabituel.** La branche par défaut est `claude/dazzling-mccarthy-H0YrY`, pas `main`, resté au 17 juin et 51 commits en arrière. C'est de cette branche que Railway déploie. `refactor/clean-architecture` est déjà fusionnée. Le dépôt n'avait pas bougé du 31 juillet au 7 septembre.

**Tests.** `cd agent && node --test`. **169 tests et 165 verts au 2026-09-08**, dont 14 neufs dans `queryBrain.test.js` sur la liste blanche et la fraîcheur, qui tournent sans réseau ni Notion ni Google ni classifier. **Quatre tests sont rouges depuis avant le découpage**, tous dans `dates.test.js` sur les fuseaux Toronto : c'est la référence, ni plus ni moins après un changement. `npm install` est nécessaire sur un clone frais, sinon trois fichiers échouent faute de `@anthropic-ai/sdk`.

**Ce qui ne se touche pas.** `infrastructure/classifier.js` est réglé pour Haiku 4.5 avec prompt caching. La règle du plan dit que l'appel au modèle reste isolé dans ce seul fichier, c'est ce qui permettra de changer de fournisseur sans réécriture. C'est pour ça que `query_brain` n'a pas créé son propre client : le classifier exporte `appelerModele()`, et `new Anthropic()` n'existe toujours qu'à un seul endroit du projet. **Appeler via l'objet, jamais en déstructurant** : `classifier.appelerModele(...)`, sinon la référence est figée au chargement et les tests ne peuvent plus la remplacer, donc ils partiraient contre l'API réelle.

**Le compte GitHub du PC, à surveiller.** Le 2026-09-07, `gh` s'était retrouvé authentifié sous `swebagencyca-agence`, qui n'a accès à aucun dépôt de Souleman : coffre bloqué à 14 commits en attente, clone de l'agent impossible, avec un « Repository not found » trompeur. Réglé par `gh auth login --web`, code à huit caractères autorisé depuis le téléphone, jeton écrit dans le trousseau sans passer par la conversation. Les deux comptes coexistent dans `gh`, `gh auth switch` bascule.

Voir [[coffre-automatisations]] pour les automates du coffre et l'export qui alimente ce cerveau.
