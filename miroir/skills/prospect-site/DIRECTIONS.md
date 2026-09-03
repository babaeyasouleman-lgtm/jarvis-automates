# Direction artistique: le moteur

Lu une seule fois, à l'étape design, avant d'écrire la moindre ligne de HTML.
Son but: empêcher que deux maquettes se ressemblent, et empêcher le réflexe par défaut
qui produit le look IA.

## La règle du moteur

Avant de construire, écris **l'ADN du build** en une ligne et affiche-la. Rien ne
commence avant.

```
MONDE <nom> · HÉROS <forme> · ÉTIQUETTE <traitement> · TYPO <titre + corps>
ACCENT <nom #hex> · RYTHME <largeurs> · SIGNATURE <l'objet du métier>
```

**Contrainte dure: aucun des quatre premiers axes (monde, héros, étiquette, typo) ne
peut répéter les cinq derniers builds.** Vérifie contre `BUILT.tsv`. Si le banc d'un axe
est épuisé, invente une entrée neuve et ajoute-la au banc, ne recycle pas.

Un axe se choisit dans cet ordre de priorité:
1. Ce que les actifs imposent (photo panoramique 1600px, ou rien d'utilisable).
2. Ce que le métier appelle (un couvreur n'est pas une clinique).
3. Ce qui n'a pas servi récemment.

---

## Axe 1: le MONDE

Le levier principal. Un monde est un parti pris complet, pas une ambiance. Il fixe
d'avance la température de la palette, la classe de la typo, le rayon, la présence ou
non de bordures, et le traitement des photos. Choisir un monde avant d'écrire du CSS
est ce qui empêche le retour au réflexe par défaut.

| # | Monde | Ce que ça donne |
|---|---|---|
| 1 | **Atelier suisse** | grille visible, grotesque, blanc massif, alignements stricts, rayon 0, filets 1px, photos désaturées |
| 2 | **Éditorial papier** | sérif de titrage, fond crème, colonnes de magazine, légendes sous les photos, rayon 0 à 2 |
| 3 | **Brutalisme doux** | blocs de couleur pleins, titres très gras en petit corps, bordures 2px, rayon 0, une seule couleur saturée |
| 4 | **Catalogue rétro** | ocre, brique, crème, empattement géométrique années 70, cadres photo 8 à 12px, numérotation visible |
| 5 | **Signalétique industrielle** | condensé en capitales, pictos, bandes diagonales, jaune ou orange sur gris foncé, rayon 0 |
| 6 | **Boutique matiériste** | la matière du métier devient la texture de fond (bois, pierre, tissu, eau), palette tirée de cette matière, typo humaniste, rayon 4 à 8 |
| 7 | **Technique monospace** | monospace pour libellés et chiffres, sans-serif neutre au corps, données en évidence, grille visible |
| 8 | **Carte postale locale** | le quartier porte le design: panoramique, nom du secteur en grand, palette tirée du paysage |
| 9 | **Vitrine nocturne** | fond sombre teinté (jamais gris boueux), une seule couleur lumineuse, les photos portent toute la lumière |
| 10 | **Herbier clinique** | blanc franc, un vert ou bleu très désaturé, illustration au trait, blanc massif, typo légère |
| 11 | **Néo-classique de quartier** | enseigne peinte: empattements gras, vert bouteille ou bordeaux et or, filets doubles, cadres, symétrie |
| 12 | **Blueprint technique** | papier de plan bleu très pâle ou millimétré, traits fins, cotes et annotations en monospace, aucun aplat |
| 13 | **Photo pleine, texte minuscule** | la photo prend 90% de l'écran, typo petite et éparse en capitales espacées, blanc sur image |
| 14 | **Champ de couleur saturée** | une seule couleur franche occupe des sections entières, blanc dessus, très peu de photo |
| 15 | **Terrain et saison** | palette prise de la saison locale, paysage large, typo robuste, textures naturelles |
| 16 | **Artisanat imprimé** | sérigraphie: deux encres qui se superposent, trames de points visibles, décalage d'impression assumé, condensé |

Le monde sombre est **un** monde sur seize, pas la valeur par défaut. Sur un couvreur ou
un salon de quartier, le sombre est presque toujours le mauvais choix.

### Le catalogue étendu: 152 jeux de tokens en plus des seize mondes

Installé le 2026-08-30 dans `mondes/`, extrait des paquets `design-systems` du dépôt
`nexu-io/open-design`. **Les seize mondes ci-dessus restent le catalogue principal.**
Le catalogue étendu ne les remplace pas, il fournit deux choses qu'ils n'ont pas:

1. **Des valeurs de cadrage mesurées**, prêtes à coller. Chaque monde étendu porte sa
   palette complète, son `--text-3xl`, son `--section-y-desktop`, son `--radius-md` et
   son `--container-max`. C'est ce qui rend la section « cadrage » plus bas mécanique
   au lieu de jugée.
2. **De la marge sur la règle du non-répété.** Avec 64 lignes dans `BUILT.tsv`,
   seize mondes commencent à être serrés sur les quatre premiers axes.

**Ne jamais lire `mondes/MONDES.tsv` en entier, il fait 36 Ko.** Passer par le script,
qui n'imprime qu'une dizaine de candidats:

```bash
python scripts/monde.py --fond clair --temp chaud,or --sans-repet
python scripts/monde.py --cherche "editorial|paper|magazine"
python scripts/monde.py --slug cafe --adn      # ligne d'ADN pré-remplie
python scripts/monde.py --slug cafe --css      # le tokens.css du monde
```

`--sans-repet` compare aux 5 derniers builds sur la police de titrage et l'accent, et
nomme les collisions qu'il écarte. Les 91 paquets de marque (Ferrari, Stripe, Nike)
sont exclus par défaut: ce sont des identités d'entreprise, pas des directions
visuelles. `--marques` les rouvre s'il le demande.

**Une limite mesurée, et elle compte.** Sur les 61 paquets libres, 35 titrent en Inter
et 12 en Georgia. La typo du catalogue étendu est le réflexe par défaut que l'axe 4
combat. **Donc: prendre la palette, le rythme et le rayon d'un monde étendu, et
continuer à choisir la typo dans le banc libre**, appairage neuf vérifié par `grep` sur
`BUILT.tsv`. Le détail est dans `mondes/LISEZMOI.md`, à lire une seule fois.

### L'algorithme de sélection

**Étape 1. Classer le prospect dans une famille de métier.**

| Code | Famille | Exemples |
|---|---|---|
| CHA | chantier | couvreur, rénovation, électricien, plombier, maçon, excavation |
| SOIN | soin du corps | spa, médico-esthétique, coiffure, ongles, massage, barbier |
| SANTÉ | santé | dentiste, physio, chiro, naturopathe, clinique médicale |
| DÉT | détail | boutique, vêtements, fleuriste, bijoux, épicerie fine |
| TAB | table | restaurant, traiteur, boulangerie, café, bar, brasserie |
| PRO | service professionnel | avocat, comptable, notaire, courtier, consultant |
| ENT | entretien | nettoyage, déménagement, paysagement, déneigement, piscine |
| ATE | atelier | informatique, sécurité, mécanique, ébénisterie, imprimerie |

**Étape 2. Lire le score de base.** 3 = naturel, 2 = marche, 1 = risqué, 0 = à écarter.

| Monde | CHA | SOIN | SANTÉ | DÉT | TAB | PRO | ENT | ATE |
|---|---|---|---|---|---|---|---|---|
| 1 Atelier suisse | 3 | 1 | 2 | 2 | 1 | 3 | 2 | 3 |
| 2 Éditorial papier | 1 | 3 | 2 | 2 | 2 | 3 | 0 | 1 |
| 3 Brutalisme doux | 2 | 1 | 0 | 3 | 3 | 1 | 2 | 2 |
| 4 Catalogue rétro | 1 | 2 | 0 | 3 | 3 | 1 | 1 | 2 |
| 5 Signalétique industrielle | 3 | 0 | 0 | 1 | 1 | 1 | 3 | 3 |
| 6 Boutique matiériste | 2 | 3 | 1 | 2 | 2 | 1 | 2 | 3 |
| 7 Technique monospace | 1 | 0 | 1 | 1 | 0 | 3 | 1 | 3 |
| 8 Carte postale locale | 2 | 1 | 1 | 2 | 3 | 2 | 3 | 1 |
| 9 Vitrine nocturne | 0 | 3 | 1 | 2 | 3 | 1 | 0 | 2 |
| 10 Herbier clinique | 0 | 3 | 3 | 1 | 1 | 2 | 1 | 0 |
| 11 Néo-classique de quartier | 1 | 2 | 1 | 3 | 3 | 3 | 0 | 2 |
| 12 Blueprint technique | 3 | 0 | 0 | 0 | 0 | 2 | 1 | 3 |
| 13 Photo pleine, texte minuscule | 1 | 3 | 1 | 3 | 3 | 0 | 0 | 1 |
| 14 Champ de couleur saturée | 2 | 1 | 2 | 2 | 2 | 2 | 3 | 1 |
| 15 Terrain et saison | 3 | 0 | 0 | 1 | 1 | 0 | 3 | 1 |
| 16 Artisanat imprimé | 0 | 1 | 0 | 3 | 3 | 0 | 1 | 2 |

**Étape 3. Appliquer les modificateurs.**

| Condition | Effet |
|---|---|
| Le monde a servi dans les 5 derniers builds | **exclu**, quel que soit le score |
| Un site ou une image de référence qu'il a envoyée est rattachée à ce monde | +2 |
| Les actifs l'imposent: photo panoramique 1600px et plus disponible | +1 aux mondes 8, 13, 15 |
| Aucune photo utilisable | +1 aux mondes 1, 3, 7, 12, 14, 16 et 0 forcé sur 13 |
| Le logo est un mot en empattements | +1 aux mondes 2, 11 |
| Le logo est en capitales condensées | +1 aux mondes 5, 12 |
| La couleur du logo est pastel ou très claire | 0 forcé sur le monde 9 |
| Le prospect vend un résultat visuel (avant/après, coiffure, paysage) | +1 aux mondes 13, 15 |

**Étape 4. Trancher.**

- Écart de 3 points ou plus entre le premier et le deuxième: **ne pas poser la question**,
  annoncer le monde retenu et sa raison en une phrase.
- Écart de 2 points ou moins: proposer les **deux premiers** comme options de la question
  unique, décrits par leur allure et non par leur nom.
- Égalité entre plusieurs mondes: départager dans cet ordre, jusqu'à ce qu'il n'en reste
  qu'un ou deux. Celui qui n'a jamais servi, puis celui qui a servi le moins souvent dans
  `BUILT.tsv`, puis le plus petit numéro. Le départage doit être déterministe, sinon deux
  prospects du même métier retombent sur le même monde.
- Aucun monde au-dessus de 2 après modificateurs: c'est le signal que la famille de métier
  est mal classée, reclasser plutôt que forcer.

---

## Axe 2: la forme du HÉROS

**Déjà servi:** photo pleine largeur + Ken Burns · deux colonnes photo portrait ·
typographique seul · deux colonnes avec badge ouvert/fermé · deux colonnes photo
intérieure encadrée · collage décalé · titre + colonne latérale + bande photo ·
split diagonal · vitrine trois panneaux verticaux.

**Banc libre:** panneau parallaxe sans vidéo · héros portant un vrai avis client en
citation · bento 4 tuiles · plein écran typographique avec un seul médaillon photo ·
bande horizontale basse (héros court, contenu tout de suite) · grille de 6 vignettes
métier · héros vidéo ou reel · héros scindé horizontalement (haut typo, bas photo
pleine largeur) · héros avec la carte du territoire desservi.

**Règles qui ne bougent pas:** un visage humain au-dessus de la ligne de flottaison
pour les métiers de proximité, jamais de placeholder dans le héros, le métier nommé
dans le titre, deux couleurs maximum, deux appels à l'action maximum, aucune pastille
d'accroche.

---

## Axe 3: l'ÉTIQUETTE de section

Petit détail, forte signature. C'est ce qui se remarque quand deux maquettes sont
côte à côte.

**Déjà servi:** barre colorée (retirée, lue comme un tiret) · pastille teintée ·
numéro 01 à 05 · chiffre géant en contour · capitales lettrées or · capitales lettrées
sauge · étiquette dans la ligne du titre avec filet vertical · filet tressé traversant
coupé par les mots.

**Banc libre:** aucune étiquette (le titre porte tout) · numéral pivoté à 90 degrés
dans la marge · monospace entre crochets `[ 02 ]` · étiquette en exposant collée au
titre · compteur `01 / 06` aligné à droite · étiquette posée dans la marge gauche sur
la ligne de base du titre · étiquette en négatif dans un carré plein.

---

## Axe 4: la TYPO

**Interdit en police de titrage: Inter, Roboto, Open Sans, Arial, Lato.** En corps de
texte ils sont acceptables.

**Appairages déjà servis (16):** Archivo · EB Garamond + Lato · Fraunces + DM Sans ·
Instrument Serif + Manrope · Bricolage Grotesque + Public Sans · Syne + Chivo ·
Sora + Figtree · Epilogue + Hanken Grotesk · Outfit + Inter · Space Grotesk + Karla ·
Familjen Grotesk + Inter Tight · Gabarito + Karla · Archivo + Public Sans ·
Bodoni Moda + Work Sans · Plus Jakarta Sans + Work Sans.

**Banc libre, rattaché à un monde** (tous sur Google Fonts, donc encodables en base64):

| Titre + corps | Monde |
|---|---|
| Schibsted Grotesk + Newsreader | atelier suisse |
| Geist + Geist Mono | technique monospace |
| Funnel Display + Funnel Sans | brutalisme doux |
| Anybody (condensé) + Barlow | signalétique industrielle |
| Unbounded + Onest | brutalisme doux |
| Bitter + Mulish | catalogue rétro |
| Darker Grotesque + Lora | éditorial papier |
| Alegreya + Alegreya Sans | carte postale locale |
| Vollkorn + Cabin | boutique matiériste |
| Rethink Sans + Newsreader | atelier suisse |
| Zilla Slab + Inter Tight | technique monospace |
| Petrona + Public Sans | éditorial papier |
| Marcellus + Jost | herbier clinique |
| Radio Canada Big + IBM Plex Mono | technique, contexte canadien |
| Antonio + Assistant | signalétique industrielle |

**Playfair Display, Cormorant Garamond et Montserrat sont à haut risque:** ce sont les
polices du look IA luxe. Utilisables seulement si la marque du prospect les emploie déjà.

**Hiérarchie:** le contraste vient du haut, pas du bas. Titres de section en graisse
500 à 40px plutôt que 800 à 58px. Corps à 16px. Accroches à 21px. Le 11px n'existe
qu'en capitales espacées sur une ligne courte.

---

## Axe 5: le RYTHME

Rejeté explicitement: `.wrap` à 1280px partout, même padding partout, même gap partout.
*« Cette uniformité parfaite est une signature de génération automatique. »*

**Au moins trois largeurs différentes dans la page, chacune justifiable:**
1240 standard · pleine largeur bord à bord · 880 mesure éditoriale · 1440 galerie ·
720 formulaire.

Et une section doit peser plus que les autres, pour que l'œil se pose quelque part.
Des rangées de cartes toutes de même poids, c'est l'équivalent visuel de l'écriture IA.

---

## Axe 6: la COULEUR

- **Un seul accent**, et il ne sert qu'à trois choses: le bouton principal, l'état actif
  ou le survol, un chiffre ou une donnée clé. Jamais sur le corps de texte, jamais sur
  les titres, jamais en décoration.
- **60 / 30 / 10**: fond dominant, surfaces et conteneurs, accent.
- **Deux couleurs prises du logo, et on s'arrête là** dans le héros. Les teintes
  secondaires vivent plus bas dans la page quand elles portent un sens.
- Contraste minimum 4,5:1 en texte courant, 3:1 en grand titre.
- Pas de logo à échantillonner: la palette devient un choix assumé, annoncé à la
  livraison comme le seul point à confirmer avec le propriétaire.

---

## Axe 7: la SIGNATURE, qui EST le métier

Un motif dessiné à la main en SVG, servi en `data:` URI, employé **exactement trois
fois**: filet d'étiquette de section, fond à faible opacité dans le héros, séparateur
de pied de page. Jamais plus, sinon c'est un tic.

Comment le trouver: prends l'outil, la matière, le geste ou la géométrie du métier.

**Déjà servi:** la trace de circuit (électricien) · l'appareillage en panneresse
(maçonnerie) · la rangée de bardeaux (couvreur) · le coup de raclette (nettoyage) ·
la tresse (coiffure) · la rangée de flacons (esthétique) · les cercles concentriques
de visée · le médaillon ovale · le symbole infini tiré de leur propre logo ·
la vitrine en trois panneaux · le champ magenta · trois mots fantômes.

---

## Le cadrage: échelle, rythme, images

Le défaut le plus visible du skill jusqu'ici, dans ses mots: *« il ne cadre pas bien les
écrits, les héros et les images, soit la police est trop grande soit elle est trop petite,
souvent il y a trop d'espace entre deux sections, et tout ça a l'air non intentionnel. »*

La cause n'est pas le goût, c'est l'absence de système. La variation était aléatoire, et
une variation aléatoire se lit comme une erreur. **Le rythme doit être irrégulier mais
réglé:** l'irrégularité vient du choix d'un cran dans une échelle fixe, jamais d'un nombre
improvisé.

### L'échelle typographique

Six crans maximum sur toute la page, pas un de plus. Chaque cran doit porter **au moins
trois usages**, sinon il ne sert à rien et il faut le supprimer.

| Cran | Valeur | Mesure |
|---|---|---|
| h1 | `clamp(30px, 4.4vw, 46px)` | 24 à 34ch |
| h2 | `clamp(25px, 2.6vw, 36px)` | 14 à 20ch |
| h3 | `clamp(18px, 1.4vw, 21px)` | libre |
| accroche | `clamp(17px, 1.5vw, 21px)` | 42 à 56ch |
| corps | `16px` fixe | 60 à 72ch |
| étiquette | `12px` capitales, `letter-spacing:.12em` | ligne courte |

**Quatre règles qui règlent les trois symptômes:**

1. **Toute taille d'affichage passe par `clamp()` à trois valeurs réelles.** Une taille en
   px fixe est la cause directe du « trop grand à 1920 » et du « trop petit à 375 ».
2. **Ce qui empêche un titre d'être trop gros, c'est la mesure en `ch`, pas la taille.**
   Un titre de 46px sur une mesure de 28ch ne peut pas partir en escalier. Précédents:
   Enterprise Spa et Salon Amina, corrigés tous les deux en descendant la taille et en
   ouvrant la mesure.
3. **Le h1 fait deux lignes, trois au maximum, et la ligne la plus courte fait au moins
   40% de la plus longue.** En dessous, c'est un escalier et ça se voit.
4. **Rien sous 16px sauf l'étiquette**, et l'étiquette n'existe qu'en capitales espacées
   sur une ligne courte. Onze pixels en minuscules ne sont pas lisibles.

### Le rythme vertical

Quatre crans, chacun avec un rôle. La variation vient du **choix du cran par section**, et
ce choix s'annonce dans la ligne d'ADN.

| Cran | Valeur | Pour |
|---|---|---|
| respirante | 96 à 128px | les deux ou trois sections qui portent la page |
| standard | 72 à 88px | le tout-venant |
| dense | 40 à 56px | rail, marquee, barre d'arguments, bande de logos |
| collée | 0 | une bande qui touche celle du dessus, volontairement |

**Trois règles:**

1. **Ne jamais empiler `margin-bottom` et `padding-top` entre deux sections.** L'écart
   entre deux sections est **une seule valeur**, portée par le `padding-top` de la section
   du bas. L'empilement est la cause numéro un du « trop d'espace ». Le dernier élément
   d'une section a toujours `margin-bottom:0`.
2. **Une section sur champ de couleur se serre d'un cran** par rapport à une section sur
   fond clair. À rythme égal, un bloc de couleur paraît vide.
3. **À l'intérieur d'une section:** titre vers intro 12 à 16px, intro vers contenu 32 à
   40px, et **une seule valeur de `gap` par grille**.

Une répartition qui marche sur six sections: 1 respirante, 3 standard, 1 dense, 1 collée.
Ce que ça ne doit jamais être: six fois la même valeur.

### Le cadrage des images

1. **Aucune image affichée plus large que sa source.** Le rapport largeur affichée sur
   `naturalWidth` doit rester sous 1,05. Au-delà, ça se voit et ça se lit comme du travail
   bâclé. Trois builds ont livré des images à 1,20x et 1,24x sans que personne le voie.
2. **Un héros pleine largeur exige une source paysage de 1600px ou plus.** Si rien ne
   qualifie, **changer la forme du héros** au lieu d'étirer. Un héros typographique assumé
   vaut mieux qu'une photo floue.
3. **Un cadre photo reçoit un `aspect-ratio`, jamais une `height`**, sauf si le parent a
   une hauteur définie. Un `height:100%` dans une grille en `align-items:center` a déjà
   fait disparaître quatre images d'un coup.
4. **Adapter la taille d'affichage à la résolution de la source.** Un portrait de 199x276
   affiché à 270px est cassé; le même fichier dans un cercle de 104px est net et paraît
   voulu. Rétrécir la case plutôt qu'agrandir le fichier.

### Rien de tout ça ne se juge à l'œil

Les quatorze règles ci-dessus sont mesurables, et aucune n'a jamais été vérifiée
autrement qu'en relisant le code. `scripts/probe.js` les teste toutes dans le panneau,
à chaque largeur. Le lancer avant de livrer, pas après un rejet.

## Le héros converti, en cinq points

1. Un titre qui dit le résultat pour le client, et qui nomme le métier et la ville.
2. Une sous-ligne précise qui dit comment, pas un slogan.
3. Un bouton dont le texte dit l'action réelle (« Obtenir une soumission en 24 h »,
   pas « En savoir plus »).
4. Un ancrage visuel: leur vraie photo, leur vrai logo, ou une composition typographique
   assumée. Jamais un placeholder ici.
5. Un signal de confiance: note Google, licence RBQ, adresse, un vrai avis. Un fait
   vérifiable vaut mille fois un pourcentage rond.

---

## La liste de rejet

Ce qui trahit une génération automatique, dans ses mots:

- Titre en dégradé ou en effet miroitant.
- Rangées de cartes de poids égal, aucune hiérarchie.
- Uniformité parfaite des espacements et des largeurs.
- Une échelle typographique dont un seul cran porte tout le contenu.
- Le 11px en minuscules.
- L'italique dorée répétée. Un seul mot en serif italique par page, dans le h1.
- Un mot fantôme qui répète le titre. Le fantôme porte la catégorie, le titre porte la
  promesse, et aucun mot ne doit apparaître dans les deux.
- Un centrage isolé dans une section sur trois. Seul le héros peut être centré.
- La pastille d'accroche dans le héros.
- Trois appels à l'action dans le héros.
- Un écran d'introduction noir.
- Un décalage arbitraire. Un décalage n'est perçu comme voulu que s'il obéit à une
  règle visible, donc des multiples d'une seule unité.
- Le tiret décoratif en `::before` sur une étiquette de section, lu comme un tiret
  cadratin.
- Le blocage du défilement.
- Trois cartes d'avis vides marquées « Exemple ». Quand le prospect n'a aucun avis,
  une section équipe nommant les gens est plus honnête et plus différenciante.

---

## Les sites de référence qu'il envoie

Trois façons d'exploiter une URL, selon ce qu'on veut en tirer:

| On veut | Comment | Coût |
|---|---|---|
| le mouvement | `python scripts/inspect_motion.py <url>`, puis recette dans `MOTION.md` | bas |
| couleurs, typo, échelle | fetch de leur CSS, lecture des variables et des `font-family` | bas |
| mise en page, rythme, allure | capture qu'il envoie, ou panneau navigateur sur l'URL en direct | moyen |

**Jamais embarquer leur JavaScript.** Il ne nous appartient pas, et une librairie CDN
casse le fichier unique hors ligne.

**Une référence renvoyée deux fois est un brief, pas une suggestion.**

### Quand il fournit une référence précise pour ce build

C'est le chemin le plus rapide et le plus fiable du skill. Une image qu'il a cherchée
lui-même vaut mieux que n'importe quelle déduction.

1. **La référence court-circuite l'algorithme.** Le monde qu'elle porte est retenu
   directement, la question de direction ne se pose pas.
2. **Prendre les dispositifs, pas la palette.** La palette reste celle du logo du
   prospect. Une planche de référence dit comment la page est bâtie, pas de quelle
   couleur elle est. Reprendre les deux, c'est livrer une copie de la planche.
3. **Nommer les trois ou quatre dispositifs repris** dans le message de livraison, pour
   qu'il vérifie que c'est bien ce qu'il avait vu dedans.
4. **La règle du non-répété tient toujours** sur héros, étiquette et typo. Deux prospects
   sur la même référence doivent quand même donner deux pages différentes.

### Le catalogue

**Douze planches Pinterest, distillées dans `inspiration/PINTEREST.md`.** Ce fichier
donne pour chacune les dispositifs concrets à reprendre. Le lire à l'étape design,
ouvrir les images seulement si la description ne suffit pas.

| Réf | Catégorie | Monde rattaché |
|---|---|---|
| A1 Amalfi Skincare | soin | éditorial papier |
| A2 SKIN by Jasmine | soin | photo pleine, texte minuscule |
| A3 Luna & Sage | soin | herbier clinique |
| A4 HURR | soin | artisanat imprimé |
| A5 AURA Salon | soin, coiffure | boutique matiériste |
| B1 Tristero | tatouage, studio | vitrine nocturne |
| B2 Tattoo Anatomy | tatouage, studio | vitrine nocturne |
| C1 The Agency | professionnel | vitrine nocturne, variante claire |
| C2 Maddie Fox | professionnel | éditorial papier |
| D1 Roofing ambre | chantier | signalétique industrielle, sombre |
| D2 Sphera&Live | chantier, architecture | atelier suisse, sombre |
| D3 Fieldo | immobilier | atelier suisse |

**Sites inspectés pour le mouvement**, recettes dans `MOTION.md`: venetianspa.ca ·
truekindskincare.com · racon360.com · spenceltd.co.uk · jannataresort.com · fluid.glass ·
luminouslabs.health · plumber-128.webflow.io · ristudio.in · rierastudio.com ·
vicpark.com · clinique7.com.

### Trois trous dans le catalogue

Aucune référence pour: **table** (restaurant, boulangerie, café), **détail**
(boutique, fleuriste) et **entretien** (nettoyage, déménagement, paysagement). Trois des
huit familles de métier n'ont donc aucune planche. Quand un prospect tombe dans l'une
d'elles, l'algorithme travaille seul et le risque d'itération monte.

**Le catalogue étendu donne un point de départ pour ces trois familles.** Ce ne sont
pas des planches, il n'y a aucune image derrière, seulement une palette et un rythme.
Mais c'est mieux que l'algorithme seul:

| Famille sans planche | Mondes étendus qui la couvrent |
|---|---|
| table | `cafe`, `warm-editorial`, `paper`, `vintage`, `storytelling`, `artistic` |
| détail | `friendly`, `colorful`, `bento`, `clean`, `clay`, `creative` |
| entretien | `spacious`, `minimal`, `flat`, `professional`, `corporate`, `application` |

Quand un de ces mondes sert et que le résultat tient, le noter dans `BUILT.tsv` comme
n'importe quel autre. Une planche Pinterest reste le vrai correctif, ceci est un
pansement.
