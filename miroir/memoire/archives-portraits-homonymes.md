---
name: archives-portraits-homonymes
description: "Deux archives nommées \"Portraits\" dans Downloads appartiennent à deux clients différents, vérifier par empreinte avant d'utiliser des photos."
metadata: 
  node_type: memory
  type: project
  originSessionId: cf76e1e0-d059-4eb0-a65c-43bee4264442
  modified: 2026-09-03T02:23:53.919Z
---

Le dossier `Downloads` contient deux archives dont le contenu s'appelle
`Portraits/` mais qui appartiennent à deux projets sans rapport :

- `PORTFOLIO-20260822T204519Z-1-001.zip` → sous-dossier `PORTFOLIO/Portraits`,
  19 fichiers `IMG_82xx`, `DSC08195`, `DSC08211`, `NECK.png`. **Ce sont les
  photos de Moctar Thera** (voir [[portfolio-moctar-thera]]).
- `Portraits-20260806T062325Z-1-001.zip` → 25 fichiers `JPE*`, `DSC089xx`,
  `_JPE9xxx`. **Ce sont celles de Pose Ta Pierre**, octet pour octet
  identiques à `PoseTaPierre\_source\Portraits\`.

Le 2 septembre 2026 les deux lots ont été mélangés dans le portfolio de Moctar
avant que Souleman ne repère les images de Pose Ta Pierre à l'écran.

**Pourquoi :** les noms de dossier sont identiques, les deux lots sortent de
boîtiers Sony, et les dates EXIF sont des dates d'export (5 et 6 août 2026),
pas des dates de prise de vue. Rien ne les distingue au nom ni à la date.

**Comment l'appliquer :** avant d'intégrer des photos venant de `Downloads`,
comparer les empreintes MD5 avec les dossiers clients déjà présents sur le
Bureau. Le test prend dix secondes et il est le seul concluant. Ne jamais se
fier au nom du dossier ni à l'EXIF pour attribuer un lot à un client.
