# Jarvis, entrée de session

Lis ce fichier en premier, et rien d'autre avant de savoir ce que la phase demande.
Tout ce qui est long vit ailleurs, avec son chemin. Tu y vas par grep, section par
section, jamais en entier. Mis à jour par la dernière session, le 11 septembre 2026, session 2 de l'équipe.

## Où j'en suis

Palier 1 complet depuis le 8 septembre 2026. Les phases 1 à 8 quater tournent.
Phases 9 à 12, les premiers chefs hors du PC : rien de fait, les chefs se
construisent d'abord sur le PC, chantier ci-dessous. Le palier 2 s'ouvre sur un signal de clients, pas
sur une date. La phase 9 attend que le chemin des réponses ait tourné quelques jours.

**Chantier en cours depuis le 11 septembre 2026 : construire l'équipe, chef par chef,
avant la phase 9.** Sept sessions dans l'ordre, le socle commun d'abord, puis le chef
de cabinet. L'ordre, ce que chaque session produit et le prompt de la suivante vivent
dans `Second Brain\_Équipe\Construction de l'équipe.md`. Le lire en entier, il est court.
Sessions 1 et 2 faites le 11 septembre. Session 2, le chef de cabinet : sa fiche et
le contrat dans `_Équipe\Chef de cabinet.md`, le champ 13 du gabarit écrit, l'arbitre
dans `C:\Obsidian\cabinet\consigne.md`, le rôle `cabinet` partout (Opus, priorité 1),
les phases 9 à 16 du plan réécrites pour huit chefs, et côté agent les objectifs :
trois par semaine, la question du jour entre 10 h et midi, le bilan du soir, le
dimanche. Puis sa revue du soir, appliquée et poussée, commit `d9136e4` : prompts à
l'affirmatif, une chose dite une fois (`infrastructure/dits.js`), programme fusionné,
plus de mode d'emploi en bas des messages, rituels variés, transcript entier, dimanche
sans redite. Le détail dans `_Équipe\Chef de cabinet, journée simulée.md`. Il reste à
Souleman à vivre sa journée avec lui, condition de fin de la session 2.
Prochaine : la session 3, le chef Déclic. Le preneur ne lit qu'une consigne, quatre
corrections l'attendent, écrites dans la section de la session 3.

Railway déploie la branche `claude/dazzling-mccarthy-H0YrY`, pas `main`. Avant de
toucher au dépôt : `git log origin/claude/dazzling-mccarthy-H0YrY..HEAD`.

Tests : `cd C:\Projets\openwa-agent\agent && node --test`. 344 tests, 344 verts,
mesuré le 11 septembre 2026. Le chiffre de référence est celui que tu mesures.

## Comment on travaille, en six lignes

- Une phase, une session. Quand le contexte dépasse 300 k, on ferme : mettre à jour
  ce fichier, écrire le prompt de la suivante en cinq lignes, et Souleman rouvre.
- Le comportement vit dans une consigne.md, pas dans le code. Le script ne change que
  si la mécanique change. Aucun accent dans un .ps1, PowerShell 5.1 lit en ANSI.
- Le déterministe d'abord, le modèle pour juger.
- Ce que Souleman fait à la main est écrit dans la phase, pas découvert en route.
- Le PC est le seul écrivain du coffre. L'agent n'a aucun jeton sur second-brain.
- Le coffre garde le pourquoi, le registre garde l'état.

## Comment une session dépense, et comment elle ne dépense pas

Mesuré le 10 septembre 2026 sur la phase 8 : 350 millions de tokens, 680 appels,
98 % en relecture de cache. Ce qui coûte n'est pas de lire, c'est de porter ce qu'on
a lu pendant tous les appels qui suivent. Les 15 % d'appels de la fin pèsent 24 %.

- Toute exploration de code passe par un sous-agent Explore qui rapporte deux Ko avec
  les numéros de lignes. La session principale ne lit que la plage qu'elle modifie,
  avec `sed -n 'a,bp'`, jamais un fichier entier de plus de 200 lignes.
- Ne jamais lire Plan Jarvis.md, les fichiers mémoire, ou un journal.log en entier.
  Grep d'abord, plage ensuite.
- Un test à la fois pendant le travail : `node --test test/<fichier>.test.js`. La
  suite entière une fois, avant de rendre.
- Compte rendu final en 40 lignes. En cours de route, une ligne par étape.
- Ne pas relire ses propres sorties écrites dans scratchpad ou tool-results : les
  produire courtes avec head et tail.

## La carte, où vivent les choses

| Quoi | Où | Poids | Quand le lire |
|---|---|---|---|
| Le plan complet, 16 phases, failles connues | `C:\Obsidian\Second Brain\02 Projets\Plan Jarvis.md` | 199 Ko | Par grep. Tableau lignes 15 à 32, règles 36 à 48, failles à partir de 1537 |
| Contrat pour ajouter une capacité à l'agent | `C:\Projets\openwa-agent\agent\src\application\intents\LISEZMOI.md` | 14 Ko | Seulement si la phase ajoute ou modifie une intention |
| Code de l'agent, 14 000 lignes, 20 % de commentaires qui racontent le pourquoi | `C:\Projets\openwa-agent\agent\src` | 620 Ko | Par sous-agent. L'en-tête d'un fichier dit pourquoi il existe et quel bug il répare |
| Tests, 32 fichiers | `C:\Projets\openwa-agent\agent\test` | 218 Ko | Jamais en lecture, seulement en exécution |
| Histoire du dépôt avant le plan, juin à juillet 2026 | `C:\Projets\openwa-agent\CLAUDE.md` | 77 Ko | Jamais à l'entrée. Grep si une session touche Notion, Telegram, le pairing WhatsApp ou les variables d'environnement |
| Les automates du PC, un dossier chacun : consigne.md, un .ps1, journal.log | `C:\Obsidian\{bibliothecaire, matin, courriels, reunions, transcriptions, captures, cerveau, billets, cabinet, filet}` | 65 Ko de consignes | La consigne de l'automate touché, et elle seule |
| L'enchaînement de nuit, étape par étape | `C:\Obsidian\bibliothecaire\passage.ps1` | 19 Ko | Si la phase ajoute une étape au passage. Les anciennes versions sont dans `bibliothecaire\avant\` |
| Ce qui quitte le PC | `C:\Obsidian\cerveau\liste-blanche.txt` et `export.ps1` | 10 Ko | Toute phase qui touche à l'export, et on relit deux fois |
| Table des matières du coffre, une ligne par note | `C:\Obsidian\bibliothecaire\index.txt` | 21 Ko | À la place de lister le coffre |
| Le coffre | `C:\Obsidian\Second Brain` | | Une note à la fois, jamais un dossier. Le bibliothécaire y range la nuit |
| Charte, gabarit et règles communes de l'équipe | `C:\Obsidian\Second Brain\_Équipe\` | 50 Ko | Par le chantier de l'équipe seulement. Charte et gabarit par section, Règles communes en entier, il est court |
| Test de cohérence des consignes, côté PC | `cd C:\Obsidian; node --test equipe/regles-communes.test.js` | 4 Ko | En exécution, à la fin de chaque session de chef. Le dossier seul ne marche pas sous node 24 |
| Journal hebdo du bibliothécaire | `C:\Obsidian\Second Brain\_Bibliothécaire\2026-Sxx.md` | 20 à 25 Ko | Jamais à l'entrée |
| Mémoire de Claude Code, un fait par fichier | `C:\Users\Administrator\.claude\projects\C--Users-Administrator-OneDrive-Bureau\memory\` | 2 Ko chacun | L'index MEMORY.md est déjà dans le contexte. Miroir versionné dans `C:\Obsidian\miroir\memoire\` |

Quatre tâches Windows, vérifiées le 10 septembre 2026 : « Filet coffre Obsidian »,
« Filet automates », « Bibliothecaire du coffre » (le passage de nuit, qui enchaîne
matin, transcriptions, courriels, réunions, captures, rangement, export), « Preneur de
billets ». Le dépôt git de `C:\Obsidian` s'appelle jarvis-automates et le filet y
commet tout, ce fichier compris.

## Les pièges payés, une ligne chacun, le détail dans le plan

- Ajouter une action à multi_action, c'est quatre endroits : l'enum du schéma, le bloc
  Format du prompt, KNOWN_ACTIONS dans intents\multiAction.js, commitSession.js. Un
  maillon manquant ne lève aucune erreur. Deux tests de comprehension.test.js le gardent.
- Le prompt du classifier est un gabarit à accents graves. Aucun accent grave dans une
  description d'intention, sinon l'agent ne démarre plus.
- Toute valeur énumérée dans un prompt vit à un seul endroit. Les organisations sont
  dans la constante ORGANISATIONS, jamais en dur ailleurs. S-WEB manquait à deux copies
  sur six pendant des semaines, en silence.
- Un message de plus de 600 caractères part sur Sonnet, config.classifier.seuilLong.
- Les cartes de validation : la liste de ce qui se fait sans demander est dans
  domain/cartes.js. Ne pas remettre de carte sur ce que Souleman a retiré le 10 septembre.
  Le ton vit dans domain/voix.js, à un seul endroit.
- Ajouter une capacité, c'est deux fichiers, ou trois si elle pose une carte. Jamais le
  routeur. Si un if te tente dans handleIncomingMessage.js, élargis ctx, comme clarify.
- Le compte GitHub bascule tout seul et le message ment. Si TOUS les dépôts répondent
  « Repository not found » : `& "C:\Program Files\GitHub CLI\gh.exe" auth switch --user babaeyasouleman-lgtm`. gh est hors PATH.
- Les connecteurs de l'app (Gmail, agenda, Fathom) n'existent pas en `claude -p`.
  Vérifier avec `claude mcp list` avant de compter dessus dans un automate.
- Le CLI Claude ne garde qu'un compte. Les automates de nuit tournent sous S-WEB. Le
  passage écrit le compte en première ligne de son journal et le compare à compte.txt.
  Si la session OAuth expire, tout ce qui pense s'arrête d'un coup, code 1 en 4 secondes.
- Ne jamais lancer passage.ps1 pendant que la tâche Windows tourne, le verrou refuse et
  c'est voulu. Ne jamais garder un journal.log ouvert pendant qu'un automate écrit,
  sous Windows ça l'empêche d'écrire. Deux passages peuvent tourner en parallèle, rien
  ne l'empêche à part le verrou.
- Un identifiant de déploiement Railway n'est pas un hash git. Comparer les messages.
- lessons.json ne déménage jamais dans le coffre. Depuis le 10 septembre, les leçons
  vivent dans `09 Voix\Leçons de l'agent.md`, écrites par le PC. profile.json ne reçoit
  plus rien mais vit encore sur le volume Railway.
- Les identifiants de capture sont horodatés à l'heure de l'agent, en UTC.
- Un jeton de dépôt n'atteint jamais un journal.
- `constantes.test.js` refuse tout littéral d'état de billet hors de `billets.js` : un
  bilan d'objectif s'appelle « accompli », jamais « fait ». Payé le 11 septembre.
- `node --test <dossier>` ne trouve rien sous node 24 : donner le fichier.
- Le compte gh actif était `swebagencyca-agence` le 11 septembre, d'où le « Repository
  not found » sur le push. Rebasculé. Vérifier avec `gh auth status` avant de conclure
  à un problème de dépôt.
- Un script JS écrit par heredoc bash depuis l'outil perd ses barres obliques inverses,
  et `cat > fichier` sans entrée bloque la commande. Écrire les scripts de modification
  avec l'outil Write, chemins en barres obliques.
- Les événements S-WEB vont dans l'agenda s.webagencyca@gmail.com sans colorId, ils
  héritent de son marron.
- Le miroir de l'export se régénère par robocopy /MIR : c'est le seul endroit où un
  script du coffre supprime, et un garde index.lock arrête l'export si un autre git tourne.
- Le preneur de billets prend « en cours » avant « à faire », donc un passage interrompu
  reprend tout seul. Il saute quand le passage de nuit tient son verrou.

## Ce qui reste ouvert, au 10 septembre

- Les journaux stdout de Railway n'ont jamais été lus. Le raisonnement du classifier y est.
- Le passage de nuit a échoué le 10 septembre sur la limite de session Claude. Rien ne
  surveille ce coût. Les automates et Souleman puisent dans le même quota.
- L'export porte maintenant `_Bibliothécaire`. À vérifier au premier passage.
- captures.ps1 a quatre types neufs jamais joués en réel : reponse-note, annule-billet,
  lecon, correction-biblio.
- profile.json vit encore sur le volume Railway. La faille « deux vérités » reste ouverte.
- Le self-ping du soir ne peut pas boucler la nuit, le téléphone dort.
- `lot-prospection-courriel` est enregistré dans les tâches de l'app Claude, désactivé,
  et ne tournerait pas même activé.
- `_Équipe` n'est pas exporté, et c'est tranché le 11 septembre : il reste dehors,
  l'arbitrage tourne sur le PC. À rouvrir quand le bilan du dimanche devra lire les
  journaux des chefs.
- Les objectifs et les deux rituels du jour n'ont jamais tourné en réel. Le type
  `objectif` de `captures.ps1` non plus. Une journée vécue les dira.
- Rien ne réveille un billet en `attente` quand son enfant est `fait`. Session 3,
  dans `preneur.ps1`. D'ici là l'arbitre le fait à la main, sa consigne le dit.
- Le courriel de la part de S-WEB, brouillon puis envoi après sa validation : décidé le
  11 septembre, pas construit. Il manque un jeton Google avec le droit d'envoi Gmail,
  que Souleman crée à la main. Ensuite `infrastructure/courriel.js` et une intention
  `courriel`, avec carte. Le classifier dit encore qu'il ne sait pas envoyer.
- Souleman veut l'équipe qui tourne PC éteint, sur l'abonnement. C'est la phase 9 :
  une machine Linux ou les routines de Claude Code dans le nuage. Le prix est une règle,
  le PC cesse d'être seul écrivain du coffre, et deux bots ont besoin de Windows, Word et
  le navigateur.

## À la fin de la session

Mettre à jour ce fichier : « Où j'en suis », les pièges si un nouveau a été payé, « Ce qui
reste ouvert ». Dix lignes, pas un récit. Le récit va dans Plan Jarvis.md, dans la section
de la phase, sous « Ce que la phase a appris ». Puis écrire le prompt de la session
suivante en cinq lignes, dont la première est « Lis C:\Obsidian\ENTREE.md ».
