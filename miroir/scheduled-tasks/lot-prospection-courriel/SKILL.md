---
name: lot-prospection-courriel
description: Mardi et jeudi 12 h 05: construit et envoie 3 courriels de prospection avec image de maquette, puis sort les relances J+3 dues
---

Lot de prospection S-WEB Agency. Tu travailles pour Souleman Baba, S-WEB Agency, Gatineau.

Invoque le skill `prospect-email` (outil Skill, nom exact `prospect-email`) et suis son SKILL.md du debut a la fin. Tout ce dont tu as besoin est dedans et dans ses fichiers voisins COURRIEL.md, ENVOI.md, SOURCE.md.

Deroule de cette execution, dans cet ordre:

1. `python C:\Users\Administrator\.claude\skills\prospect-email\scripts\lot.py mode` puis `quota`. Si le mode effectif est `arret`, tu t'arretes la et tu le dis. Si c'est `brouillon`, tu fais tout le travail mais tu crees des brouillons Gmail au lieu d'envoyer, et tu dis pourquoi le mode a bascule.

2. `python ...\lot.py relances` d'abord. Pour chaque relance due, envoie la relance J+3 de COURRIEL.md sur le meme fil, trois lignes, puis marque la fiche `RELANCE`. Une seule relance par prospect, jamais deux. Les relances comptent dans les plafonds du jour.

3. `python ...\lot.py suivants 3` pour les nouvelles fiches. Si SOURCE.md porte une valeur dans `DATA_SOURCE`, lis Notion a la place, comme SOURCE.md le decrit, en UNE seule requete.

4. Pour chaque fiche: controle d'identite (etape 1 du skill, bloquante), un seul fetch de leur site, un seul haut de page de 120 a 200 lignes, image par `scripts\teaser.py`, courriel selon COURRIEL.md, envoi Gmail avec l'image en piece jointe inline plus une version texte simple, puis `lot.py envoye ...`.

5. Regarde chaque image une fois avant son envoi. C'est obligatoire. Une capture vide ou cassee ne part pas: tu marques la fiche `SAUTE` avec la raison.

Contraintes fermes, aucune ne se contourne:
- Le fichier HTML de la maquette ne part JAMAIS par courriel. Seulement l'image.
- Zero tiret cadratin, zero vocabulaire marketing generique, en francais comme en anglais.
- Aucune adresse devinee. Le courriel doit venir de leur site ou de leur fiche Google.
- Tu ne reponds jamais a un fil entrant. Si un prospect a repondu, tu le signales et tu laisses.
- Si une reponse contient STOP, UNSUBSCRIBE, DESABONNER ou une demande de ne plus etre contacte, ajoute l'adresse avec `lot.py stop <adresse>` avant tout autre envoi.

Compte rendu final en cinq lignes: traites, envoyes, sautes avec la raison, le monde visuel de chacun, et la date des prochaines relances. Ecris-le en francais.