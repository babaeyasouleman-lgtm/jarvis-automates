# Technique. Lu à la demande, jamais par défaut.

Recettes payées en temps réel sur des builds passés. Ne rien lire ici tant qu'on n'a pas
le problème correspondant.

## Récupérer les photos d'un prospect

| Situation | Commande |
|---|---|
| WordPress | leur `wp-content/uploads` héberge souvent des dizaines de photos réelles, y compris des exports Instagram |
| Shopify | `https://LEBOUTIQUE.myshopify.com/products.json?limit=250` donne tout le catalogue: prix, collections, images CDN |
| Site bloqué | `https://archive.org/wayback/available?url=DOMAIN` puis `https://web.archive.org/cdx/search/cdx?url=DOMAIN%2Fwp-content%2Fuploads%2F*&output=text&fl=timestamp,original,statuscode&filter=statuscode:200&collapse=urlkey&limit=200` |
| Brief «montrer leurs réalisations» | crawler **toutes** les sous-pages de galerie. L'accueil d'Envert montrait 3 diapos de gabarit, les 12 sous-pages contenaient 94 vraies photos. C'est la seule exception à la règle du budget qui interdit de crawler. |

**Trier un gros lot coûte une seule lecture d'image, pas quarante:** composer une
planche-contact et la regarder.

```bash
ffmpeg -y -v error -i SRC -vf "scale=260:390:force_original_aspect_ratio=decrease,pad=260:390:(ow-iw)/2:(oh-ih)/2:color=white" NN.png
ffmpeg -y -v error -i "%02d.png" -vf "tile=5x2" sheet.png
```

`tile` ne monte **qu'une seule vignette** si les sources n'ont pas toutes la même taille:
normaliser d'abord en `scale`+`pad`, mosaïque en seconde passe. `drawtext` est indisponible
ici, fontconfig n'a pas de fichier de configuration et ffmpeg segfault.

## Photos libres de droits

- **Openverse répond sans clé:** `api.openverse.org/v1/images/?q=...&license=cc0&size=large`.
  Filtrer sur **cc0**, qui autorise le commercial sans attribution.
- Ajouter `source=stocksnap` évite entièrement rawpixel et ses filigranes.
- **Le CDN StockSnap renvoie une page HTML de 4570 octets sans User-Agent de navigateur.**
  Il faut `-A` plus `-H "Referer: https://stocksnap.io/"`. Vérifier la signature du fichier
  avant de faire la planche-contact, sinon dix fichiers identiques de 4,5 Ko passent pour
  des images.
- **Plafond StockSnap: 960px, sans contournement.** Toutes les variantes de largeur et le
  chemin `original/` renvoient 404. Donc **jamais de héros pleine largeur sur une image
  StockSnap**: sur son écran de 1356px cela fait déjà 1,4x.
- **Unsplash:** `images.unsplash.com/photo-<id>?w=1500&q=80` passe en curl simple, licence
  commerciale sans attribution. Les pages de recherche et `napi` sont bloquées, donc les
  identifiants ne se récoltent pas. Méthode: sonder un lot d'identifiants candidats, garder
  les 200.
- **Pexels** est rendu en JS et ne renvoie rien. **Wikimedia** refuse un User-Agent générique,
  il en faut un descriptif sinon le fichier revient en page d'erreur de 1966 octets.
- **Rechercher des intérieurs architecturaux, pas du médical.**

## Images générées

- **Le négatif compte autant que la description.** Bannir nommément ce qui n'est pas voulu.
  Sans négatif, tout modèle redescend vers le cliché chaleureux: guirlandes, lanternes,
  bougies, feu, lumière dorée.
- **Deux lignes de négatif obligatoires sur toute image d'équipement:** aucun texte, logo,
  étiquette ni plaque de série (sinon le modèle invente des marques et pose un faux logo sur
  le site d'un client), et aucune rouille, moisissure ni pièce cassée.
- **Imposer la composition:** sujet dans le tiers droit, moitié gauche vide pour le titre.
- **La pastille IA se cadre hors champ, elle ne se retouche pas.** Une retouche par recopie
  de pixels laisse un fantôme.
- **La localiser par balayage de luminance ne marche que sur fond sombre.** Sur une serviette
  crème, un ciel ou de l'herbe éclairée, le pixel le plus lumineux est le décor. Méthode
  fiable dans tous les cas: `crop` le coin, `scale=2x`, regarder une planche de cinq images,
  la pastille saute aux yeux. Positions observées: Gemini vers (1805, 1795) sur 2048x2048,
  Veo à (1160, 599) rayon 23px sur 1280x720.
- **Garder la pleine hauteur au recadrage.** Le héros est en `object-fit:cover`, le navigateur
  recadre déjà: livrer 1120x720 plutôt que 1120x630 donne 90 lignes gratuites.

## Vidéo

- **Une sortie Veo dérive sur la fin: la couper, jamais l'accélérer.** Ne jamais modifier le
  tempo d'un plan filmé pour tenir un budget de poids. Le poids se règle au recadrage, à la
  durée et au crf.
- **crf 23, environ 1,8 Mbit/s.** Le crf 33 donnait 520 kbit/s sur un plan de drone, très
  en dessous. **Le plafond de 1,5 Mo vaut pour des images, pas pour un héros vidéo:** 2,40 Mo
  est passé sans remarque et reste loin des limites de courriel.

## Logos

- Les logos exportés de WordPress sont souvent énormes avec un immense padding transparent.
  Recadrer sur la boîte englobante des pixels non transparents avant de s'en servir.
  **Il n'existe pas de `logo_prep.ps1`**, malgré ce que l'ancien SKILL.md affirmait: le
  recadrage se fait à la main avec System.Drawing ou ffmpeg (`cropdetect`).
- **Échantillonner la couleur de marque dans le logo et l'utiliser**, elle bat toute palette
  qu'on choisirait. Voir dans `RULES.md` les deux cas où elle ne gagne pas.
- Parfois le logo **est** la réponse: le «logo» de l'ambassade du Gabon était le drapeau, qui
  livrait l'identité tricolore complète en un fichier.
- **Un texte incrusté dans une image** reste dans une seule langue quand la bascule joue, et
  bloque l'overlay d'un titre. Le recadrer, ou employer l'image ailleurs.

## Dimensions sans ouvrir les fichiers

```powershell
Add-Type -AssemblyName System.Drawing
Get-ChildItem assets\* -Include *.png,*.jpg | ForEach-Object {
  $i=[System.Drawing.Image]::FromFile($_.FullName)
  "{0} {1}x{2} {3}" -f $_.Name,$i.Width,$i.Height,$i.PixelFormat; $i.Dispose() }
```

## Poids du fichier

- `scripts/optimize.ps1` **seulement si** les actifs dépassent environ 1 Mo. Il utilise
  System.Drawing parce que Pillow n'est pas installé et ne doit pas l'être.
- Passer les images de grand affichage à `-HeroPattern` en **une seule chaîne séparée par des
  virgules**, pas un tableau PowerShell.
- **Convertir en JPEG les PNG photographiques opaques est le plus gros gain disponible:**
  1,7 Mo à 228 Ko sur le build Gabon.

## Retrouver un fichier qu'il vient d'enregistrer

`find -newermt` limité à Downloads, Bureau et Images a déjà échoué alors que le fichier y
était. Ce qui marche: `Get-ChildItem -Recurse` sur Downloads, OneDrive, Pictures, Documents
et Desktop, trié par `LastWriteTime` décroissant, quinze premiers. Les fichiers Gemini
gardent leur nom `Gemini_Generated_Image_*.png`.

## Pièges CSS payés en temps réel

- **`position:sticky` doit venir en premier parmi ses frères.** Un panneau collant placé
  après les espaceurs reste échoué en fin de piste et la section rend une feuille blanche
  de 2500px.
- **`overflow:hidden` sur un ancêtre tue le sticky.** Utiliser **`overflow:clip`**, qui
  rogne sans créer de conteneur de défilement.
- **L'état final d'une animation écrase un transform statique.** Ajouter `transform:scale(1.18)`
  à une image qui a déjà `@keyframes ... to{transform:scale(1)}` ne fait rien. Modifier aussi
  la valeur de fin du keyframe et l'override `prefers-reduced-motion`.
- **`height:100%` exige un parent à hauteur définie.** Dans une grille en `align-items:center`,
  cela a réduit le cadre à 0px et fait disparaître quatre images. Le parent a besoin de
  `align-self:stretch` plus `display:flex;flex-direction:column;min-height:0`.
- **`<figure>` garde 40px de marge à gauche et à droite** dans la feuille du navigateur.
  Dans une grille, chaque vignette perd donc 80px de large: des colonnes de 222px ne
  donnaient que 142px d'image. Poser `figure{margin:0}` dans la remise à zéro, toujours.
  Le défaut est passé inaperçu deux builds de suite parce que le contrôle ne cherchait que
  l'agrandissement, jamais l'écart entre la colonne et son contenu.
- **Ne jamais poser un raccourci `padding` sur un élément qui porte déjà `.wrap`.** Deux
  sélecteurs à une classe, le second gagne, et le raccourci remet l'horizontal à zéro. Le
  titre du héros s'est retrouvé 30px à gauche du logo de la nav.
- **Les deux termes d'un garde-fou de collision doivent avoir la même base.**
  `calc(100% - 45vw)` où `100%` est plafonné à 1240 pendant que `45vw` continue de croître
  faisait tomber la colonne à 316px sur 1920. Remplacer par `min(620px, calc(53vw - 90px))`.
- **Un élément posé après le `<script>` qui le cherche renvoie `null` et tue tout le reste du
  script.** Une barre collante mobile a fait disparaître 29 images d'un coup, filet de sécurité
  compris. Placer les éléments fixes avant le script.
- **La règle qui RÉVÈLE doit être scopée comme celle qui CACHE, sinon elle perd.**
  `html.js .rv{opacity:0}` vaut **(0,2,1)** et `.rv.in{opacity:1}` vaut **(0,2,0)**: le
  masquage gagne et **tout le site sous le héros reste invisible dans TOUS les
  navigateurs**. Écrire `html.js .rv.in`, soit (0,3,1). Constaté sur Venturia le
  2026-08-20, signalé par lui: « pourquoi le reste du site web est vide ». Le piège est
  sournois parce que la classe `.in` EST bien posée: la mécanique JS a l'air de marcher.
  **Diagnostic en une ligne**, à refaire avant de soupçonner le JS: parcourir
  `document.styleSheets`, garder les règles qui `matches()` la cible, et comparer les
  spécificités. Ne jamais conclure « les transitions sont gelées » sans avoir vérifié la
  cascade d'abord: neutraliser la transition et relire l'opacité départage les deux causes.
- **Un lecteur qui ne composite pas ne démarre jamais une transition CSS**, donc un
  élément qui porte `.in` et dont la règle gagnante dit `opacity:1` reste quand même à 0.
  C'est une deuxième cause, distincte de la spécificité. Filet: un chien de garde à 3 s
  qui relit l'état réel et pose `html.notrans`, lequel force `transition:none`,
  `opacity:1` et `transform:none`. 3 s couvre la pire cascade (1,4 s de transition plus
  0,7 s de décalage en cascade).
- **`@font-face` base64 plus un `<link>` Google Fonts = double téléchargement.** Garder le
  base64, supprimer les `<link>`.
- **`font-weight:100 900` dans `@font-face` n'est pas un bug**, c'est l'axe d'une police
  variable.
- **Avec `gap` sur une piste de marquee, `translateX(-50%)` rate d'un intervalle.** Mettre
  l'écart en `padding-right` sur chaque tuile, piste sans `gap`.
- **Recadrer une photo en CSS est de l'arithmétique.** Avec `object-fit:cover`, la fenêtre
  horizontale vaut `1/s` de la source, centrée sur `transform-origin`. Calculer avant de
  promettre de cacher quelque chose, et dire quand deux objets gênants sont sur des bords
  opposés: aucune fenêtre ne peut exclure les deux sans un grossissement visible.

## Le panneau de prévisualisation

- **`javascript_tool` est l'outil de vérification le plus fiable du skill.**
  `getBoundingClientRect`, `getComputedStyle` et le canvas renvoient des valeurs vraies.
- **`resize_window` ne s'applique pas toujours.** Toujours lire `innerWidth` en retour.
- **Le panneau ne décode aucune image** quand la page est servie en `data:`: `naturalWidth`
  vaut 0 partout et les captures ne montrent que typographie, mise en page et couleurs.
  Servir le `index.html` avec `assets/` pour mesurer les images.
- **Les captures marchent parfois seulement.** Quand elles marchent, photographier en bandes
  en décalant le document (`body.style.position='relative'` puis `top` négatif calculé sur le
  rect courant), jamais avec `scrollTo`.
- **Les révélations cachent tout à la capture.** Forcer avant:
  `document.querySelectorAll('.rv,.rv-h').forEach(el => el.classList.add('in'))`.
- **Un titre assemblé caractère par caractère ne se photographie pas.** Constaté deux fois
  sur Elite Beauty Lab, 2026-08-12: les `span.ch` mesurent tous `opacity:1` et le h1 a un
  rect correct, mais la capture rend la zone vide. Le panneau ne compose pas cette couche.
  Neutraliser avant de photographier, c'est un diagnostic et non une modification du
  fichier: `document.querySelectorAll('#h1 .ch').forEach(s=>{s.style.transition='none';
  s.style.transform='none';s.style.opacity='1';s.style.willChange='auto'})`.
- **`inspect_motion.py` sans `--deep` ne rend rien sur un WordPress.** Toujours refaire la
  passe profonde.
