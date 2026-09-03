# Règles. Lues à chaque build.

Remplace `PREFERENCES.md`, conservé en archive. Chaque ligne est une règle applicable.
Quand une règle en a remplacé une autre, seule la version finale figure ici.

**Discipline d'écriture de ce fichier: une préférence nouvelle remplace une ligne ou en
ajoute une. Jamais un paragraphe.** C'est ce qui a fait passer l'ancien fichier à 819 lignes.

---

## Identité et données du prospect

- Avant d'écrire quoi que ce soit sur un prospect sans URL, **chercher son numéro de
  téléphone**. Il résout l'entreprise en une requête. Nom et numéro qui divergent: demander
  avant de construire. (Divine MedSpa était Lemonade Beauty.)
- Garder le nom de l'entreprise dans **une seule clé i18n**, pour le remplacer en une ligne.
- **N'inventer aucun nombre.** Ni licence, ni téléphone, ni année de fondation, ni «500+
  projets», ni statistique ronde. Une maquette n'a presque pas besoin de chiffres.
- **Aucune année de fondation sans confirmation**, et pas de «récemment établie».
- **Aucune mention non vérifiée**, même plausible («salle d'exposition» a été retirée).
- Vérifier un chiffre dans le **HTML brut**, pas dans le texte rendu. Ouimette avait deux
  numéros de licence RBQ dont un dans un commentaire HTML.
- **Un fait vérifiable bat un pourcentage rond.** Licence RBQ, numéro de kiosque, adresse.
- Une section équipe **sans noms fournis se construit sans aucun nom**. Rôles génériques,
  portraits en aplat. Jamais un prénom plausible.
- Un changement d'équipe se traite **par grep sur chaque nom** dans le fichier livré, pas de
  mémoire. Les noms vivent dans le HTML, dans le dictionnaire de l'autre langue et parfois
  dans un nom de fichier.
- **Quand le brief vient du propriétaire en personne, il écrase tout ce qui a été déduit du
  site.** Consigner le brief dans un fichier du dossier prospect avant de construire: ce qui
  est confirmé, ce qui est à confirmer, ce qui devient inutilisable.

## Avis Google

- **Section d'avis sur tous les sites.** Règle permanente.
- **Ne jamais mentionner le nombre d'avis. Nulle part.** Ni pastille, ni chiffre, ni mot, ni
  «deux», ni «plus de», ni dans un titre de section. La note et les étoiles suffisent.
- **La note apparaît une seule fois**, dans la section des avis. Jamais aussi dans le héros.
- Un vrai avis **reste dans sa langue** et n'est jamais traduit, et **cela ne se commente pas
  sur la page**. Le nom et la mention «Avis Google» suffisent.
- **Les avis défilent, ils ne s'alignent pas.** Rail horizontal, flèches, `scroll-snap`,
  retour au début, avance automatique qui s'arrête au survol. La carte de note ouvre le rail.
- **Un rail court et vrai vaut mieux qu'un rail plein et faux.** Ne pas compléter.
- **Zéro avis n'est pas un trou, c'est un argument de vente:** proposer un dispositif de
  collecte d'avis, c'est du travail facturable en plus.
- **Zéro avis: préférer une section équipe nommée à trois cartes vides marquées «Exemple».**
  Trois cartes vides sont l'aveu qu'il n'y a pas de contenu.

## Images et photographie

- **Les vraies photos du prospect passent avant tout**, quand elles sont présentables. Une
  photo authentique mais mauvaise vaut moins qu'une photo libre de droits correcte.
- **Aucune image ne doit apparaître deux fois sur la page.** C'est le signal le plus visible
  d'une démo vide. Une photo, un seul emploi.
- **Photos de banque: en ambiance seulement, jamais présentées comme leur travail**, et
  uniquement sous licence vérifiée. La section réalisations est soit leurs photos, soit des
  emplacements réservés.
- **Jamais de visage de banque ni de visage généré dans une section équipe.** Cela ferait
  passer un inconnu pour son employé. Vaut aussi pour les images générées.
- **Aucune photo de personne générée par IA** sur ces maquettes.
- **Ne pas réutiliser les photos d'une entreprise fermée qui a précédé le prospect**, et
  surtout pas un portrait. Google garde les avis à travers un changement de nom et une vente.
- **Une photo de héros générée se RETOURNE avant tout le reste si sa source de lumière tombe
  du côté du texte.** Se décide par la mesure, pas à l'œil: luminance moyenne du tiers gauche
  contre le tiers droit. Sur Les Francs Planchers, 110,7 contre 151,9 après le miroir. Un
  plancher n'a ni texte ni visage, le miroir ne coûte rien.
- **Une photo de héros générée n'est pas leur photo: elle prend la bande de légende**, comme
  une photo de banque, et cette bande se formule en argument de vente et non en excuse.
- **Aucune photo du prospect à 1600px: lui proposer de générer le fond du héros sur Gemini,
  avant de changer la forme du héros.** Demandé le 2026-08-24 sur KDM, dont la plus grande
  photo faisait 960x480. La couche photo se construit alors comme **une seule règle CSS**
  (`.hero .shot`, `background-image`) pour que l'image se pose en une ligne quand elle arrive,
  et le reste de la page se bâtit sans attendre.
- **Emplacements réservés: sous la ligne de flottaison, jamais dans le héros**, l'air voulu
  (panneau de marque, glyphe d'appareil, libellé court), jamais l'air cassé, et traduits.
- **Un seul emplacement réservé de type reel par page**, et il saute s'il coûte un bloc entier.
- Si la photo du héros est du stock, **garder et poser une bande de légende sombre** en bas:
  «Photo à remplacer, séance photo professionnelle incluse».
- **Aucun certificat ni diplôme scanné.** L'accréditation peut rester en texte.
- **Un voile sur une photo plafonne à .55.** Au-delà, la photo ne compte plus comme une photo;
  protéger le texte par une ombre portée plutôt qu'en assombrissant toute l'image.
- Signaler les photos de banque à la livraison: un nom de fichier générique est un identifiant
  de banque d'images et la licence appartient à qui l'a achetée.

## Couleur

- **Échantillonner le logo donne la teinte, pas la luminosité ni la saturation d'un fond plein
  écran.** Un teal cyan vif étalé sur un héros a été rejeté («ça fait mal aux yeux»).
- **Quand le métier a une couleur naturelle évidente, elle bat l'échantillonnage du logo.**
  L'eau veut du bleu, même si le logo est rose.
- **Le pied de page prend la couleur du logo**, pas un neutre.
- **Ni blanc ni crème en fond de page unique.** La couleur vient de **l'alternance de champs
  plats**, pas du canevas.
- **Pas de noir.** Grep `#000` et `#111` avant de livrer. Un gris très foncé teinté à la place.

## Typographie et échelle

- **Plafond: h1 autour de 46px, h2 autour de 34px, corps 16px.** Il lit une typo surdimensionnée
  comme non fini, pas comme audacieux. Un h1 à 116px a été rejeté.
- Le détail complet de l'échelle et du rythme est dans `DIRECTIONS.md`, section «cadrage».
- **Le serif d'affichage n'est pas interdit.** Ce qui est interdit, c'est le combo AI luxury:
  serif léger géant plus crème plus champagne plus nav foncée. Un serif dense sur une page à
  blocs colorés passe.
- **Un seul mot ou groupe en serif italique par page**, dans le h1 du héros. Répété, c'est un tic.
- **Le nom de la ville détaché du titre**, en serif italique léger et dans la couleur de marque.
  Le reste du titre ne prend aucune couleur.
- **Un énoncé centré sur plusieurs lignes se lit comme «pas uniforme»**, dans une SECTION.
  Deux colonnes, texte aligné à gauche, image à droite.
- **Sur un héros en photo pleine largeur, l'énoncé se centre**, et il le demande sans qu'on lui
  propose: «le 1 avec une photo en fond dans le hero principal et le texte centré» le
  2026-08-24 sur KDM, puis «centre le titre» le même jour sur Les Francs Planchers. Le voile
  directionnel n'a alors plus de sens: il passe symétrique, et l'écran local devient un
  radial centré sous le seul énoncé.

## Structure d'une maquette

- **5 à 7 sections. 40 à 70 chaînes traduisibles. 3 à 5 images. Un titre et une ou deux phrases
  par section.** Le build Gabon en a eu 173 et a pris 45 minutes.
- Là où leur vraie page a un mur de contenu, montrer **la forme** de la section et noter que le
  détail vient de leur matériel existant.
- **Rien qui précède le titre du héros.** Pas de pastille d'accroche, pas de bande de faits
  juste dessous. Ce qui précède le titre vole la place de ce qui compte.
  **Y compris le nom de la ville ou de la région en petites capitales espacées.** Rappelé le
  2026-08-30 sur le Centre Islamique de l'Outaouais: *« j'aime pas le Gatineau Outaouais en
  haut en bordeaux, ne mets jamais ça sur les sites web. »* La ville a une seule place
  autorisée, celle de la règle plus haut: détachée DANS le titre, en serif italique léger et
  dans la couleur de marque. Jamais au-dessus, jamais en bordeaux ou en brique.
- **Le héros prend tout l'écran par défaut**, en `calc(100svh - hauteur de barre)`. Demandé le
  2026-08-13. Plein écran ne veut pas dire photo pleine largeur: si cette forme a servi dans les
  cinq derniers builds, c'est la forme retenue qui s'étire à 100svh, pas la forme qui change.
- **Deux appels à l'action maximum dans le héros.** Trois, c'est un de trop.
- **Rien par-dessus la photo du héros, à part le voile et l'écran du texte.** «Retire les traits
  qui sont au-dessus de l'image», le 2026-08-24. Le motif de signature en fond de héros, prévu
  comme un des trois emplois, est le premier à sauter: il reste la bande de section et le
  séparateur de pied de page, et la signature vit très bien à deux emplois.
- **Le téléphone dans l'en-tête pour un métier de chantier**, pas un bouton de formulaire. Sur
  mobile, c'est le bouton Soumission qui disparaît, jamais le téléphone.
- **La bascule de langue va dans la barre collante**, jamais dans une rangée qui défile. C'est
  l'argument qu'il démontre en direct, elle doit rester atteignable partout.
- **Une rangée utilitaire ne répète aucun lien de la nav.** Téléphone et raccourcis, rien d'autre.
- **Pas de badge «ouvert maintenant» par défaut.** Seulement si les heures sont l'argument.
- **Pas de badge de remplissage.** S'il ne dit rien sur quoi le visiteur agirait, il saute.
- **Un prospect qui vend des produits a droit à une section boutique entière**, avec ses vrais
  articles, ses vrais prix et un panier de démonstration dont le compteur monte dans la barre.
  Demandé le 2026-08-27 sur La KouPol v3: *« il n'y a pas leur boutique parce qu'ils vendent des
  produits »*. Les prix suivent la langue **par un attribut, pas par une clé i18n**: quinze produits
  en clés feraient sauter le plafond de 70.
- **Une liste de prix se présente en rail de cartes qui défilent**, pas en menu de restaurant.
- **Un ruban ondulé se génère depuis un sinus, jamais avec des points de contrôle Bézier.**
  Une Bézier ne tire la courbe qu'aux trois quarts de ses contrôles: sur Cléopâtre, des
  contrôles poussés au bord de la boîte ne donnaient que 27% d'amplitude et il l'a vu tout
  de suite, « pas assez ondulé ». Échantillonner le sinus en polyligne et décaler la bande
  perpendiculairement, par la dérivée.
- **Avant et après veut dire un curseur qui glisse**, pas deux cases côte à côte. Un
  `input[type=range]` transparent pilotant un `clip-path:inset()`.
- **Pas de faux avant/après.** Supprimer la section entière plutôt que de la simuler.
- **Les réalisations défilent en continu** (marquee), les avis avancent par flèches. Le rail à
  flèches convient aux avis, pas aux photos.
- **Un prix, un classement ou une prime de référence se montre en haut du site**, en bande promo
  défilante au-dessus de la barre collante, pas seulement dans le héros.
- **Sauf quand il vend la calculatrice à part: alors les prix sont préétablis.** Demandé le
  2026-08-21: *« je veux que les prix soient préétablis par les prix du marché [...] une vraie
  calculatrice de soumission qui vaut 2000$ »*. Les montants sont alors des **fourchettes
  publiées, annoncées sur la page comme des moyennes de marché et non comme ses prix**, les
  champs restent éditables, et deux facteurs d'ajustement au maximum, affichés en clair.
- Un champ **vide et éditable bat un montant inventé** sur une calculatrice ou une grille de
  prix, et le remplir en direct devant le propriétaire est le moment de démo de la maquette.

## Écriture

- **Zéro tiret cadratin (U+2014).** Dans la page et dans le chat. Virgules, points, ou deux-points
  avant une liste.
- **Bannis:** seamless, robust, leverage, elevate, transformative, streamline, unlock, empower,
  cutting-edge, harness, delve.
- **Pas de slogan parallèle creux.** Nommer la chose concrète: «Panel upgrades, service work and
  new builds», pas «Real projects, real results».
- **Aucune note éditoriale sur la page.** Pas de «Mockup from their website», pas de commentaire
  sur ce qui manque. Les réserves vont dans le message de chat. Seule exception qui reste: le
  formulaire dit «démonstration, rien n'a été envoyé».
- **Français canadien:** soumission, courriel, main-d'œuvre, territoire desservi.
- **Un prospect dont le site est tenu par un proche se gagne sans critiquer le site actuel.**
  Aucune comparaison, ni sur la page ni dans le message au propriétaire.

## Langue

- **Bilingue toujours**, la bascule est l'argument de vente.
- **Quand il demande une version claire ET une version sombre, les deux sont dans le même
  fichier**, basculées par un petit bouton dans la barre collante à côté du FR/EN, et l'état
  retenu en `localStorage`. Le champ sombre du héros reste identique dans les deux versions:
  ce n'est pas un thème, c'est un dispositif.
- **La langue par défaut suit leur marché**, pas une règle fixe. Site anglais à Ottawa: anglais.
  Site en français seulement et propriétaire francophone: français. Confirmer à la livraison.

## Marques S-WEB Agency, sur chaque build

1. **Filigrane diagonal en tuiles** sur toute la page. Superposition fixe, `pointer-events:none`,
   SVG en `data:` URI répétant «S-WEB AGENCY» à environ **0.075** de `fill-opacity`. Échapper `#`
   en `%23` dans l'URI, sinon la couleur échoue en silence.
2. **Badge fixe en bas à droite**, petites capitales «S-WEB Agency». Il survit aux captures.
3. **Ligne de propriété dans le pied de page**, traduite: conçu et réalisé par S-WEB Agency,
   propriété exclusive, fourni pour présentation, aucun droit d'usage, de reproduction, de
   modification ni de publication sans entente écrite.

Plus deux dissuasions faibles, à décrire honnêtement comme telles: `preventDefault` sur
`contextmenu` au-dessus des images et `dragstart` bloqué sur chaque `img`. Le filigrane est
la vraie protection.

## Méthode de travail, à respecter sans qu'il la redemande

- **Un prospect qui ne veut pas de site se travaille par l'audit et l'automatisation, pas par la maquette.** Demandé le 2026-08-20 sur Venturia: *« Ce prospect n'avait pas l'air de vouloir un site web donc je veux profiter pour offrir autre chose. »* Le livrable devient un document en huit parties, audit mesuré, plan en trois vagues, fiches d'automatisation chiffrées en heures, questions de découverte et table douleur vers offre. La planche se livre quand même, en second, comme levier.
- **La planche à trois bandes se fait TOUJOURS, et avant qu'il choisisse la direction.** Elle ne
  se saute jamais sous prétexte qu'il a déjà répondu à la question de direction: répondre à une
  option décrite en mots ne remplace pas voir trois haut de page. Demandé le 2026-08-13.
- **Un curseur en forme d'outil pointe vers le haut à gauche, la pointe exactement sous le
  pointeur.** Outil dessiné vers le haut avec la pointe à l'origine, puis `rotate(-38)`. Corps
  vers le bas à droite. Une pointe qui tombe sous le pointeur se lit « à l'envers ».
- **Aucune réécriture globale par regex ou remplacement sur tout le document. Jamais.** Chaque
  changement vise une chaîne unique. (Un `[^;}]+` sans terminateur a avalé cinq sections en
  silence sur TOP Construction.) Si un remplacement en masse est inévitable, le borner au bloc
  `<style>` et interdire `;`, `}`, `{`, `:`, `"` et le saut de ligne dans la valeur.
- **Compter `<section>`, `<div>` et `<figure>` avant et après.** Annoncer l'écart attendu à voix
  haute avant d'éditer. **Si un compte ne correspond pas, ARRÊTER et le signaler**, ne pas
  tenter de réparer.
- **Ne faire QUE ce que la passe demande.** Aucune amélioration spontanée, aucun refactoring.
- **Signaler les contradictions plutôt que de trancher en silence.** Ses consignes décrivent
  parfois un état du fichier déjà dépassé. Dire ce qu'on observe, appliquer l'intention,
  expliquer l'écart.
- **Signaler aussi ce qu'on n'a pas pu faire**, avec la raison chiffrée et l'option.
- **Terminer par un compte rendu court:** ce qui a changé ligne par ligne, et ce qui n'a pas pu.
- **Poser les questions aussi en texte simple dans le chat**, pas seulement par le panneau. Le
  panneau a déjà échoué en silence en renvoyant «pas de réponse» sans jamais l'atteindre.
- **Un PDF se vérifie en le RENDANT, pas en extrayant son texte.** Les polices embarquées
  sont des sous-ensembles à encodage CID, donc aucune chaîne ASCII n'en sort. `pip install
  pypdfium2` puis `PdfDocument(f)[0].render(scale=1.6).to_pil()`.
- **`--print-to-pdf` écrit le fichier puis ne rend pas la main.** La commande expire alors que
  le PDF est bon. Lancer en arrière-plan, attendre, puis `taskkill //F //IM chrome.exe`.
- **RENDRE la page avant de la livrer, pas seulement la mesurer.** Chrome en ligne de
  commande: `chrome.exe --headless=new --disable-gpu --hide-scrollbars`
  `--virtual-time-budget=9000 --window-size=L,H --screenshot=CHEMIN URL`. Le chemin de
  sortie doit être en forme Windows, sinon rien n'est écrit et aucune erreur ne sort.
  Pour voir les sections épinglées, servir une **copie** avec un `<style>` qui déplie
  `sticky` et `absolute`: une fenêtre haute ne montre que le héros, qui fait `100svh`.
- **Compter les `/*` et les `*/` après toute insertion de bloc CSS.** Sur SLGN, un bloc
  inséré s'est terminé par un en-tête de commentaire sans `*/`, ce qui a avalé les deux
  règles suivantes: **le filigrane et le badge S-WEB étaient morts dans un fichier livré**.
  Aucune sonde de contraste, de cran, de débordement ou de cible ne peut voir ça.
- **Chrome headless impose une largeur de fenêtre minimale de 500px sur Windows.**
  `--window-size=390` donne un viewport CSS de 500 et une capture rognée à 390, ce qui
  simule un débordement horizontal inexistant. Vérifier en injectant `clientWidth`.
- **`text-wrap:balance` sur h1 et h2** règle l'escalier à toutes les largeurs sans
  toucher au texte ni à la mesure en `ch`. À essayer avant de réécrire un titre.
- **Une fourchette de prix se resserre en POSITIONNANT une fenêtre dans la bande de
  marché, pas en la multipliant.** Un multiplicateur conserve le rapport haut/bas du
  marché (2,5x à 4,2x); une fenêtre de 18% placée par les réponses du client tombe
  entre 1,1x et 1,6x sans jamais sortir des bornes publiées. Afficher les deux.
- **Un jeton qui sert de fond ET de couleur de texte ne se renverse jamais.** Sur SLGN,
  `--ink` faisait les deux; le passer en clair pour la version claire a donné du texte clair
  sur fond clair, 42 échecs de contraste d'un coup. Basculer les **fonds** un par un.
- **Un contraste se mesure en recomposant l'alpha sur le fond opaque le plus proche.**
  Sans cette recomposition, `rgba(247,239,228,.42)` sur encre se lit 15,23:1 au lieu de 3,71:1
  et la mesure ne voit aucun échec. Seuil 3:1 au-dessus de 24px ou 18,66px gras, 4,5:1 ailleurs.
- **Le panneau de prévisualisation ne compose aucune image** (`visibilityState:"hidden"`), donc
  `requestAnimationFrame` ne se déclenche jamais et les transitions CSS ne progressent pas.
  Un effet au défilement passé par rAF y paraît mort, et tout `.rv.in` y paraît à opacité 0.
  Se prouve en dix secondes et se contourne en appelant la frame directement.
- **Le JS lit le même point de bascule que le CSS, avec `matchMedia`.** `window.innerWidth` peut
  diverger de la largeur du viewport CSS, et la branche mobile ne part alors jamais.
- **Un élément qui n'apparaît pas se diagnostique par ce que les manquants ont en commun**,
  en croisant leur liste avec leurs classes, pas au hasard.
- **Dire à chaque livraison ce qui a été prouvé par mesure et ce qui n'a jamais été vu rendu.**

## Ce qui fait «IA» et qui est rejeté

- **La combinaison** cartes arrondies 16 à 22px, ombres douces, boutons pilule 100px, rangée de
  quatre cartes égales, et même rythme étiquette plus titre plus intro répété sur cinq sections.
  Chacun se défend seul, ensemble c'est la signature du gabarit.
- **L'uniformité parfaite** des paddings, des largeurs et des gaps.
- **Une échelle dont un seul cran porte tout le contenu.**
- **Le combo AI luxury:** serif léger géant, crème, champagne doré, nav foncée.
- **Le logo de plateforme livré comme logo.** Duda sert `logo-header.svg` qui rend un «L» cerclé
  à côté du mot LOGO. Confirmer le vrai logo par le `alt` de leur HTML et en ouvrant le fichier.
- **Les grandes marges latérales vides et les cellules de grille orphelines.** Choisir des
  comptes de grille qui divisent juste: 10 éléments en une bande pleine plus un 3x3, 4 éléments
  en une rangée de 4.
- **Les tics que le détecteur attrape mécaniquement** (`bash scripts/detect.sh`, étape 6):
  texte en dégradé, pastille d'accroche au-dessus du titre du héros, tuile d'icône arrondie
  au-dessus de chaque titre, cartes dans des cartes, halo radial derrière le héros, lueur
  sombre, serif italique de display, easing rebond, point qui pulse, tracking négatif
  extrême, bandes de dégradé répétées, rayures de grille en fond. Ne pas attendre la passe
  de vérification pour les éviter: ne pas les écrire.
- La liste complète des rejets de design est dans `DIRECTIONS.md`.

## Ce qu'il fait systématiquement et qu'il faut anticiper

- **Il coche trois effets de mouvement quand la question en propose deux.** Constaté quatre
  fois. **Le plafond de deux est un plancher pour lui.** Les trois effets doivent occuper des
  zones différentes pour ne pas se battre. Ne pas ramener à deux sans le lui dire.
- **Une image de référence fournie pour le build écrase AUSSI la planche à trois bandes**, pas
  seulement la question de direction. Deux règles se contredisaient là-dessus, `SKILL.md` disant
  de la sauter et `RULES.md` de la faire toujours. La référence tranche: elle montre déjà un haut
  de page, la planche ne lui apprendrait rien.
- **Il envoie une référence et veut la structure, pas la palette.** Sa formulation: «C'est pas
  tellement les couleurs, c'est le côté moderne et épuré qui casse du site web IA classique.»
- **Une référence renvoyée deux fois est un brief, pas une suggestion. Une référence
  envoyée UNE fois avec le mot « exactement » l'est déjà**, même en plein milieu d'un build,
  même après une planche à trois bandes. Ses mots le 2026-08-24 sur Les Francs Planchers:
  *« je veux que le site ressemble exactement a celui la »*.
- **Quand les trois bandes d'une planche sont rejetées, demander une référence, pas une
  deuxième planche.** Sur Cléopâtre il a répondu « tu m'envoies une référence » plutôt que
  de regarder trois mondes neufs. Deux planches rejetées coûtent plus qu'une référence.
- **Il génère volontiers sur Gemini si on lui donne le prompt.** Recette qui marche: cadrage
  serré nommé, mains gantées seulement, aucun visage entier, et un **négatif explicite** contre
  le texte, les logos, les étiquettes de série, la rouille, la rougeur et le registre médical.
  Sans négatif, tout modèle redescend vers le cliché chaleureux.
- **Le négatif n'empêche pas le texte sur une machine: regarder les images avant d'intégrer un
  clip.** Sur SLGN, Veo a écrit « OUTAOAIS » en grosses lettres blanches sur la flèche de la pelle
  malgré un négatif explicite contre le texte. Relever les bornes du texte image par image,
  recadrer pour le sortir du cadre, et couper avant l'instant où il revient.
- **Une boucle vidéo se ferme au fondu, et la couture se MESURE.** Segment principal, plus
  la queue superposée en fondu alpha sur le début. Se prouve en comparant la première et la
  dernière image: si l'écart moyen tombe au niveau de deux images consécutives du milieu,
  la jonction ne se voit pas. Sur KDM, 8,21/255 contre 6,15/255 de référence.
- **Une vidéo trop lourde se RACCOURCIT, elle ne se dégrade pas.** Passer de 9,2s à 6,2s au
  même CRF a fait tomber le fichier de 3,08 à 2,24 Mo sans toucher à l'image. Monter le CRF
  aurait abîmé la vedette pour le même gain.
- **Une vidéo qui porte déjà l'effet ne se double pas.** Le clip de KDM contenait sa propre
  chute de neige: le canvas est descendu d'un facteur trois en densité, flocons plus gros et
  plus lents, pour jouer en parallaxe de premier plan au lieu de faire de la poussière.
- **La vidéo du héros est la vedette, pas une texture de fond.** Demandé le 2026-08-21:
  *« je trouve que les vidéos ne mettent pas assez en avant et ne sont pas assez premium »*.
  Plein écran, voile plafonné à .42 en haut et allégé au tiers, et un push lent plutôt qu'un plan fixe.
- **Les bandes d'une planche ne sont pas exclusives: il en COMPOSE deux.** Le 2026-08-25 sur
  MSB Cleaning: *« la deuxieme avec la photo du premier comme hero qui occupe tout l'espace
  derriere »*. Proposer la composition soi-meme quand deux bandes sont proches, et annoncer
  AVANT de batir ce que le melange casse: ici la signature est tombee de trois emplois a deux,
  parce que rien ne va par-dessus une photo de heros.
- **Il taille dans le contenu en cours de route:** «pas besoin de toutes les photos, c'est juste
  un mockup, choisis les plus belles». Proposer le tri soi-même.
