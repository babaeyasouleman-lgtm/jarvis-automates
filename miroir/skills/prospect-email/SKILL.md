---
name: prospect-email
description: Envoie un courriel de prospection froid a un commerce, avec UNE image de ce a quoi son site pourrait ressembler et un appel a la rencontre de 15 minutes. Construit un seul haut de page, le capture en cadre ordinateur + telephone, ecrit le courriel bilingue, envoie et journalise. Utiliser quand il dit "envoie un cold email a ce prospect", "fais-moi un teaser pour cette entreprise", "lance le lot de prospection", ou donne une URL en demandant un courriel plutot qu'une demo complete.
---

# Courriel de prospection avec image

Le petit frere de `prospect-site`. Celui-la construit une maquette entiere pour un Meet
deja fixe. Celui-ci sert **avant l'appel**: un seul haut de page, transforme en **une
image**, colle dans un courriel froid qui demande 15 minutes.

**Ce qui part au prospect: une image et six lignes de texte. Jamais le fichier HTML.**
C'est la regle de son propre processus, section 4: la maquette ne part jamais par
courriel, seulement une capture. L'image donne assez pour donner envie, pas assez pour
se passer de lui.

Objectif de temps: **12 a 20 minutes par prospect**, pas 45. Si un prospect en demande
plus, c'est qu'il merite le vrai skill `prospect-site`, pas celui-ci.

---

## Les quatre regles de travail

Reprises de `prospect-site`, elles s'appliquent ici aussi.

1. **Aucune reecriture globale par regex ou sed.** Chaque changement vise une chaine unique.
2. **Compter `<section>` et `<div>` avant et apres** toute edition, annoncer l'ecart attendu.
3. **Ne faire QUE ce que la passe demande.** Aucune amelioration spontanee.
4. **Finir par un compte rendu court**: ce qui est parti, a qui, et ce qui a ete saute.

Deux regles de plus, propres a ce skill:

5. **Regarder l'image une fois avant l'envoi.** Une seule lecture d'image, obligatoire.
   Un courriel froid avec une capture vide brule le prospect pour toujours.
6. **Zero tiret cadratin, zero vocabulaire IA.** Voir la memoire `no-em-dashes-no-ai-voice`.
   Un courriel froid qui sent la machine est supprime en deux secondes.

---

## Le fichier a lire, et quand

| Fichier | Quand |
|---|---|
| `COURRIEL.md` | chaque envoi, une fois. C'est le texte et ses regles |
| `ENVOI.md` | chaque envoi, une fois. Plafonds, fenetres, liste d'exclusion |
| `../prospect-site/DIRECTIONS.md` | a l'etape design, pour choisir le monde |
| `../prospect-site/BUILT.tsv` | **jamais en entier**, il fait 152 Ko. `tail -5` pour le non-repete, `grep` pour une typo |
| `../prospect-site/mondes/MONDES.tsv` | **jamais en entier**. Toujours par `monde.py` |
| `../prospect-site/RULES.md` | seulement si un point de style bloque |
| `ENVOYES.tsv` sur le Bureau | avant tout envoi, c'est la liste de suppression |
| `contenu/metiers.json` | voie standard, pour savoir si le metier est couvert |

Ne jamais charger `BUILT-ARCHIVE.md` ni `PREFERENCES-ARCHIVE.md`.

---

## Etape 0. La source des prospects

**Si la file est vide, la remplir soi-meme. Ne pas attendre FM Media.**

```bash
python scripts/moisson.py "salon de coiffure" --ville "Gatineau QC" --courriels --essai
```

`--essai` affiche le classement sans rien ecrire, retirer le drapeau pour ecrire dans
`FILE-ATTENTE.tsv`. Le detail du score, des quatre filtres et des pieges est dans
`SOURCE.md`. Une moisson par semaine couvre le plafond de six courriels par jour.

**Prevu: le CRM Notion de FM Media.** Il n'est pas encore accessible depuis son compte
Notion (`babaeyasouleman@gmail.com` ne voit que son espace perso). Le jour ou FM Media
partage la base, coller son URL dans `SOURCE.md` et ce skill la lit directement:
`notion-fetch` sur l'URL pour recuperer le `collection://`, puis `notion-query-data-sources`
en SQL pour sortir les fiches non contactees.

**En attendant: `C:\Users\Administrator\OneDrive\Bureau\Prospection\FILE-ATTENTE.tsv`.**
Neuf colonnes, remplies depuis son export Outscraper. `python scripts/lot.py suivants 3`
sort les trois prochaines fiches valides et applique deja la liste d'exclusion et les
plafonds.

Un prospect a la main: il donne l'URL, on saute directement a l'etape 2.

---

## Etape 0.5. LA VOIE. Trancher ici, en dix secondes, avant tout le reste.

**C'est le levier de temps numero un du skill.** Le 2026-08-24, Qualite d'air Outaouais a
pris une quarantaine de minutes au lieu de cinq, parce que la voie n'a jamais ete choisie:
elle a ete subie.

| | Voie STANDARD | Voie SUR MESURE |
|---|---|---|
| Duree | quelques minutes | 30 a 40 minutes |
| Comment | `recolte.py` puis `assemble.py` sur `gabarits/batiment.html` | a la main, monde choisi dans `DIRECTIONS.md` |
| Palette | accent echantillonne sur leur logo, papier du monde passe en `--monde` | echantillonnee sur leur logo a la main |
| Typo | derivee de leur nom, donc jamais deux fois la meme le meme mois | choisie dans le banc libre |
| Quand | par defaut, et pour tout lot de 3 | prospect a gros contrat, ou qu'il va appeler de toute facon |

**Par defaut c'est STANDARD.** On ne passe en sur mesure que si l'une de ces trois
conditions est vraie, et on la nomme dans le compte rendu:

1. **Il colle une image d'inspiration.** `DIRECTIONS.md` dit qu'une reference est un brief
   qui court-circuite l'algorithme, donc elle force la voie sur mesure. **C'est le piege:
   coller une inspiration fait basculer dans la voie lente sans qu'il l'ait decide.** Si le
   prospect ne vaut pas 40 minutes, lui dire et proposer la voie standard.
2. **Le metier n'est pas dans `contenu/metiers.json`.** Metiers couverts: plomberie,
   toiture, electricite, excavation, construction, paysagement, cvac.
3. **Aucune photo utilisable sur leur site**, donc il faut generer le heros.

### La photo generee est l'etape la plus chere du skill

C'est la seule qui contient un aller-retour humain: prompt, sa visite sur Gemini,
telechargement, verification des trois zones a risque, integration, capture, coup d'oeil,
reglage du point focal, recapture, coup d'oeil.

**Ne generer que si leur site n'a AUCUNE photo utilisable.** Regarder d'abord, toujours:
- la page A propos et la page Equipe, souvent une vraie photo studio des proprietaires
- les fonds de section dans le CSS en ligne, `background-image` sur un `.vc_custom_`
- leur page Facebook

Qualite d'air Outaouais avait une photo studio de ses deux PDG a `2021/04/jocelyn-jean.jpg`,
detourable sur fond gris uni. La version sans generation etait finie et capturee avant
meme que la question de Gemini se pose.

**Une photo de banque dans leur heros n'est pas une raison de generer.** C'est un argument
de vente a garder pour l'appel, et leur vraie photo d'equipe fait un bien meilleur heros
qu'un technicien generique: elle est vraie, et le courriel peut le dire.

### Grouper par etape, pas par prospect

Pour un lot de 3, ne jamais faire un prospect du debut a la fin puis le suivant. Faire
les 3 fetch et les 3 controles d'identite, puis les 3 constructions, puis les 3 captures.
Les lancements de Chrome, le cache de polices et le contexte de travail s'amortissent.

---

## Etape 1. Le controle d'identite. Il bloque tout le reste.

Son processus dit que cette verification **reste a la main, sans exception**. Ici elle est
automatisee, donc elle est stricte: **au moindre doute, on saute le prospect et on le dit.**

1. Chercher son numero de telephone dans Google. Il doit renvoyer le meme nom d'entreprise.
   Un autre nom: on ne batit rien, on marque `IDENTITE` dans la file et on passe.
2. La fiche ne dit pas "ferme definitivement".
3. Le courriel de destination doit **provenir de leur propre site ou de leur fiche Google**.
   Jamais un `info@` devine, jamais un motif reconstruit. Pas d'adresse trouvee: on saute.

C'est la lecon Divine MedSpa, qui a failli envoyer a un proprietaire une page au nom d'un
autre commerce. En froid, cette erreur ne se rattrape pas par telephone.

---

## Etape 2. Un seul fetch

```bash
curl -sL https://PROSPECT.com/ -o prospect.html
grep -oE '(src|href)="[^"]*(png|jpg|jpeg|webp|svg)[^"]*"' prospect.html | sort -u
grep -oE '#[0-9A-Fa-f]{6}' prospect.html | sort | uniq -c | sort -rn | head
```

On ne prend que ce qu'un haut de page montre: **nom, metier, tagline, telephone, une
photo, le logo**. Rien d'autre. Aucune sous-page. Aucun texte long.

**Le detail qui ouvre le courriel se prend ici ou sur leur fiche Google**: la note et le
nombre d'avis, une phrase de leur propre formulation, l'annee de fondation, un service
qu'ils sont seuls a offrir. Sans ce detail, le courriel est un publipostage et il se lit
comme tel. Voir `COURRIEL.md`, section "la premiere ligne".

Site absent: la fiche Google et la page Facebook suffisent. Cas Hosanna Tattoo.

---

## Etape 3. Un seul haut de page

**Une section, entre 120 et 200 lignes.** Pas de sections en dessous, pas de bascule
bilingue, pas de traductions, pas de formulaire, pas de compteurs. L'image ne montre que
le haut de page, tout le reste serait du travail invisible.

Ce qu'il contient, et rien de plus:
- la barre de navigation avec leur vrai logo, 4 ou 5 libelles, la bascule EN / FR **dessinee**
  (elle vend le bilingue en un coup d'oeil sans qu'une seule cle i18n existe)
- leur vrai numero de telephone, visible
- un titre, une accroche de deux lignes maximum, un bouton
- une vraie photo a eux

**Le monde visuel se choisit dans `DIRECTIONS.md` et ne repete pas les cinq dernieres
lignes de `BUILT.tsv`** sur les quatre premiers axes (monde, heros, etiquette, typo).
Deux prospects du meme metier dans la meme semaine qui recoivent la meme image, c'est le
risque reel: ils se parlent entre eux a Gatineau.

**Sur la voie STANDARD, c'est `--monde` qui porte ce risque.** Sans le drapeau,
`assemble.py` pose le meme papier `#F2F1EE`, la meme encre `#16181B` et le meme filet
`#DCDAD5` a chaque build: seul l'accent du logo change. Trois prospects du meme lot se
ressemblent donc de fond en comble. Tirer un monde du catalogue etendu, puis le passer:

```bash
python ../prospect-site/scripts/monde.py --fond clair --temp chaud,or --sans-repet
python scripts/assemble.py --json p.json --gabarit gabarits/batiment.html \
                           --out "<Nom>/teaser/index.html" --ville Gatineau --monde cafe
```

`--monde` remplace le papier, l'encre, le gris et le filet. **Il ne touche jamais a
l'accent**, qui reste echantillonne sur LEUR logo, c'est la regle. Le script refuse de
lui-meme un monde a fond sombre et un monde dont l'encre sur papier tombe sous 7:1, et
imprime le contraste mesure dans son compte rendu. La colonne `creme` du selecteur
previent quand `detect.sh` signalera `cream-palette` sur ce fond: 26 des 49 mondes
libres a fond clair sont dans ce cas.

**Les polices passent par le cache, jamais par un telechargement a la main.** Le premier
appel pour un appairage prend le sous-ensemble latin chez Google et le range dans
`contenu/polices/`, tous les suivants ne touchent plus au reseau:

```bash
python scripts/polices.py --titre "Radio Canada Big" --corps "IBM Plex Mono" \n                          --out "<Nom>/teaser/assets/fonts.css"
```

Ecrire la ligne d'ADN avant tout HTML, comme dans `prospect-site`:

```
MONDE <nom> · HEROS <forme> · TYPO <titre + corps> · ACCENT <nom #hex>
```

Le filigrane S-WEB sur l'image est **obligatoire** et deja dans `RULES.md`. C'est ce qui
empeche un proprietaire de faire capturer l'image par son neveu.

**Rien d'important dans le quart inferieur droit du haut de page.** C'est la que le
telephone se pose dans l'image finale, il masque cette zone. Mesure du 2026-08-19 sur
Plomberie Lalonde: une bande verticale portant leur numero, collee au bord droit, etait
entierement cachee par le telephone. Le numero est passe en bande horizontale en bas a
gauche et il est redevenu le premier element lu.

Le travail vit dans `C:\Users\Administrator\OneDrive\Bureau\<Nom-Du-Prospect>\teaser\`
avec `index.html` et `assets/`. S'il commande la demo complete plus tard, ce dossier est
le point de depart et l'image est deja faite.

---

## Etape 3.5. Les deux detecteurs, avant la capture

**D'abord `lint.py`, qui juge la MECANIQUE.** 0,2 seconde, aucun jugement de gout. Il
attrape les bogues qui ne produisent aucune erreur, seulement un rendu faux, et il evite
un cycle capture-regard complet:

```bash
python scripts/lint.py "<Nom-Du-Prospect>/teaser/index.html"
```

Ses cinq controles viennent chacun d'un bogue deja paye:

| Controle | Le bogue d'origine |
|---|---|
| `collision-de-classe` | `.act{margin-top:28px}` du bouton du heros ecrasait `.lang span.act`, la bascule FR, qui sortait a 4px de haut au lieu de 32 |
| `classe-sans-regle` | `.nbr` existait dans le HTML, sa regle CSS avait ete oubliee en reportant la feuille: telephone coupe en `(613) 779- / 8540` |
| `fichier-absent` | une image cassee dans l'image du courriel, c'est le courriel mort |
| `1fr-sans-minmax` | une colonne en `1fr` nu ne descend jamais sous la largeur min-content, le texte deborde et `overflow-x` le coupe en silence |
| `regle-orpheline` | renommage a moitie fait |

Sortie 1 s'il reste un GRAVE. Ne jamais capturer avec un GRAVE ouvert.

**Ensuite `detect.sh`, qui juge le GOUT.**

```bash
bash scripts/detect.sh "<Nom-Du-Prospect>/teaser/index.html"
```

Deterministe, aucun LLM, aucun token, 1,5 seconde. A faire **avant** `teaser.py`, jamais
apres: une fois l'image capturee, un contraste rate ou un texte a 9px est cuit dedans et
c'est exactement ce que le proprietaire regarde en premier.

Ce qui compte ici, dans l'ordre:

1. `low-contrast` et `gray-on-color`. Le proprietaire ouvre le courriel sur son telephone,
   souvent dehors. Un 3:1 qui passe sur ton ecran ne passe pas au soleil.
2. `undersized-ui-text` et `tiny-text`. Le haut de page est reduit dans le cadre ordinateur,
   puis recompresse en JPEG sous 500 Ko. Un libelle de nav a 10px devient une bouillie.
   Dans ce skill le plancher est plus haut que dans `prospect-site`: **12px sur la nav**.
3. `broken-image` et `text-occlusion`. Une image cassee dans l'image, c'est le courriel mort.
4. `hero-eyebrow-chip` et `icon-tile-stack`. Ce sont les deux tics qui crient le gabarit IA
   sur un haut de page seul, et un haut de page seul est tout ce qu'il voit.

Le reste se juge. Ne pas corriger une trouvaille qui ne se voit pas dans le cadrage capture.

---

## Etape 4. L'image

```bash
python scripts/teaser.py --html index.html --out "../<Nom>-teaser" --url "leursite.ca"
```

Deux captures Chrome sans interface, 1440x900 et 390x844 en 2x, composees dans un cadre
ordinateur avec un telephone devant, sur un fond tire de la couleur moyenne de la maquette.
Sortie: un `.png` maitre et un `.jpg` sous 500 Ko pour le courriel.

Le script injecte un CSS de capture qui force les elements en attente de revelation a
opacite 1. Sans lui, tout ce qui attend un `IntersectionObserver` sort vide, parce que
Chrome sans interface ne compose qu'une seule image.

**Deux pieges mesures le 2026-08-19, tous deux corriges dans le script.** Ne pas les
reintroduire en le simplifiant:

1. **Chrome sans interface refuse un viewport sous environ 477px.** `--window-size=390`
   rend la page a 477px puis rogne l'image a 390, ce qui coupe le texte en plein mot sans
   qu'aucune erreur n'apparaisse. Le script rend donc le mobile **dans une iframe de
   390px** posee dans une fenetre plus large, puis recadre. C'est la seule facon d'obtenir
   un vrai viewport mobile en ligne de commande.
2. **Une colonne de grille en `1fr` ne descend jamais sous la largeur min-content de son
   contenu.** Toujours `minmax(0,1fr)`, y compris dans les media queries, sinon le texte
   deborde et `overflow-x:hidden` le coupe en silence.

Pour mesurer au lieu de deviner: copier la page, injecter un `<script>` synchrone en fin
de `<body>` qui ecrit `clientWidth`, `scrollWidth` et les elements dont le `right` depasse
dans un `<pre>`, puis lire le resultat avec `--dump-dom`. Ca ne coute aucune lecture
d'image.

**Deux verifications, les deux obligatoires:**

1. L'ecart-type imprime par le script. Sous 12, la page n'a rien rendu, le script le dit.
2. **Ouvrir le `.jpg` et le regarder.** Une lecture d'image. Le titre est-il lisible, la
   photo chargee, le telephone au bon endroit, le logo net. C'est la regle 5.

Reglages utiles: `--desktop 1440x820` si le haut de page est court, `--mobile 390x760`
si le telephone parait trop haut, `--no-force-reveal` si le CSS de capture casse un
effet voulu.

---

## Etape 5. Le courriel

Lire `COURRIEL.md` et suivre son gabarit.

**SA VOIX EST ARRETEE et elle vit dans `COURRIEL.md`, section 'SA VOIX'.** Chaleureuse et
diplomate, jamais donneuse de lecons. **Ne jamais proposer un autre registre.** Le
2026-08-24, le meme courriel a ete reecrit trois fois faute de ce paragraphe, et la
version retenue reprenait 80 % de son propre brouillon. Le premier jet sort dans sa voix.

En resume, ce qui ne bouge pas:

- **Objet sous 45 caracteres**, sans majuscules criees, sans point d'exclamation. Et
  **ne pas annoncer la vente dans l'objet**, type "Amelioration de votre site web"
- **125 mots maximum**, 6 paragraphes. Un courriel froid long n'est pas lu
- **La premiere ligne parle d'eux**, avec un detail verifie **tourne en compliment**.
  Jamais de "j'espere que vous allez bien"
- **Un seul narrateur, et c'est lui.** "je", jamais "notre agence" puis "je"
- **Une impression, jamais un verdict.** Et desamorcer: "pas parce qu'il est mauvais"
- **L'image est en piece jointe ET affichee en ligne** dans le HTML du courriel
- **Deux creneaux reels**, tires de ses fenetres, 12 h a 13 h ou apres 17 h, **plus
  l'ouverture sur les leurs**: "si ces moments ne vous conviennent pas, proposez-moi le
  votre". C'est cette ouverture qui separe le chaleureux du dirigiste
- **Jamais le temps passe sur la maquette.** Ca ancre la valeur sur son temps a lui
- **Sans engagement**, dit une fois, en clair
- Le bloc d'identification et de desabonnement de `COURRIEL.md`, obligatoire par la LCAP
- **Langue: francais pour Gatineau, anglais pour Ottawa**, decide par la langue de leur
  propre site. Les deux versions sont dans `COURRIEL.md`

---

## Etape 6. Envoyer

Lire `ENVOI.md` avant, chaque fois. Il porte les plafonds, la fenetre horaire, la liste
d'exclusion et l'interrupteur d'arret.

Envoi par Gmail, compte `babaeyasouleman@gmail.com`, image en piece jointe `inline`.

```
send_message(to=[adresse], subject=..., body=<texte simple>, htmlBody=<version HTML>,
             attachments=[{filename:"<Nom>-teaser.jpg", content:<base64>,
                           mimeType:"image/jpeg", inline:true}])
```

**Toujours fournir `body` en texte simple en plus du `htmlBody`.** Un courriel froid en
HTML seul tombe en indesirable beaucoup plus souvent.

Apres chaque envoi, une ligne dans `ENVOYES.tsv`. C'est la liste de suppression: **une
adresse qui y figure ne recoit jamais un deuxieme premier contact.**

---

## Etape 7. La relance, une seule

**J+3, sur le meme fil, trois lignes.** Le gabarit est dans `COURRIEL.md`. Une seule
relance, jamais deux. Sans reponse apres elle, la fiche passe a `APPELER`: le telephone
prend le relais, avec l'accroche qui existe deja dans son processus, "je vous ai envoye
un courriel et je n'ai pas eu de retour".

C'est le vrai role de ce skill. **Le courriel ne vend pas le forfait, il rechauffe l'appel.**

---

## Le compte rendu

Cinq lignes, pas une page:

- combien de prospects traites, combien envoyes, combien sautes et pourquoi
- pour chacun: le nom, l'adresse, l'objet, le monde visuel retenu
- ce qui a ete prouve par mesure et ce qui a seulement ete regarde
- ce qui reste a faire a la main
- la date de la relance J+3
