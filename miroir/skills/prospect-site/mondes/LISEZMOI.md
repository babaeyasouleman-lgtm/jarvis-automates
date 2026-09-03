# Le catalogue étendu de mondes

152 jeux de tokens installés le 2026-08-30, extraits des paquets `design-systems/`
du dépôt `nexu-io/open-design` (Apache-2.0). Un fichier `<slug>.css` par monde,
plus `MONDES.tsv`, l'index.

## La règle de lecture. Elle est la raison d'être de cette forme.

**Ne jamais faire `cat MONDES.tsv`.** L'index fait 36 Ko, soit à peu près le coût
d'un build entier. Il n'est là que pour être filtré. Passer par le script:

```bash
python scripts/monde.py --fond clair --temp chaud,or --sans-repet
python scripts/monde.py --cherche "editorial|paper|magazine"
python scripts/monde.py --slug cafe --adn
python scripts/monde.py --slug cafe --css > travail/monde.css
```

Une sélection imprime une dizaine de lignes. C'est ce qui fait que passer de 16
à 168 mondes ne coûte rien par build: **un appel de script, puis un seul
`tokens.css` lu, celui du monde retenu.**

`--sans-repet` compare les candidats aux 5 derniers builds de `BUILT.tsv` sur les
deux axes vérifiables mécaniquement, la police de titrage et l'accent, et écarte
les collisions en les nommant. Mesuré sur l'historique complet: 56 des 152 mondes
entrent en collision avec au moins un des 64 builds passés.

## Ce que ces mondes apportent vraiment, et ce qu'ils n'apportent pas

Chaque `tokens.css` porte une palette complète, une échelle typographique, une
échelle d'espacement, un rythme de section, un rayon et une largeur de conteneur.
**Ce sont des valeurs mesurées et cohérentes entre elles.** C'est le vrai gain:
la section « cadrage » de `DIRECTIONS.md` existe pour régler le reproche le plus
constant, police trop grande ou trop petite et trop d'espace entre les sections.
Un monde qui arrive avec son `--text-3xl`, son `--section-y-desktop` et son
`--container-max` rend ce réglage mécanique au lieu de jugé.

**La typo, elle, ne vaut rien ici.** Sur les 61 paquets libres, 35 titrent en
Inter et 12 en Georgia. Soit 47 sur 61 qui retombent sur les deux polices par
défaut de l'industrie. C'est exactement le réflexe par défaut que l'axe 4 de
`DIRECTIONS.md` combat.

**Donc: prendre la palette, le rythme et le rayon d'un monde, et continuer à
choisir la typo dans le banc libre, appairage neuf vérifié par `grep` sur
`BUILT.tsv`.** L'appairage en est à 33 et c'est un compte à ne pas casser.

**Le deuxième réflexe par défaut du catalogue, c'est le fond crème.** 26 des 49
mondes libres à fond clair posent un blanc cassé chaud du type `#fbf6ee`,
`#f7eee6` ou `#fff8d7`, exactement ce que `detect.sh` signale sous
`cream-palette`. Le sélecteur marque ces mondes d'un `creme` dans sa colonne, ce
qui permet de choisir en connaissance de cause au lieu de découvrir la trouvaille
après la capture, quand elle est cuite dans l'image.

Mesuré sur un build d'essai avec `--monde cafe`: une trouvaille `low-contrast`
en moins que le gabarit d'origine, une trouvaille `cream-palette` en plus. Le
troc est acceptable, il n'est pas gratuit.

## Les 91 paquets de MARQUE

`monde.py` les exclut par défaut. Poser l'identité de Ferrari, Stripe ou Nike sur
la page d'un plombier de Gatineau n'est pas une direction visuelle, c'est un
problème de marque. Ils restent installés et `--marques` les rouvre quand il le
demande explicitement, par exemple pour une palette dont il aime la mécanique.
La colonne `usage` porte `MARQUE` ou `libre`.

## Les trois trous du catalogue, bouchés

`DIRECTIONS.md` nommait trois familles de métier sans aucune planche. Candidats
libres, à confirmer au premier usage réel:

| Famille sans planche | Mondes qui la couvrent |
|---|---|
| table (restaurant, boulangerie, café) | `cafe`, `warm-editorial`, `paper`, `vintage`, `storytelling`, `artistic` |
| détail (boutique, fleuriste) | `friendly`, `colorful`, `bento`, `clean`, `clay`, `creative` |
| entretien (nettoyage, déménagement, paysagement) | `spacious`, `minimal`, `flat`, `professional`, `corporate`, `application` |

## Un défaut du dépôt d'origine, à connaître

**Dans un même paquet, `DESIGN.md` et `tokens.css` se contredisent.** Vérifié sur
`editorial`: le `DESIGN.md` annonce primaire `#111111`, police Gelasio et échelle
14/16/18/24/32/40, alors que le `tokens.css` du même dossier donne accent
`#9a5a2f`, Georgia et Source Serif Pro, échelle jusqu'à 92px. Deux systèmes
différents dans le même dossier.

Seul le `tokens.css` a été repris. Les `DESIGN.md` ont été laissés là-bas: c'est
de la prose générée du type « Keep hierarchy obvious: headline → support text →
primary action », qui n'apprend rien que `DIRECTIONS.md` ne dise déjà mieux.

## Régénérer

`scripts/build_mondes.py` refait le dossier depuis un clone du dépôt:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/nexu-io/open-design.git
cd open-design && git sparse-checkout set design-systems
python scripts/build_mondes.py open-design/design-systems mondes
```

Il convertit hex, `rgb()` et `oklch()` en `#rrggbb`, ne lit que le premier bloc
`:root` (sinon un bloc `[data-theme=dark]` écrase les valeurs claires), et calcule
la température de l'accent et la classe de la police. L'index est reconstruit en
entier, aucune écriture partielle.

## Colonnes de `MONDES.tsv`

`slug`, `nom`, `categorie`, `usage`, `fond` (clair/sombre, calculé sur la
luminance du fond), `temperature` (de l'accent), `accent`, `bg`, `fg`,
`classe_titre`, `police_titre`, `classe_corps`, `police_corps`, `titre_px`,
`corps_px`, `rayon_px`, `section_y_px`, `conteneur_px`, `allure`.
