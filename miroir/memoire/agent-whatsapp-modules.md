---
name: agent-whatsapp-modules
description: "La forme de l'agent WhatsApp openwa-agent : un routeur de 321 lignes, des modules d'intention découverts par un registre, le second point de contact obligatoire dans le classifier, la lecture du cerveau en deux temps, la boîte aux lettres des captures qui écrit avant de pousser, et l'état inhabituel de son dépôt."
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

**Phase 7 du [[Plan Jarvis]], faite le 2026-09-08 : `capture`.** Un fichier neuf, `intents/capture.js`, plus les trois endroits du classifier. Trois entrées, une sortie : une réflexion dictée, un lien partagé dont l'agent lit et résume la page, un livre commenté. Une vidéo partagée donne le lien et le commentaire, **jamais de transcription**, et l'agent le dit. `infrastructure/outbox.js` porte la boîte aux lettres, `config.captures` les réglages, `CAPTURES_REPO_URL` est le **seul jeton d'écriture de tout l'agent** et il ne donne accès qu'à `jarvis-captures`.

**L'ordre de la boîte aux lettres est tout le sujet.** Écrire dans `/data/outbox` sur le volume, PUIS copier dans le clone, commit, push, et **n'effacer qu'après le push**. Jamais l'inverse. Le premier jet effaçait la capture quand `git diff --cached` ne trouvait rien à enregistrer, en supposant qu'elle était déjà dans le dépôt : faux après une poussée refusée au réseau, où un commit local attend et où les mêmes fichiers recopiés ne changent plus l'index. La capture disparaissait sans avoir jamais atteint le dépôt. Corrigé : on commit s'il y a de quoi, **on pousse toujours**, on efface après. C'est `capture.test.js` qui l'a attrapé, avec un vrai dépôt git nu dans un dossier temporaire ; une poussée simulée n'aurait rien prouvé.

**`capture` ne pose AUCUNE carte de validation, et c'est une décision.** Une capture ne part vers aucun tiers, ne crée rien dans Notion, ne réserve rien : elle atterrit dans `00 Inbox`, sous git, relue le dimanche. Une carte à valider à chaque réflexion dite en marchant tuerait l'usage que le plan appelle « capture sans réfléchir, range plus tard ». **On valide ce qui engage, pas ce qui se note.** Conséquence : rien à ajouter dans `commitSession.js`, le contrat reste à deux fichiers. Le billet de la phase 8, lui, aura une carte et touchera ce troisième endroit.

**Le piège du classifier, payé à la phase 7.** `SYSTEM_PROMPT` est un gabarit délimité par des accents graves. Une description d'intention qui en contient, même pour citer un nom de champ, ferme la chaîne et l'agent ne démarre plus. Citer avec des guillemets droits dans ce prompt.

**Le webhook `/webhook` est le point d'entrée du raccourci Siri.** POST JSON avec `from` (le numéro sans le plus), `type: text`, `body`, `senderName`. Protégé par `adminGuard` : il faut `?key=<ADMIN_TOKEN>`, sinon 401 silencieux. La réponse part sur WhatsApp, pas dans Siri. Un point d'entrée qui **renvoie** la réponse, pour que Siri la lise à voix haute, n'existe pas encore ; c'est ce qu'il faudra pour `Demande à Jarvis`.

**Le contrat est écrit dans `agent/src/application/intents/LISEZMOI.md`**, c'est là qu'il faut aller avant d'ajouter quoi que ce soit, pas dans le routeur. Un module déclare `type` avec `handle(result, ctx)`, ou `sessionTypes` avec `resume(session, ctx)`, ou les deux. 18 modules couvrent 15 types du classifier et 11 dialogues depuis le 2026-09-08.

**Le fall-through, la subtilité qui coûte cher à redécouvrir.** Quand Souleman ne répond pas à une carte de validation et passe à autre chose, la session est abandonnée et son message repart en classification normale. `resume()` retourne donc `HANDLED` ou `FALLTHROUGH`. Un module qui l'oublie enferme Souleman dans un dialogue sans sortie.

**L'ordre du bloc session est déclaré par les modules, pas codé dans le routeur.** `avantAnnulation` pour `external_pending`, qui passe même devant « Annule » parce que tout ce que Souleman écrit part alors vers l'inconnu. `avantConfirmation` pour `pick_task` et `pick_slot`, parce qu'un « OK » sur une liste de créneaux veut dire « le premier » et non « je valide la carte ».

**Un bug préexistant, vu le 2026-09-07 et volontairement non corrigé.** Après l'abandon d'une liste, le `isConfirmation` global est encore évalué avec la session effacée mais toujours en mémoire : un « ok » au mauvais moment peut valider une session `pick_task`. Un commentaire le signale à l'endroit exact du routeur. La règle « un découpage ne corrige pas » a tenu, mais c'est à traiter un jour.

**L'état du dépôt, inhabituel.** La branche par défaut est `claude/dazzling-mccarthy-H0YrY`, pas `main`, resté au 17 juin et 51 commits en arrière. C'est de cette branche que Railway déploie. `refactor/clean-architecture` est déjà fusionnée. Le dépôt n'avait pas bougé du 31 juillet au 7 septembre.

**Tests.** `cd agent && node --test`. **187 tests et 183 verts au 2026-09-08 après la phase 7**, dont 14 dans `queryBrain.test.js` et 18 dans `capture.test.js`, qui tournent sans réseau ni Notion ni Google ni classifier. **Quatre tests sont rouges depuis avant le découpage**, tous dans `dates.test.js` sur les fuseaux Toronto : c'est la référence, ni plus ni moins après un changement. `npm install` est nécessaire sur un clone frais, sinon trois fichiers échouent faute de `@anthropic-ai/sdk`.

**Ce qui ne se touche pas.** `infrastructure/classifier.js` est réglé pour Haiku 4.5 avec prompt caching. La règle du plan dit que l'appel au modèle reste isolé dans ce seul fichier, c'est ce qui permettra de changer de fournisseur sans réécriture. C'est pour ça que `query_brain` n'a pas créé son propre client : le classifier exporte `appelerModele()`, et `new Anthropic()` n'existe toujours qu'à un seul endroit du projet. **Appeler via l'objet, jamais en déstructurant** : `classifier.appelerModele(...)`, sinon la référence est figée au chargement et les tests ne peuvent plus la remplacer, donc ils partiraient contre l'API réelle.

**Le compte GitHub du PC, à surveiller.** Le 2026-09-07, `gh` s'était retrouvé authentifié sous `swebagencyca-agence`, qui n'a accès à aucun dépôt de Souleman : coffre bloqué à 14 commits en attente, clone de l'agent impossible, avec un « Repository not found » trompeur. Réglé par `gh auth login --web`, code à huit caractères autorisé depuis le téléphone, jeton écrit dans le trousseau sans passer par la conversation. Les deux comptes coexistent dans `gh`, `gh auth switch` bascule.

Voir [[coffre-automatisations]] pour les automates du coffre et l'export qui alimente ce cerveau.
