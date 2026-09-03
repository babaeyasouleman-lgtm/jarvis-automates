---
name: prospect-site
description: Build a bilingual demo MOCKUP of a sales prospect's website from their existing site URL, and deliver it as ONE self-contained HTML file ready to email. A visual direction to present to the owner, not a content-complete site. Use when the user gives a prospect's URL and wants a demo/mockup to pitch them, says "fais une démo pour ce prospect", "build a sample site for this company", "j'ai un nouveau prospect", or asks to redo/improve a prospect demo.
---

# Prospect Demo Site

Transforme le site faible d'un prospect en une **maquette** bilingue qu'il envoie au
propriétaire pour gagner le contrat.

**Livrable: UN fichier `.html` autonome.** Pas un dossier, pas un ZIP. Il l'envoie par
courriel, le propriétaire double-clique, ça marche hors ligne. Tout vit dans
`C:\Users\Administrator\OneDrive\Bureau\<Nom-Du-Prospect>\`, avec `index.html` + `assets/`
pour itérer.

## Ce que c'est, et ce que ce n'est pas

C'est une **direction visuelle présentée à un propriétaire d'entreprise**: une vue globale
de ce que son site pourrait être. Il doit voir le design, la structure et la bascule
bilingue. C'est tout.

Ce n'est **pas** le site fini. Ne pas reconstruire leur contenu. Ce travail est ce qu'il se
fait *payer* après le pitch, et le faire d'avance est ce qui a transformé des jobs de
10 minutes en jobs de 45. *« J'ai juste besoin d'une maquette, quelque chose de faisable en
5 à 10 min. »*

S'il demande explicitement le build complet, c'est un autre travail. Le dire et confirmer.

---

## Quel fichier lire, et quand

Le poids de lecture est le premier poste de dépense de ce skill. Ne rien lire « au cas où ».

| Fichier | Quand | Poids |
|---|---|---|
| `RULES.md` | **chaque build**, une fois | 28 Ko |
| `BUILT.tsv` | **jamais en entier.** `tail -5` pour le non-répété, `grep` pour le reste | 152 Ko |
| `DIRECTIONS.md` | à l'étape design, une fois | 28 Ko |
| `inspiration/PINTEREST.md` | à l'étape design, si une référence s'applique | 8 Ko |
| `mondes/MONDES.tsv` | **jamais en entier.** Toujours par `scripts/monde.py` | 36 Ko |
| `mondes/<slug>.css` | un seul, celui du monde retenu | 8 Ko |
| `mondes/LISEZMOI.md` | une fois pour comprendre le catalogue, jamais en build | 8 Ko |
| `MOTION.md` | seulement pour les effets retenus | à la demande |
| `TECHNIQUE.md` | seulement face au problème correspondant | à la demande |
| `*-ARCHIVE.md` | jamais en entier. `grep` sur un mot-clé | 260 Ko |

**Ne jamais lire `BUILT-ARCHIVE.md` ni `PREFERENCES-ARCHIVE.md` en entier.** Ils sont là
pour retrouver le contexte d'une décision par `grep`, pas pour être chargés.

**`BUILT.tsv` a passé les 150 Ko et ne se lit plus en entier non plus.** La règle du
non-répété n'a besoin que de `tail -5 BUILT.tsv`. Une vérification d'appairage typo se
fait par `grep -c "NomDeLaPolice" BUILT.tsv`, jamais par une lecture.

---

## Les quatre règles de travail. Non négociables.

Elles viennent d'un désastre réel et il les redit en tête de chaque demande. Les suivre
sans qu'il les demande.

1. **Aucune réécriture globale par regex, sed ou remplacement sur tout le document.
   Jamais.** Chaque changement vise une chaîne unique identifiée.
2. **Compter `<section>`, `<div>` et `<figure>` avant et après**, annoncer l'écart attendu
   avant d'éditer. *Si un compte ne correspond pas, ARRÊTER et le signaler. Ne pas tenter
   de réparer.*
3. **Ne faire QUE ce que la passe demande.** Aucune amélioration spontanée, aucun
   refactoring opportuniste, aucun changement de contenu non demandé.
4. **Finir par un compte rendu court:** ce qui a changé ligne par ligne, et ce qui n'a pas
   pu être fait.

Ce qui a produit la règle 1: une passe de normalisation avec
`re.sub(r'(padding|margin|gap):\s*([^;}]+)', ...)` sur tout le document. Sur un
`style="margin-top:20px"` en ligne, `[^;}]+` n'avait pas de terminateur, a dépassé le
guillemet fermant et **avalé cinq sections en silence**. Détecté seulement en comptant les
`<section>` et en en trouvant 4 au lieu de 7.

---

## Étape 1. Un seul fetch

```bash
curl -sL https://PROSPECT.com/ -o prospect.html
grep -oE '(src|href)="[^"]*(png|jpg|jpeg|webp|svg)[^"]*"' prospect.html | sort -u
grep -oE '#[0-9A-Fa-f]{6}' prospect.html | sort | uniq -c | sort -rn | head
```

Retirer les balises pour avoir le texte, et le lire une fois. Cela donne le métier, la
tagline, téléphone, courriel, adresse, heures, noms de services, numéro de licence.

**Ne prendre que ce qu'une maquette montre:** nom, métier, noms de services, bloc de
contact, heures, deux ou trois phrases de leur propre formulation. Rien d'autre.
**Ne pas crawler les sous-pages**, sauf brief « montrer leurs réalisations ».

Prospect sans URL: chercher son numéro de téléphone avant tout. Voir `RULES.md`.

---

## Étape 2. Deux questions, un seul appel

Groupées sur sa demande du 2026-08-12. Poser aussi les questions **en texte simple dans le
message**, parce que le panneau a déjà échoué en silence.

**Q1. Direction visuelle.** Les deux mondes les mieux classés par l'algorithme de
`DIRECTIONS.md`, décrits par leur allure et non par leur nom. **Si l'écart de score est de
3 points ou plus, ne pas poser la question:** annoncer le monde retenu et sa raison en une
phrase. Si il a fourni une image de référence pour ce build, la référence gagne et la
question ne se pose pas.

**Q2. Sections et mouvement**, multi-select, options concrètes. Sections: avis Google
(toujours proposé), avant/après, tarifs, réservation, galerie, équipe, blogue. Mouvement,
tiré de `MOTION.md`: révélation clip-path, bulles flottantes, deck ancré épinglé, curseur
personnalisé, marquee, rayon scrubé, titre assemblé. **Proposer trois effets, pas deux:**
il en coche trois à chaque fois, quatre fois de suite. Ils doivent occuper des zones
différentes pour ne pas se battre.

**La langue par défaut n'est pas une question:** elle suit leur marché. La confirmer à la
livraison.

Sans réponse, avancer avec: le monde le mieux classé, palette du logo, avis Google plus une
section adaptée au métier, trois effets.

**S'il dit « reste proche de leur look actuel », dire dans le même message qu'on ne peut pas
voir leur site rendu et demander deux ou trois captures avant de commencer.** Le HTML, les
variables de thème et les fichiers image donnent la palette et le logo, ils ne disent rien
de la mise en page, du rythme ni du mouvement. Sur Maro cela a coûté deux rondes rejetées.

---

## Étape 2.5. La planche de direction, avant le build complet

Ajoutée sur sa demande du 2026-08-12: *« ça sauve du temps et des tokens »*.

**Un seul fichier HTML contenant trois bandes empilées**, trois versions du haut de page du
même prospect. Même logo, même titre, même bouton. Ce qui change: le monde, la typo, la
palette, la forme du héros. Il ouvre, il regarde, il répond « la 2 ».

- **150 lignes par bande, pas une de plus.** Héros seulement, plus une étiquette de section
  et un bouton. Aucune autre section, aucun texte de remplissage, aucune traduction.
- Les trois bandes sont les **trois mondes les mieux classés** par l'algorithme, ou les deux
  premiers plus une variante du gagnant s'il domine.
- Les vraies photos et le vrai logo dedans, sinon la comparaison ne vaut rien.
- Envoi par `SendUserFile`, une phrase par bande pour dire ce qui la distingue.
- Puis **le build complet ne construit que la bande choisie.**

**Pourquoi cette étape existe.** Un aperçu en texte dans la question laisse trop
d'imagination: sur Elite Beauty Lab il a choisi sur un croquis ASCII. Un rejet de direction
après le build complet coûte environ 50 000 tokens et une refonte entière; trois bandes en
coûtent environ 8 000. Rentable dès qu'un rejet sur six est évité.

**Quand la sauter:** il a fourni une image de référence pour ce build, ou il a demandé
explicitement d'aller vite, ou l'algorithme donne un écart de 3 points ou plus.

---

## Étape 3. Les actifs, vite

Télécharger le logo et les 3 ou 4 photos les plus prometteuses. Obtenir les dimensions
**numériquement** (commande dans `TECHNIQUE.md`), puis **n'ouvrir que le candidat au héros**.
Juger le reste sur les dimensions seules.

**Les images sont le poste coûteux.** Une lecture d'image coûte plus que n'importe quelle
quantité de texte. Pour trier un lot, faire une planche-contact et la lire une fois.

Deux choses que les dimensions disent sans regarder:

- Un héros pleine largeur exige une source paysage de **1600px ou plus**. Sinon **changer la
  forme du héros** plutôt qu'étirer.
- **Adapter la taille d'affichage à la résolution de la source.** Rétrécir la case plutôt
  qu'agrandir le fichier.

---

## Étape 4. La direction, décidée en une fois

**Lire `DIRECTIONS.md` et `BUILT.tsv`, puis écrire la ligne d'ADN avant tout HTML:**

```
MONDE <nom> · HÉROS <forme> · ÉTIQUETTE <traitement> · TYPO <titre + corps>
ACCENT <nom #hex> · RYTHME <largeurs et crans> · SIGNATURE <l'objet du métier>
```

**Le catalogue de mondes est double.** Les seize mondes de `DIRECTIONS.md` restent le
choix principal. Quand ils sont serrés par la règle du non-répété, ou quand le prospect
tombe dans une des trois familles sans planche (table, détail, entretien), tirer un
monde du catalogue étendu de 152 jeux de tokens:

```bash
python scripts/monde.py --fond clair --temp chaud,or --sans-repet
python scripts/monde.py --slug cafe --adn
```

En prendre la palette, le rythme et le rayon, **pas la typo**: 47 des 61 paquets libres
titrent en Inter ou en Georgia, ce qui est exactement le réflexe par défaut que l'axe 4
combat. La typo reste choisie dans le banc libre, appairage neuf vérifié par `grep` sur
`BUILT.tsv`.

**Aucun des quatre premiers axes ne peut répéter les cinq dernières lignes de `BUILT.tsv`.**
C'est la règle qui empêche deux prospects de se ressembler, et c'est la raison d'être de ce
skill: il les présente côte à côte à des propriétaires différents. Ouimette v1 a été rejeté
pour avoir réutilisé la barre, la nav, le héros, les cartes, les pastilles, le CTA et le
formulaire d'Alictro. *« Deux gouttes d'eau. »*

L'échelle typographique, le rythme vertical et le cadrage des images sont dans
`DIRECTIONS.md`, section « cadrage ». Ce sont les règles qui règlent le reproche le plus
constant: police trop grande ou trop petite, trop d'espace entre les sections, et un
ensemble qui n'a pas l'air intentionnel.

Sauter le CLI `ui-ux-pro-max` sauf métier vraiment inconnu: sa palette se fait écraser par
la couleur du logo de toute façon.

---

## Étape 5. Construire une fois

Un seul `index.html`, `<style>` et `<script>` en ligne, images en `assets/...` pendant le
travail.

**Copier la plomberie depuis `scripts/mechanics.html`** au lieu de la réécrire: récolte et
bascule bilingue, révélations au défilement avec leur filet de sécurité, compteurs qui ne
peuvent jamais afficher 0, nav mobile, formulaire de démo, `prefers-reduced-motion`. Le
fichier ne contient **ni mise en page ni style**, exprès, pour qu'il ne puisse pas faire
se ressembler deux prospects.

Deux garde-fous ne sont pas optionnels, parce qu'il présente ça en direct et qu'une page
blanche ou à zéro perd le contrat. Les compteurs portent la vraie valeur dans le HTML et ne
sont remis à 0 qu'à l'instant où JS peut les animer. Chaque règle « caché jusqu'à
révélation » est cadrée sur `.js`, et le filet de 1,5 seconde révèle tout si l'observateur
ne se déclenche jamais.

Aussi: cibles tactiles à 44px ou plus, et honorer `prefers-reduced-motion`.

### Plafonds. C'est tout l'intérêt du skill.

| | Plafond |
|---|---|
| Sections | 5 à 7 |
| Chaînes traduisibles | 40 à 70 (le build Gabon en a eu 173) |
| Texte par section | un titre et une ou deux phrases |
| Images employées | 3 à 5 |
| Texte long tiré de leur site | aucun, une phrase citée au maximum |

Les marques S-WEB Agency, obligatoires sur chaque build, sont dans `RULES.md`.

---

## Étape 6. Vérifier par la mesure

```bash
python scripts/verify.py "Prospect-demo.html"
```

Puis **`scripts/probe.js` dans le panneau**, sur `index.html` servi avec ses `assets/`
(en `data:` le panneau ne décode aucune image et `naturalWidth` vaut 0 partout). Balayer
375 / 820 / 1280 / 1440 / 1920 et **vérifier `out.w` en retour**, le panneau ignore parfois
le redimensionnement.

`probe.js` teste ce qu'aucune relecture de code ne trouve: débordement horizontal, images
affichées plus larges que leur source, cibles sous 44px, sticky tué par un ancêtre,
police retombée sur Arial, crans typographiques orphelins, paddings empilés entre sections,
rythme uniforme, h1 en escalier, contenu vivant sous un masque, et largeur de conteneur
unique.

**Troisième mesure, le détecteur d'anti-patterns.** Déterministe, aucun LLM, aucun token,
1,5 seconde. Sur le fichier inline final, pas sur `index.html`.

```bash
bash scripts/detect.sh "Prospect-demo.html"
```

Il attrape ce que `verify.py` et `probe.js` ne voient pas: contraste WCAG calculé, texte
fonctionnel sous 11px, niveaux de titres sautés, `<img>` sans `src`, longueur de ligne,
interligne serré, texte gris sur couleur. Sur Pose ta Pierre il a trouvé un 2,3:1 sur
`#0a0a0a` posé sur `#6b4226`, cinq fois, et des libellés de formulaire à 9,5px.

**Trier avant de corriger.** `undersized-ui-text` se déclenche sur les étiquettes de section
espacées, qui sont un choix assumé du skill. Regarder la valeur: sous 10px on remonte,
entre 10 et 11px on juge. `low-contrast`, `skipped-heading`, `broken-image` et
`text-occlusion` se corrigent toujours, sans discussion. Ce sont des défauts, pas des goûts.

**Toujours dire quelles parties ont été prouvées par mesure et lesquelles n'ont jamais été
vues rendues.** Le comportement au défilement se prouve par mesure mais ne se ressent pas:
le dire et le laisser juger.

---

## Étape 7. Livrer et enregistrer

```bash
python scripts/inline.py --html index.html --assets assets --out "Prospect-demo.html"
```

`inline.py` réécrit chaque référence `assets/<fichier>` en `src`, `href` et `url()` CSS en
data URI base64. Viser sous 1,5 Mo pour les images. Un héros vidéo peut aller à 2,5 Mo.

Envoyer avec `SendUserFile`. Dire clairement ce qui est réel (logo, photos, téléphone,
licence) et ce qui est un emplacement réservé, signaler toute photo de banque et son risque
de licence, nommer les dispositifs repris d'une référence, et dire ce qui n'a pas été vu
rendu.

Puis **deux écritures, et deux seulement:**

1. **Une ligne dans `BUILT.tsv`.** Colonnes: date, nom, langue, palette, typo, héros,
   étiquette, signature, rayon, mouvement. Une ligne, pas une page.
2. **Ce qu'il demande de changer, dans `RULES.md`**, avec ses mots. Une préférence nouvelle
   **remplace une ligne existante ou en ajoute une.** Jamais un paragraphe. Ne jamais
   inventer une préférence.

Une préférence enregistrée une fois ne devrait jamais avoir à être répétée.
