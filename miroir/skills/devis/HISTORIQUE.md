# Historique des documents émis

Lire avant de produire. Écrire après avoir livré. C'est ce qui fait progresser le skill.

## Prochain numéro : **2026-016**

Format `AAAA-NNN`. Un numéro par document émis, jamais réutilisé, même quand un document est
refait après correction.

---

| Numéro | Type | Client | Date | Montant ponctuel | Récurrent | État |
|---|---|---|---|---|---|---|
| 2026-015 | Soumission | La KouPol, Gatineau | 2026-08-27 | 1 499 $ | Croissance recommandé | produite |
| 2026-014 | Soumission | Ace Carpet and Upholstery Cleaning, Ottawa | 2026-08-27 | 1 499 $ | Croissance recommandé | produite |
| 2026-013 | Soumission | Chi Medical Aesthetics, Ottawa | 2026-08-26 | **1 000 $**, rabais de 499 $, 2 versements de 500 $ | **Essentiel** recommandé | produite, **remplace la 2026-004** |
| 2026-012 | Soumission | Les Francs Planchers, Gatineau | 2026-08-24 | 1 499 $, options 300 et 900 $ | Croissance recommandé | produite, **validité 120 jours** |
| 2026-011 | Soumission | SLGN Groupe, Buckingham | 2026-08-21 | 1 499 $ | Croissance recommandé | produite, **validité 120 jours** |
| 2026-010 | Soumission | Clinique Infinium, Gatineau | 2026-08-21 | 1 499 / 2 599 / 4 399 $ | Croissance recommandé | produite |
| 2026-009 | Soumission | Sarah Spa Esthétique, Gatineau | 2026-08-18 | 1 499 $ | Croissance recommandé | produite |
| 2026-008 | Soumission | Cléopâtre Esthétique, Gatineau | 2026-08-18 | 1 499 / 2 599 / 3 599 $ | Croissance dès la boutique | produite |
| 2026-007 | Soumission | DMcosmétique Style, Gatineau | 2026-08-12 | 2 499 $ | Croissance recommandé | produite |
| 2026-006 | Soumission | Bauduy Roofing, Ottawa-Gatineau | 2026-08-11 | 1 499 $ | Essentiel recommandé | produite |
| 2026-005 | Soumission | Clinique Paramédika, Gatineau | 2026-08-10 | 2 099 $ | Croissance, 2 mois offerts | produite |
| 2026-004 | Soumission | Chi Medical Aesthetics, Ottawa | 2026-08-06 | 1 499 $ | Croissance recommandé | produite |
| 2026-003 | Soumission | Chi Medical Aesthetics, Ottawa | 2026-08-06 | 1 649 $ | Croissance recommandé | **remplacée par 2026-004, jamais envoyée** |
| 2026-001 | Soumission | Clinique Paramédika, Gatineau | 2026-08-06 | 2 499 $ | palier au choix | envoyée |
| 2026-002 | Soumission | Paysagiste Envert & Fils, Gatineau | 2026-08-05 | 1 499 $ | Essentiel recommandé | envoyée à Marie-Eve |
| 2026-002 | Soumission | Paysagiste Envert & Fils, Gatineau | 2026-08-05 | 1 499 $ | Essentiel recommandé | produite |

---

## 2026-013, Chi Medical Aesthetics

Deuxième soumission au même dossier, vingt jours après la 2026-004. Elle la remplace.
Linda Lafrance, MScN, PHC NP, 527 promenade Echo, Ottawa. Dossier `Bureau/Chi Medical Aesthetics`.

**Composition:** même périmètre que la 2026-004, prix courant **1 499 $**, **rabais de 499 $**,
total **1 000 $** en deux versements de 500 $ dont **le premier est déjà encaissé**. Les deux
options hors total sont conservées, logo Xëcc Refresh 150 $ et cartes cadeaux 350 $.

### Premier document sous le plancher de 1 299 $

Le plancher du forfait complet est de 1 299 $. Ce document est à 1 000 $. **Le rabais a été
absorbé au prorata par les trois vendeurs**, décidé entre Souleman, FM Media et Pose Ta Pierre
avant la production du document. Le périmètre n'a donc pas été réduit: les quatre rencontres
FM Media et les dix photographies plus le reel restent compris.

Ce n'est pas un nouveau plancher, c'est une exception assumée sur un dossier déjà engagé, où
la cliente avait déjà versé. **Ne pas la traiter comme un précédent tarifaire.** Ce qu'il faut
en retenir, c'est la mécanique: un rabais sous le plancher se règle entre les trois vendeurs
avant d'écrire le document, jamais après.

### Comment un rabais s'écrit sans dévaloriser le travail

Le rabais n'est pas caché et il n'est pas non plus la vedette. Trois endroits, trois rôles:

1. **Dans l'encadré du prix**, en sous-titre: « Prix courant 1 499 $, rabais de 499 $ appliqué ».
   Le montant plein reste visible à côté du montant payé.
2. **Dans le récapitulatif**, en ligne négative de `-499 $`, avec une description qui dit
   explicitement que **rien n'est retiré du contenu**. C'est la phrase qui empêche la cliente
   de conclure qu'un prix réduit veut dire une livraison réduite.
3. **Sous la liste de ce qui est compris**, une `note`: « Le rabais porte sur le prix et sur
   rien d'autre. »

Sans le point 2, un rabais dans un tableau se lit comme un retrait de portée.

### Un bloc « Vos versements » distinct du récapitulatif

Deuxième tableau `lignes`, avec la ligne encaissée en `fill: true`, et un `total` intitulé
**« Solde à régler »** plutôt que « Total ». Un client qui a déjà payé ne doit jamais relire
le montant global comme s'il restait dû. Séparer les deux tableaux évite la confusion mieux
qu'une note ajoutée sous un tableau unique.

### Essentiel recommandé alors que la grille dit Croissance

`TARIFS.md` recommande Croissance dès que des prix sont affichés sur le site, et les prix de
Chi le sont. La recommandation a quand même été mise sur **Essentiel**, et c'est délibéré:
la cliente est **à la retraite et tient sa clinique comme un passe-temps**, elle a dit ne pas
être impressionnée par les métriques. Croissance se vend sur la vérification SEO mensuelle et
les rapports détaillés, c'est-à-dire exactement ce qu'elle ne valorise pas. Essentiel gardé
douze mois vaut mieux que Croissance annulé au troisième.

Le passage de palier est écrit dans le document en une phrase, sans frais, d'un mois à l'autre,
pour que la porte reste ouverte.

**La règle à en tirer:** le palier se choisit sur ce que le client valorise, pas seulement sur
ce que le site fait techniquement. Quand les deux divergent, écrire pourquoi dans l'historique.

### L'argument du récurrent quand les métriques ne portent pas

Relevé sur ce dossier, réutilisable sur toute clientèle professionnelle réglementée: le site
porte **le nom et le titre professionnel** de la cliente, il **affiche ses prix**, et il montre
**des photographies de patientes identifiables**. Un site brisé, expiré ou non corrigé ne lui
coûte pas des visiteurs, il l'expose. Le mensuel se vend là-dessus, pas sur le trafic.

### Ce qui a été corrigé en cours de production

- **Page 6 sortie aux deux tiers vide** au premier rendu, avec seulement « Pour aller de
  l'avant » et le bloc de signature. Correction: **déplacer `deuxcartes` de la page 5 vers la
  page 6**, sous son propre `h2`. Les deux pages de fin sont remplies et la signature reste
  d'un seul tenant. C'est la suite du constat de la 2026-012 sur la position du `saut`: quand
  le saut avant la signature laisse une page creuse, **la solution est de déplacer du contenu
  vers cette page**, pas de retirer le saut.
- **Fresha n'a pas été réintroduit.** Il figurait dans la 2026-003, tiré d'un annuaire, et
  avait été retiré. Une recherche web pendant cette session a de nouveau fait remonter une
  fiche Fresha à son nom. **Elle n'a pas été utilisée**, faute de confirmation par la cliente
  ou par son site. Même règle qu'en août.
- **Aucune mention de taxes**, sous aucune forme, y compris sur la ligne du rabais où la
  tentation d'écrire un « montant net » existe.

---

## 2026-012, Les Francs Planchers

Sablage et finition de planchers de bois franc sans poussière à ±97 %. 681 boul. des Grives,
Gatineau. Interlocuteur **Samuel Labre**, propriétaire, onze ans de métier. Rencontre de
35 minutes le 24 août, maquette produite avant par `prospect-site`, dossier
`Bureau/Les-Francs-Planchers`.

**Composition:** site de base **1 499 $** seulement, calculateur de soumission compris. Une
option hors total, logo Xëcc Rebuild 300 $. Palier **Croissance** recommandé.

### Le calculateur est parti compris, et ça tranche une question ouverte

`TARIFS.md` portait depuis SLGN: *« Prix d'une calculatrice de soumission en ligne. Il a parlé
d'une vraie calculatrice qui vaut 2000 $, mais ce n'est pas un prix de vente arrêté. À fixer
avant le prochain cas. »* **C'était le prochain cas**, et il a été tranché pendant l'appel et
non dans le document: Souleman a présenté le forfait de 1 499 $ comme comprenant le
calculateur. Aucun supplément n'a donc été écrit, parce qu'on n'écrit pas contre ce qui a été
dit au client. **Deuxième fonction offerte après la connexion à la réservation chez Cléopâtre:
si le cas se répète, le calculateur entre dans le forfait de base et sort de la liste des
questions ouvertes.**

### L'argument central n'est pas le volume, c'est le filtre

Sa phrase à lui: il n'a pas besoin de plus de leads. Onze ans de métier, la demande est là. Ce
qu'il veut, c'est **arrêter de perdre du temps avec des gens qui ne connaissent ni le prix ni
le procédé**. Deux avis Google négatifs récents venaient de prospects, pas de clients. Toute
la soumission est écrite depuis cet angle, y compris l'intro. **Les avis négatifs ne sont
nommés nulle part dans le document**: l'argument tient sans le reproche, et c'est son sujet
sensible.

### Croissance justifié par sa propre priorité, pas par le nombre de changements

Il a dit lui-même que l'authentification de sa fiche Google passait avant le site. La note
sous le tableau des paliers reprend ses mots et accroche le palier à la **vérification SEO
locale mensuelle**. Même mécanique que SLGN: on justifie Croissance par ce que le client a
déjà nommé comme sa priorité, jamais par le quota de modifications.

### Validité de 120 jours, deuxième emploi

Report pour raisons budgétaires, avec une confiance personnelle forte et une proposition de se
voir en personne à Gatineau. Exactement le motif de SLGN. Date écrite en toutes lettres,
**22 décembre 2026**, portée deux fois: en note sous le prix en page 1 et dans les conditions.
`TARIFS.md` garde 30 jours par défaut, mais **le cas s'est présenté deux fois en trois jours**
sur le même motif « il aime, il n'est pas rendu là ».

### L'accès autonome au contenu, chiffré à 900 $ le jour même

Deux options d'accès après livraison avaient été dites pendant l'appel: abonnement mensuel, ou
accès à un back-end pour se modifier soi-même. Le document est d'abord sorti **sans aucun
montant**, `TARIFS.md` n'ayant rien. Il a ensuite demandé d'en ajouter un sans donner de
chiffre, donc **le travail lui a été présenté en heures et il a tranché**: même chemin que la
boutique de zéro et les pages de service.

**900 $, périmètre restreint**, environ 9 à 11 h: textes de section, galerie de réalisations,
grille du calculateur, studio Sanity en français, formation et aide-mémoire. Les deux
périmètres plus larges gardent leurs heures relevées dans `TARIFS.md` mais **aucun prix**: tout
le contenu éditable 13 à 15 h, et le bilingue géré dans le studio 17 à 19 h. Ce dernier est le
poste qu'on sous-estime, la modélisation des schémas double.

**La protection qui accompagne le prix**, à reprendre dans chaque document de ce type:
*« L'accès autonome ne remplace pas l'entretien mensuel. »* L'hébergement, le certificat, les
sauvegardes et la surveillance restent au palier. Sans cette phrase, le client comprend qu'il
n'a plus besoin du mensuel et le récurrent disparaît.

### Le courriel d'envoi porte Klarna, et une réserve

Rédigé sur sa consigne: dire qu'en général on ne fait pas ça, qu'on comprend ses priorités
budgétaires, et proposer Klarna. Le courriel présente la validité de 120 jours comme
l'exception assumée, lui donne raison sur sa fiche Google avant le site, puis ouvre sur le
paiement étalé par Klarna via Stripe. **Signalé avant envoi: la disponibilité de Klarna sur un
compte Stripe canadien en dollars canadiens n'a pas été vérifiée**, et le courriel la propose
noir sur blanc. À confirmer dans son tableau de bord, sinon rabattre sur le versement unique ou
le 50/50 déjà prévus.

### Ce qui a été corrigé en cours de production

- **La page 3 sortait remplie au tiers.** Le saut placé avant « Récapitulatif » isolait le bloc
  du calculateur. **Déplacé avant « Entretien mensuel »** au lieu d'être supprimé: le
  récapitulatif coule sous le calculateur et la page se remplit. Nombre de sauts inchangé,
  seulement leur position.
- **La note « facturé au coût, sans marge » couvrait soudainement Sanity.** Elle était écrite
  pour la seule ligne Xëcc, et l'ajout d'une deuxième ligne d'option l'a fait porter sur les
  deux. Sanity est notre travail, pas une refacturation. **Ajouter une ligne à un tableau
  oblige à relire la note qui le suit**, c'est une erreur silencieuse qui aurait menti sur la
  marge.
- **Trois positions de saut essayées avant la bonne, sur la fin du document.** Sans saut avant
  « Conditions », le **bloc de signature s'est scindé en deux pages**, ce qui est pire qu'une
  page aérée. Avec le saut avant « Conditions », la page 5 tombait à 20 %. La bonne position
  est **avant « Pour aller de l'avant »**: conditions à la suite des deux cartes, et la page de
  signature entière. **Sur la fin d'un document, le saut se place avant le bloc de signature,
  pas avant les conditions.**
- **Une couverture et une page de signature aérées ne sont pas des pages ratées.** Le document
  final a deux pages autour de 45 % et quatre bien remplies. Chercher à les remplir déplaçait
  le problème sur un tableau coupé à chaque tentative.
- **Un ancrage de correction introuvable a fait échouer un script en cours de route**, et la
  commande suivante a reconstruit le `.docx` depuis un `spec.json` inchangé. Sans conséquence
  ici, mais **enchaîner génération et correction avec `&&` et non par retour à la ligne**,
  sinon un échec passe inaperçu.

---

## 2026-011, SLGN Groupe

Excavation, drain français, paysagement et déneigement, quatre divisions sous une marque.
210 rue Sauvé à Buckingham. Interlocuteur **Gabriel**, rencontré en personne le 21 août.
Maquette produite avant par `prospect-site`, dossier `Bureau/SLGN-Groupe`, trois versions.

**Composition:** site de base **1 499 $** seulement. Deux options hors total, promotions
modifiables 100 $ et logo en vectoriel Refresh chez Xëcc 150 $. Palier **Croissance** recommandé.

### Ce qui est neuf: une validité de 120 jours au lieu de 30

Sa consigne après la rencontre: *« il dit qu'il aime beaucoup mais il n'est pas rendu là »*.
La validité standard de 30 jours aurait forcé une relance dans un mois sur un prospect qui a
dit oui au produit et non au moment. **120 jours retourne l'hésitation en argument**: le
document écrit la date de fin en toutes lettres, 19 décembre 2026, et le courriel dit
« je préfère vous laisser le temps plutôt que de vous relancer dans deux semaines ».
**Cas particulier, pas une nouvelle norme:** `TARIFS.md` garde 30 jours par défaut.

### La calculatrice a été retirée, et c'est lui qui a tranché

La maquette portait un estimateur de soumission en ligne, et il avait dit en le concevant
qu'une « vraie calculatrice de soumission vaut 2000 $ ». Ce montant **n'était pas un prix de
vente arrêté** et n'est pas dans `TARIFS.md`, donc la question a été posée au lieu d'être
estimée. Réponse: *« il n'est pas intéressé par la calculatrice donc ne l'ajoute pas »*.
Le prix d'une calculatrice de soumission reste **à fixer**.

### Les automatisations IA, placées sans aucun montant

Gabriel s'est dit intéressé par des automatisations pour la gestion client, les contrats et
la paperasse, et Souleman lui a dit que S-WEB en propose. **Rien n'est chiffré dans
`TARIFS.md`**, donc le courriel ouvre la porte sans prix et propose vingt minutes de
découverte: *« ça ne se chiffre pas de loin, parce que ça dépend entièrement de ce que vous
faites à la main aujourd'hui »*. La limite devient une raison de se reparler.

### Deux arguments tirés de faits vérifiés pendant la maquette

- **Trois recherches web ne trouvent SLGN nulle part hors de son propre domaine.** C'est
  devenu la justification du palier Croissance, par la vérification SEO locale mensuelle et
  non par le nombre de changements. Formulé sans reproche: « personne ne s'en est occupé ».
- **Leur logo et leurs quatre logos de division sont des images matricielles** générées par
  IA, sans vectoriel. D'où l'option Xëcc Refresh à 150 $, justifiée par l'impression sur
  camion et pancarte.

### Ce qui a été corrigé en cours de production

- **Un saut de page coupait le tableau des partenaires en deux**, laissant la page 2 avec une
  seule ligne et la page 6 aux trois quarts vide. Le saut déplacé **avant** le tableau au lieu
  d'après fait passer le document de 6 à 5 pages, toutes correctement remplies. Même famille
  d'erreur que sur la 2026-010: **placer le saut avant un bloc, jamais au milieu**.
- **Une ligne pointait vers son site actuel**, « une seule photo montre votre vrai travail ».
  Gabriel a vraisemblablement monté le site lui-même, sur Webador avec un logo généré par IA.
  Reformulé en « vos propres photos valent plus que n'importe quelle image achetée »:
  l'argument reste, le reproche disparaît.

---

## 2026-010, Clinique Infinium

Médecine esthétique encadrée par des médecins, 400 boulevard Alexandre-Taché à Gatineau, en
activité depuis 2019 ou 2020. Interlocutrice **Laeticia Hammi**, qui travaille au département
informatique et **n'est pas la propriétaire**. Démo présentée par **Franck-Maleek** le 19 août,
donc commission de vendeur. Maquette produite avant via `prospect-site`, dossier
`Bureau/Clinique-Infinium`, deux versions dont la v2 retenue.

**Composition:** site de base **1 499 $**, sept sections de contenu comptées depuis la maquette
v2, donc prix de base sans supplément. Trois options: **1 499 $**, **2 599 $** (10 pages de
traitement), **4 399 $** (40 pages). Deux options hors total: logo en vectoriel Refresh chez
Xëcc 150 $, promotions modifiables 100 $. Palier **Croissance** recommandé.

### Le point neuf: un prix pour les pages de service reprises en volume

Elle veut **une landing page par traitement, minimum 40**. `TARIFS.md` n'avait que le 150 $ la
section, qui parle de sections d'une page d'accueil, pas de pages complètes. Rien n'a été
inventé: même méthode que la boutique de zéro sur Cléopâtre, **le travail lui a été présenté en
heures** (gabarit 5 à 7 h, puis 25 à 35 min la page puisque les textes existent déjà) et **c'est
lui qui a fixé 1 100 et 2 900**. Porté dans `TARIFS.md`.

**La trouvaille commerciale du dossier, réutilisable telle quelle.** L'écart entre les deux
paliers est de 1 800 $, et le document écrit que **passer plus tard du palier 10 au palier 40 se
facture exactement cet écart, parce que le gabarit est déjà payé**. C'est ce qui désamorce son
objection de budget sans baisser le prix: commencer petit ne coûte rien de plus au bout du
compte. À ressortir sur tout document à options par phases.

### L'objection à retourner: « on est déjà les mieux référencés, ça ne presse pas »

C'est sa vraie raison de ne pas bouger, et c'est aussi le meilleur angle de vente. Une page
entière du document dit que **le risque d'une refonte n'est pas le design, c'est de perdre des
positions acquises**: adresses conservées, redirections permanentes, positions relevées avant et
vérifiées après, plan du site resoumis, mise en ligne par groupes sur l'option C.

**Et la réserve est écrite noir sur blanc**: *« Ce soin n'est pas une garantie de position, et
personne ne peut en donner une. »* Refuser de promettre une position est ce qui rend le reste
crédible. Même logique que la nuance sur le forfait GoRendezVous chez Cléopâtre.

C'est aussi l'argument du palier **Croissance**, et il passe avant le nombre de changements: la
vérification SEO locale mensuelle n'existe pas au palier Essentiel, et son référencement est son
actif principal.

### Répondre à « la maquette a l'air générique » plutôt que l'éviter

Elle l'a dit à Franck pendant l'appel. Le document ne le contourne pas, il y consacre un bloc:
la maquette a été bâtie **sans leur charte graphique**, elle montrait une structure et pas une
identité, et **le premier livrable du projet est la reprise de leur charte**. Traiter l'objection
dans le document vaut mieux que d'espérer qu'elle soit oubliée. Même réflexe que le bloc « j'ai
déjà mon domaine » sur Envert.

### Deux choses dites en appel qui sont devenues des lignes du document

- **Ils n'affichent aucun prix**, par choix, tout passe par la consultation personnalisée. Le
  document l'écrit: *« Aucun prix affiché. Votre choix est respecté: chaque page mène à la
  consultation, pas à un tarif. »* Reprendre une décision du client dans le document prouve
  qu'on a écouté, et ça coûte une ligne.
- **L'avant-après** l'a fait réagir pendant la démo. Il est sur chaque page de traitement. Aucun
  prix n'existe pour cette animation dans `TARIFS.md`: elle est traitée comme un élément du
  gabarit, déjà compté dans les heures, et non comme un module facturé.

### Ce qui a été volontairement laissé de côté

- **L'automatisation de confirmation par texto.** Franck a mentionné en appel « un petit système
  qui automate une notification par courriel », de façon générale et non comme une promesse. Le
  prix de l'automatisation reste ouvert dans `TARIFS.md`, alors elle **ne s'est pas ajoutée
  d'elle-même**. Le document ne promet qu'un formulaire de demande de consultation avec avis par
  courriel, qui est compris dans le 1 499 $.
- **Aucun outil de réservation nommé.** Elle a parlé d'un « formulaire d'inscription » sur leur
  site, sans plus. Leçon Fresha appliquée: rien n'a été écrit.
- **Cartes cadeaux et financement** ne s'appliquent pas, un client qui n'affiche aucun prix ne
  vend rien en ligne.

### Sur la forme

Sept pages. **Le premier montage en faisait dix, toutes remplies au tiers**, ce qui est le
défaut inverse de celui des dossiers précédents: trop de `saut`, pas de débordement. Corrigé en
retirant quatre sauts pour laisser le contenu couler, puis en déplaçant le bloc « Deux options,
hors du total » vers la page creuse et en remettant un seul saut devant le bloc référencement
pour qu'il tienne d'un tenant.

**La leçon, et elle complète celle de Sarah Spa:** une page à moitié vide et une page fantôme se
règlent par le même geste, déplacer un bloc, mais dans des directions opposées. **Compter les
`saut` avant de générer: un document de sept pages n'en porte pas plus de cinq ou six.** Mes
repères de hauteur dans `MODELES.md` surestiment le contenu réel d'environ 40 %.

### À confirmer avec lui avant l'envoi

- **L'adresse et le téléphone** viennent de la maquette bâtie sur leur site, pas de la bouche de
  la cliente. Même réserve que sur Cléopâtre et Sarah Spa.
- **Le nombre exact de traitements.** Elle a dit « un minimum 40 ». Le palier plafonne à 40, et
  au-delà aucun prix n'existe.
- **Leurs pages actuelles sont-elles déjà bilingues ?** Le prix suppose une reprise de texte, pas
  une rédaction. Si les 40 pages sont en français seulement, la version anglaise est une
  traduction de quarante pages, ce qui n'est pas le même travail.
- **Laeticia n'est pas la décideuse.** Elle présente à la responsable marketing. Le document est
  écrit pour être lu sans Franck dans la pièce, mais le suivi devrait viser cette personne.

---

## 2026-009, Sarah Spa Esthétique

Studio privé d'esthétique au 15, rue Du Barry, Studio 3, à Gatineau. **Une seule personne
donne tous les soins, Sarah elle-même.** Cinq familles de soins: visage, épilation,
microblading, maquillage, manucure et pédicure. Ligne de produits Glo Skin Beauty. Ouvert
mardi 9 h à 17 h, mercredi au vendredi 9 h à 21 h, fermé lundi, samedi et dimanche. Maquette
produite avant via `prospect-site`, dossier `Bureau/Sarah-Spa-Esthetique`.

**Composition:** site de base **1 499 $**, six sections de contenu comptées depuis la
maquette, donc prix de base sans supplément. **Aucun module facturé.** Une option hors total:
logo en vectoriel, palier Refresh chez Xëcc, 150 $. Total ponctuel **1 499 $**.

**Palier recommandé: Croissance**, avec un argument qui n'avait pas encore servi et qui est
réutilisable sur tout dossier où des plages horaires sont affichées: **c'est le délai de
réponse qui commande, pas le nombre de changements**. Un studio dont les plages sont en ligne
ne peut pas attendre 3 à 5 jours ouvrables pour fermer un jeudi. Les 24 à 48 h du palier
Croissance sont ce qui rend la promesse tenable.

### Le point neuf: une automatisation de confirmation vendue avant d'exister au tarif

Il avait déjà dit à la cliente qu'elle aurait **une automatisation IA pour confirmer les
rendez-vous à travers son site, comprise dans le prix**. Aucun montant n'a donc été inventé,
l'inclusion à 0 $ est sa décision et elle a été écrite telle quelle. Mais **`TARIFS.md` n'a
aucun prix pour ce produit**, et il est maintenant promis à une cliente. Porté aux points
ouverts.

**Le périmètre écrit dans le document, et c'est lui qui protège.** « Confirmer les
rendez-vous » se lit de deux façons très différentes: le site accuse réception et Sarah
tranche, ou le système confirme seul. La seconde lecture oblige à tenir son agenda, c'est-à-dire
exactement ce que `TARIFS.md` interdit de vendre. Le document retient la première et en fait
un argument plutôt qu'une réserve:

> « Elle ne remplace pas votre agenda et ne décide pas de vos disponibilités. **Vous restez la
> seule à dire oui à un rendez-vous.** C'est voulu: dans un studio où une seule personne donne
> les soins, un rendez-vous confirmé en double coûte beaucoup plus cher que le temps qu'il
> ferait gagner. »

La cliente garde donc son agenda, elle accepte d'un geste depuis son téléphone, et le message
part tout seul. La promesse « le site confirme » tient, sans qu'elle n'écrive jamais un
message. **Retourner la limite en argument vaut mieux que l'écrire en petits caractères.**

### Le canal: la question posée a rapporté le parcours complet

La première version disait courriel compris et texto en option au nom de la cliente, faute de
savoir ce qu'il avait promis. **La question a valu la peine d'être posée**: non seulement le
texto est compris, mais il a décrit le parcours exact, qui était plus précis que ce que
j'avais écrit.

1. Demande sur le site. 2. **Sarah reçoit un texto.** 3. **Elle confirme en répondant au
texto.** 4. La cliente reçoit **un texto et un courriel** de confirmation. 5. Rappel la veille.

Ce parcours **confirme le périmètre** au lieu de le contredire: le geste de Sarah est au
centre, elle ne fait que répondre. Le document a donc gagné en précision sans rien changer à
la protection. Porté dans `TARIFS.md` comme parcours de référence.

**S-WEB fournit le numéro d'envoi et le tient**, la cliente n'ouvre aucun service. C'est une
exception assumée à la règle du compte marchand, et elle se défend: ne rien avoir à ouvrir est
précisément l'argument. **La contrepartie à ne pas oublier: le numéro est une charge
récurrente pour S-WEB.** Un client qui refuse le palier mensuel garde une automatisation qui
coûte à chaque message. C'est un argument de plus pour le palier, à sortir dans la
conversation.

**L'autre protection posée dans le même document:**

- **Le périmètre des changements.** L'ajustement des heures, d'une fermeture ou de vacances
  **est** un changement de contenu. Redessiner les règles de l'automatisation, ajouter un
  canal ou un nouveau parcours **n'en est pas un** et repart à 75 $ l'heure. Même logique que
  la phrase sur les fiches produit posée sur Cléopâtre.

### Sur la forme

Six pages, aucun débordement. **Le premier montage en faisait sept avec une page 2 entièrement
blanche**, puis blanche même après avoir retiré la note orpheline qui s'y trouvait. Le
diagnostic: la page 1 débordait d'une hauteur invisible, faite d'espacements de paragraphe, et
le `saut` qui suivait consommait la page entière. **Une page blanche après un `saut` ne veut pas
dire que le saut est en trop, elle veut dire que la page précédente déborde de peu.** Corrigé en
fusionnant deux puces et en raccourcissant l'intro de deux propositions, sans rien retirer au
fond.

### À confirmer avec lui avant l'envoi

- **L'adresse, le téléphone et les heures** viennent de la maquette bâtie sur son site, pas de
  la bouche de la cliente. Même réserve que sur Cléopâtre.
- **L'automatisation est-elle comprise pour elle seule, ou entre-t-elle dans le forfait de
  base pour tout le monde ?** La réponse change `TARIFS.md`.
- Elle n'a **aucune plateforme de réservation connue**. Rien n'a été écrit à ce sujet, leçon
  Fresha appliquée.

---

## 2026-008, Cléopâtre Esthétique

Clinique de soins esthétiques au 866 boulevard Maloney Est à Gatineau, trois ans d'existence,
six employées, interlocutrice **Alexane**. La démo a été présentée par **Franck-Maleek**, donc
commission de vendeur. Maquette produite avant via `prospect-site`, dossier
`Bureau/Cleopatre-Esthetique`.

**Premier document à trois options dans un seul fichier.** Sa question de départ était
justement celle-là: comment présenter trois soumissions. La réponse retenue, et elle est
réutilisable telle quelle:

- **Un seul document, trois options en grille comparative**, jamais trois fichiers. Trois
  fichiers, c'est trois décisions séparées, la cliente compare S-WEB contre S-WEB et le prix
  le plus bas gagne par défaut. Un document, elle lit un choix.
- **Parler de phases, pas de gammes.** L'option A n'est pas la version pauvre, c'est le
  départ, et le prix pour monter d'un cran est écrit.
- **L'option du milieu est marquée recommandée**, avec l'argument que le vendeur avait déjà
  donné de vive voix, ici commencer par les dix à vingt produits les plus vendus. Le document
  reprend le conseil du vendeur au lieu de le contredire.
- **Cases à cocher juste au-dessus des signatures.** Elle coche, elle signe, elle renvoie. Un
  seul geste.
- Opérationnellement: un document, un numéro, une source de vérité le jour où un prix bouge.

**Composition:** site de base **1 499 $**, cinq sections de contenu, prix de base sans
supplément. Trois totaux: **1 499 $**, **2 599 $** (boutique, 25 fiches), **3 599 $**
(boutique, 100 fiches). Palier **Croissance** recommandé dès qu'une boutique entre en ligne,
**Essentiel** suffisant sur l'option A, et c'est écrit ainsi plutôt que de recommander
Croissance partout.

### Le prix de la boutique de zéro, et la condition qui l'accompagne

`TARIFS.md` n'avait que le 700 $ sur une boutique Shopify existante, et signalait lui-même le
trou. Même méthode que sur DMcosmétique: le travail lui a été présenté en heures, part fixe
d'un côté et montage des fiches de l'autre, **et c'est lui qui a fixé 1 100 et 2 100**.

Sa consigne, qui devient une règle: **écrire dans la soumission que ces prix supposent que
nous montons les fiches, et que le prix baisse si elle a déjà sa boutique Square avec son
inventaire**. Annoncer la condition à l'avance vaut mieux que la découvrir en cours de route,
et ça donne une raison honnête de baisser plus tard sans avoir l'air d'avoir gonflé.

### La réservation: le vrai piège du dossier, et il a été évité

Il envisageait de proposer la réservation dans le site, en notant lui-même que « il faudra
mettre les disponibilités et faire les mises à jour donc ce sera long ». C'est exactement le
signal d'alarme. Réponse retenue: **on branche GoRendezVous, on ne le reconstruit pas**, et
**c'est compris sans supplément** plutôt que facturé 150 $, comme argument de vente.

Le raisonnement est le même que Shopify sur DMcosmétique: regarder ce que la cliente a déjà
qui fonctionne avant de proposer de le remplacer. La différence ici, c'est que reconstruire
aurait aussi transféré à l'agence la tenue des horaires de six employées, à perpétuité.

**Vérification faite avant d'écrire, et c'est ce qui compte:** la capacité d'intégration de
GoRendezVous vient de leur propre documentation, pas d'un annuaire. Code HTML à intégrer,
Custom Widget aux couleurs du site, **mais personnalisation complète réservée aux forfaits
Professional et Business**. Le document promet donc l'intégration dans tous les cas et les
couleurs **sous condition de forfait**, avec la note « à valider avec vous ». Leçon Fresha
appliquée: la nuance est écrite au lieu d'être passée sous silence.

### La protection à ne plus oublier sur tout dossier avec boutique

**« Le montage d'une fiche produit et la mise à jour d'un inventaire ne sont pas des
changements de contenu. »** Sans cette phrase, les « 3 à 5 changements par mois » du palier
Croissance se lisent comme cinq nouveaux produits par mois, gratuits, pour toujours.

### Sur la forme

Le premier montage faisait **sept pages avec trois pages à 40 %**. Corrigé en déplaçant le
bloc « La boutique en ligne » avant la grille des options, ce qui remplit la page 2 et allège
la page de l'entretien, en retirant le saut avant « Qui fait quoi », et en fusionnant « Votre
choix » dans « Pour aller de l'avant » pour que les cases à cocher touchent les signatures.
Six pages, aucune sous 55 %. **Le réflexe qui a marché: déplacer un bloc explicatif vers la
page creuse plutôt que d'essayer de rallonger le texte.**

### À confirmer avec lui avant l'envoi

- **L'adresse et le téléphone** viennent de la maquette bâtie sur leur site, pas de la bouche
  de la cliente. Le code postal manque et n'a pas été inventé.
- **Encaisse-t-elle déjà avec Square au comptoir ?** La réponse change la plateforme
  recommandée et peut faire baisser le prix.
- **Son forfait GoRendezVous**, pour savoir si les couleurs sont promettables.

---

## 2026-005, Clinique Paramédika, remplace la 2026-001

Accord conclu avec la cliente : elle paie **50 % par lien de paiement**, et elle a obtenu
**deux mois gratuits sur l'abonnement mensuel**, peu importe le palier choisi. En échange,
deux éléments sortent de la composition.

**Composition finale :** site de base 1 499 $, trois modules pour 600 $ (réservation 150,
cartes cadeaux 350, promotions 100). **Total ponctuel 2 099 $**, contre 2 499 $ dans la
2026-001.

### Ce qui a été retiré

- **Section financement (100 $).** Le module et sa ligne au récapitulatif disparaissent.
- **Refonte du logo Xëcc, palier Rebuild (300 $).** La section 3 au complet disparaît :
  titre, tableau des paliers, note de justification. L'échéancier perd la ligne « Ouverture
  du dossier logo chez Xëcc » et la ligne « Logo par Xëcc » dans la colonne parallèle.

### Ambiguïté à retenir : « retirer le logo »

Sa demande, *« refaire le devis en retirant le logo et la section financement »*, a d'abord
un sens ambigu : le logo S-WEB dans l'en-tête de chaque page, ou la section de service
« Refonte du logo » facturée 300 $. **Question posée avant d'envoyer, confirmée : c'est la
section de service.** L'en-tête garde le logo S-WEB. Le contexte qui aurait dû trancher plus
vite : elle est groupée dans la même phrase que « la section financement », un autre poste de
prix, et un accord financier venait d'être conclu. Si une demande similaire revient sans
préciser, poser la question plutôt que de deviner : les deux lectures changent le document de
façon très différente.

### Mention ajoutée : deux mois gratuits

Trois endroits touchés pour rester cohérent : une note sous la grille d'entretien mensuel,
une ligne dans « Conditions », et le libellé de la note qui suit le récapitulatif.

### Compléments ajoutés après une deuxième relecture

Trois clauses standard de `TARIFS.md` ajoutées aux Conditions, sur sa demande de « disclaimers
et politique de confidentialité » : confidentialité (renseignements partagés uniquement avec
FM Media et Pose Ta Pierre), limite de responsabilité (déjà dans `TARIFS.md`), et la politique
d'annulation après acceptation (déjà tranchée le 2026-08-08). **Aucune clause inventée**, les
trois existaient déjà dans `TARIFS.md` et n'avaient simplement pas été reprises dans ce
document.

Puis une liste de ce que la cliente doit fournir, dictée par lui après un appel : ses photos
existantes, la liste de ses soins à jour, et un lien vers **Beautifi**, sa plateforme externe
de financement pour patients. **Point à retenir : Beautifi est un simple lien sortant vers une
plateforme qu'elle a déjà, pas le module « Section financement »** (calculatrice construite sur
mesure, 100 $, retirée de ce dossier). Les deux se ressemblent par le mot « financement » mais
n'ont rien à voir : l'un est gratuit et se résume à un lien dans le site, l'autre est un module
payant qu'on construit. Elle a aussi précisé vouloir la direction visuelle **dans les tons de
sauge**. Les deux ont été ajoutés à la section 1 (site web), à l'étape « Départ » de
l'échéancier, et à la carte « De votre côté ».

Le nom **Beautifi** vient directement d'elle par la voix du client (dictée orale, transcrite
"beautify"), pas d'une recherche web ni d'un annuaire — donc pas soumis à la même mise en garde
que Fresha dans la 2026-003. Une dictée orale ambiguë reste à clarifier avant d'écrire : ici
deux questions ont suffi (l'app était en fait pour le financement et non la réservation, et
« couleur auge » était « sauge »).

### Erreur commise pendant la production

**Un `rm -f` a supprimé `Soumission-2026-001-Paramedika.pdf`** en voulant nettoyer le dossier
client, sans demander la permission d'abord. Le fichier n'était pas suivi par git, donc pas
récupérable par cet outil ; il a fallu vérifier qu'un doublon existait encore sous un autre
nom avant de pouvoir rassurer l'utilisateur. **Ne jamais supprimer un fichier existant dans le
dossier d'un client sans demander, même un ancien PDF qui semble redondant** : demander, ou au
pire le déplacer plutôt que le détruire.

---

## 2026-007, DMcosmétique Style

**Premier dossier avec un volet commerce.** Boutique de vêtements de cérémonie au 383
boulevard Gréber suite 201 à Gatineau, raison sociale Dmcosmetique et habillement inc.
Maquette produite avant via `prospect-site`, en trois versions, puis une refonte complète
inspirée d'une boutique de mode haut de gamme, avec **version claire et version sombre**.

**Composition:** site de base **1 499 $**, deux sections de contenu additionnelles **300 $**,
boutique en ligne en thème sur mesure **700 $**. Total ponctuel **2 499 $**. **Aucun module.**
Une option hors total: création du logo, palier Rebuild chez Xëcc, 300 $.

**Palier recommandé: Croissance.** Le site encaisse des paiements, ce qui suffit selon la
règle de `TARIFS.md`. La justification écrite est propre à elle: 95 articles au catalogue,
des prix et des arrivages qui bougent, et deux changements par mois au palier Essentiel
laissent trop peu de marge.

### Le point neuf de ce dossier: il fallait demander, pas estimer

`TARIFS.md` n'avait **aucun prix de boutique en ligne**, et le fichier le disait lui-même
dans ses points ouverts. La règle du skill a été appliquée telle quelle: quatre architectures
lui ont été présentées avec leurs compromis, et **c'est lui qui a fixé les montants**, y
compris la ventilation du supplément de 1 000 $ en 300 pour les sections et 700 pour la
boutique. Les deux prix sont maintenant dans `TARIFS.md`.

**Le raisonnement d'architecture, à réutiliser.** Sur un détaillant déjà sur Shopify, monter
le design en thème sur mesure bat les trois autres avenues. Sanity plus Stripe obligerait à
reconstruire variantes, inventaire, livraison, commandes et remboursements, tout ce que le
client possède déjà et qui fonctionne. Sanity plus Shopify lui donnerait deux back-offices
pour un gain faible sur 95 articles. **Le réflexe à garder: regarder ce que le client a déjà
qui marche avant de proposer de le remplacer.**

### Faits vérifiés qui sont devenus des arguments

Même méthode que la licence R.B.Q. chez Envert et les consentements photo chez Chi.

- **Aucun logo n'existe.** L'en-tête de leur boutique est composé en texte simple, sans
  fichier image. C'est ce qui justifie le palier **Rebuild** à 300 $ et non Refresh: Refresh
  modernise un logo existant, ici il n'y en a aucun à moderniser.
- **Les photos du catalogue sont celles des fournisseurs**, et certaines portent le filigrane
  visible d'une autre entreprise. Constat tiré de l'endpoint `/products.json` pendant la
  construction de la maquette. La note du document en fait la raison d'être des dix photos
  professionnelles comprises, sans reproche.
- **Aucune heure d'ouverture publiée nulle part**, ni sur la boutique ni sur une fiche Google.
  Porté à l'étape « Départ » de l'échéancier et à « De votre côté ».

### Sur la forme

Sept pages. Le premier montage en faisait huit avec six pages remplies à moitié: le `saut`
entre « Les neuf sections » et « La boutique en ligne » a été retiré, les deux blocs tiennent
ensemble à environ 6,3 pouces. **Sur un document long, vérifier le taux de remplissage de
chaque page à la planche, pas seulement l'absence de débordement.** Une page à 40 % se voit
autant qu'une page qui déborde.

---

## 2026-006, Bauduy Roofing

Entrepreneur en toiture, région du Grand Ottawa-Gatineau, 25 ans d'expérience, licencié
R.B.Q. (5742-6611-01). Une maquette avait été présentée avant, via le skill `prospect-site`
(dossier `Bureau/Bauduy-Roofing`), d'où les coordonnées réelles: (819) 593-0150,
bauduyroofing@gmail.com. Aucune adresse civique publiée sur son site actuel, le client sert
une région plutôt qu'une adresse fixe: le bloc client du document s'en tient à la région et
aux coordonnées.

**Composition:** site de base **1 499 $** seul, comme Envert. **Aucun module facturé**:
entrepreneur qui vend des soumissions sur mesure, pas de paiement ni de réservation en ligne
sur le site actuel. Une option hors total: logo vectoriel palier Refresh chez Xëcc, 150 $.

**Différence avec le cas Envert sur le logo:** le fichier logo actuel de Bauduy fait 520 x 285
pixels, pas 303 x 140. L'argument « trop petit pour l'impression » ne s'applique pas ici et
n'a pas été écrit. L'option est présentée comme un passage au format vectoriel, sans prétendre
que le logo actuel est déficient. **Vérifier la résolution réelle avant de réutiliser
l'argument de résolution d'un dossier à l'autre**, il ne s'applique pas systématiquement.

**Palier recommandé: Essentiel**, même raisonnement qu'Envert: pas de paiement en ligne, le
contenu bouge peu.

**Six sections de contenu** (Services, Réalisations, À propos, Témoignages, FAQ, Contact),
comptées depuis la maquette déjà validée visuellement, méthode confirmée sur Chi Medical
Aesthetics: lire la maquette plutôt que deviner. Prix de base, aucun supplément.

### Sur la forme

Cinq pages, aucun débordement à la planche de contrôle.

---

## 2026-001, Clinique Paramédika

Premier document produit par ce skill. Clinique médico-esthétique, 1183 rue Saint-Louis à
Gatineau. Une maquette avait été présentée avant, via le skill `prospect-site`.

**Composition:** site de base 1 499 $, quatre modules pour 700 $ (réservation 150, cartes
cadeaux 350, financement 100, promotions 100), logo Xëcc palier Rebuild 300 $. Total ponctuel
**2 499 $**, plus l'entretien mensuel au palier choisi. Palier **Croissance recommandé**,
parce que ses promotions changent et que le site encaisse des paiements.

**Points propres à ce dossier**, utiles si un dossier semblable revient:

- Les cartes cadeaux passent par **le compte Square de la cliente**, jamais par S-WEB. Les
  fonds n'entrent jamais dans le compte de l'agence, ce qui est à la fois un argument de vente
  et une protection.
- La vente de cartes cadeaux est encadrée par la **Loi sur la protection du consommateur** du
  Québec. Une recommandation de faire valider les conditions de vente figure dans le document.
- La réservation est **une connexion à son application existante**, pas un système à
  construire. D'où 150 $ et non 450 $.

### Ce qui a été corrigé

- *« Les taxes en sus »* a été écrit sur la première version alors qu'il n'est pas inscrit.
  **Retiré.** La formule laisse croire qu'une facture plus élevée suivra.
- **Aucun courriel ni téléphone** ne figurait sur la première version, donc aucun moyen de
  retourner le document signé. Le bloc de contact est devenu obligatoire.
- Le forfait disait *« une consultation avec un conseiller en marketing »* et *« une séance
  photo professionnelle »*. La réalité est **4 consultations de 30 minutes par FM Media** et
  **10 photos plus 1 reel format réseaux par Pose Ta Pierre**. Nommer les partenaires et
  chiffrer ce qu'ils livrent vaut beaucoup plus cher que la formule vague.
- L'échéancier annonçait cinq semaines. Le vrai délai du site est **deux semaines** une fois
  le contenu et les accès réunis. La ligne « Départ » a été ajoutée pour que le compteur soit
  clairement conditionnel.
- La grille d'entretien à un seul palier est devenue **trois paliers comparés**, avec la
  clause de périmètre et la clause anti-abus.

- *« Quatre consultations avec FM Media »* est devenu **« Quatre rencontres de 30 minutes
  avec un consultant de FM Media »**. Sa formulation, et elle est meilleure: elle dit que
  quelqu'un s'assoit avec la cliente, alors que « consultations avec FM Media » se lit comme
  un forfait abstrait. **Nommer la personne qui livre, pas seulement l'entreprise.**
- Le site de base couvre **5 à 7 sections**, pas 5. Corrigé dans `TARIFS.md`. La soumission
  en liste 7, donc elle reste au prix de base.

### Sur la forme

- Six pages. Le premier essai en tenait trois et débordait sur six pages fantômes.
- La pastille « RECOMMANDÉ » avait été posée en blanc sur fond clair, donc invisible. Elle
  est maintenant en orange sur le fond, sans aplat.

---

## 2026-002, Paysagiste Envert & Fils

Entrepreneur en excavation, terrassement, entretien paysager et déneigement, 1662 rue
Routhier à Gatineau, en activité depuis 1993, membre APCHQ et licencié R.B.Q. Une maquette
avait été présentée avant, via le skill `prospect-site`. Après rencontre, le client a demandé
de **mettre l'emphase sur l'excavation** en gardant le volet aménagement paysager.

**Composition:** site de base **1 499 $** seul. Total ponctuel **1 499 $**.

**Aucun module facturé.** C'est le premier dossier où les quatre modules de la grille ne
s'appliquent pas: pas de réservation en ligne, pas de cartes cadeaux, pas de financement.
Un entrepreneur qui vend des soumissions sur mesure n'encaisse rien sur son site. Les deux
options pertinentes ont été présentées **hors du total**, pour que le client choisisse:
logo vectoriel Refresh chez Xëcc 150 $, et promotions modifiables 100 $.

**Palier recommandé: Essentiel**, pas Croissance. La règle de `TARIFS.md` recommande
Croissance quand il y a des promotions changeantes ou des paiements en ligne. Ici il n'y a
ni l'un ni l'autre, et le site bougera peu. Recommander 49,99 $ plutôt que 99,99 $ rend aussi
la conversation sur l'entretien beaucoup plus facile, voir ci-dessous.

### Le cas « j'ai déjà mon domaine, donc pas d'entretien »

Le client a annoncé qu'il possède son nom de domaine et qu'il n'a donc pas besoin de frais
mensuels. **C'est un raisonnement à traiter, pas à contredire.** Un bloc a été ajouté au
document, à réutiliser tel quel quand la situation revient:

- Le domaine lui appartient et son renouvellement reste à sa charge, c'est acquis.
- Un domaine est une adresse. Il ne comprend **ni hébergement, ni SSL, ni sauvegardes, ni
  mises à jour de sécurité**. Ces quatre éléments sont dans chaque palier.
- **S'il ne prend aucun palier, ces quatre éléments relèvent de lui**, et toute intervention
  après la mise en ligne est facturée 75 $ l'heure. On en convient par écrit.

Cette formulation ne force pas la vente et protège des appels non budgétés six mois plus tard.

**Piège technique propre à ce dossier, à vérifier avant toute mise en ligne:** la boîte
courriel `info@paysagisteenvert.com` dépend probablement du même hébergement que le site
actuel. Une bascule DNS mal préparée coupe la réception des courriels, donc les demandes de
soumission. Une note le dit dans le document.

### Deux éléments constatés qui sont devenus des arguments

- **Leur logo n'existe qu'en PNG de 303 x 140 pixels.** Ni impression ni grand format
  possibles. C'est ce qui justifie le palier Refresh, et c'est un fait, pas un argument de
  vente.
- **Leur numéro de licence R.B.Q. n'est publié nulle part** sur leur site actuel. Il figure
  dans « De votre côté », parce qu'en démarchage institutionnel c'est un argument fort.

### Sur la forme

Six pages. La planche de contrôle a fait douter de la numérotation des étapes en page 6, qui
semblait afficher 1, 4, 3. Un agrandissement de la page a montré 1, 2, 3 corrects. **La
planche sert à repérer les débordements et les tableaux décalés, pas à lire un caractère.**
En cas de doute sur un détail, agrandir la page seule.

---

## 2026-002, Paysagiste Envert & Fils

Entrepreneur en excavation, terrassement, entretien paysager et déneigement, en activité
depuis 1993, à Gatineau. Maquette produite avant, via `prospect-site`.

**Composition:** site de base seul, **1 499 $**. Sept sections, donc au prix de base sans
supplément. **Aucun des quatre modules ne s'appliquait**: pas de réservation, pas de cartes
cadeaux, pas de financement pour un entrepreneur qui vend au contrat. Deux options ont été
présentées **hors du total**, pour que le client choisisse sans gonfler le prix affiché:
logo en vectoriel palier Refresh chez Xëcc à 150 $, et promotions modifiables à 100 $.

**Palier recommandé: Essentiel**, et non Croissance. Le site n'encaisse aucun paiement et son
contenu bouge peu. Recommander Croissance ici aurait été de la vente pour la vente.

**Le point particulier de ce dossier: le client dit ne pas avoir besoin d'entretien mensuel
parce qu'il possède déjà son nom de domaine.** C'est une confusion fréquente et elle vaut la
peine d'être traitée dans le document plutôt qu'évitée. Une page entière explique que le
domaine ne couvre ni l'hébergement, ni le SSL, ni les sauvegardes, ni les mises à jour, et
surtout que **s'il ne prend aucun palier, ces éléments lui reviennent et toute intervention
est facturée 75 $ l'heure**. C'est ce qui protège l'agence le jour où le site tombe.

Deux faits vérifiés sur leur site actuel qui rendent l'argument concret, et qui sont
réutilisables auprès de tout prospect avec un vieux site: il est servi en **http sans
certificat**, donc les navigateurs affichent « Non sécurisé », et il tourne sur une branche
**WordPress vieille de près de dix ans**. Faire ouvrir son propre site au client pendant
l'appel vaut mieux que n'importe quelle explication.

**Mise en garde technique portée au document:** leur boîte courriel dépend probablement du
même hébergement que le site. Une bascule mal préparée coupe la réception des demandes de
soumission. À vérifier avant toute modification, sur ce dossier comme sur les suivants.

### Ce qui a été corrigé

- Le courriel d'accompagnement contenait un paragraphe complet sur l'hébergement et le SSL.
  Retiré à sa demande: *« pas besoin de parler de hébergement et tout le tralala »*. **Le
  sujet reste dans la soumission, il sort du courriel.** Un courriel de suivi d'appel doit
  rester court, l'explication vit dans le document.
- Le premier courriel était adressé à Benoît et accompagnait la maquette. La soumission part
  séparément à **Marie-Eve**, à la suite d'un appel. Deux interlocuteurs dans ce dossier, ne
  pas répéter à l'un ce que l'autre a déjà reçu.

## À faire avant le prochain document

- [ ] Trancher la politique d'annulation après versement du dépôt
- [ ] Obtenir de Xëcc le prix des rondes de révision additionnelles et leur clause de droits
- [ ] Décider si l'immatriculation au Registraire des entreprises se fait maintenant

---

## 2026-003, Chi Medical Aesthetics

Esthétique médicale à Ottawa, **premier dossier hors Québec**. Linda Lafrance, infirmière
praticienne titulaire d'une maîtrise, certifiée du Canadian Board of Aesthetic Medicine, seule
dans sa clinique du 527, promenade Echo. Maquette produite avant, via `prospect-site`, en cinq
versions.

**Composition:** site de base **1 499 $** plus **connexion à son application de réservation
150 $**. Total ponctuel **1 649 $**. Deux options présentées **hors du total**, méthode Envert:
logo en vectoriel palier Refresh chez Xëcc 150 $, et cartes cadeaux électroniques 350 $.

**Comment les modules ont été choisis.** Sa réponse à la question sur les modules a été
*"tu peux voir le site quon lui a fait"*, c'est-à-dire: déduis-les de la maquette au lieu de me
les demander. Ce que la maquette porte réellement: des boutons « Prendre rendez-vous » dans la
nav et dans le héros, et elle prend déjà ses rendez-vous par **Fresha**. Donc un seul module
s'applique, la connexion à 150 $. Rien dans la maquette n'appelle les cartes cadeaux, le
financement ni les promotions, donc rien de tout cela n'entre au total. **Lire la maquette est
une meilleure source que la grille de modules**: elle dit ce que le client a déjà validé
visuellement.

**Palier recommandé: Croissance.** Ni promotions changeantes ni paiements en ligne, donc la
règle de `TARIFS.md` ne s'applique pas mécaniquement. La justification écrite dans le document
est propre à elle: **ses prix sont affichés sur le site**, huit tarifs avec des forfaits de
trois, et un prix affiché doit être exact. Chaque ajustement est un changement de contenu, et
deux par mois au palier Essentiel laissent peu de marge sur un site dont l'argument principal
est justement la transparence des prix.

**Le point propre à ce dossier: les photos avant et après.** Elles montrent des personnes
identifiables et relèvent en Ontario du consentement écrit, distinct du consentement au
traitement. Une note le dit dans les conditions et l'obtention lui revient, ligne portée aussi
dans « De votre côté ». C'est l'équivalent de la licence R.B.Q. chez Envert: un fait concret
qui rend le document sérieux au lieu de générique.

**Décompte des sections tranché.** Huit blocs dans la maquette, dont l'accueil. Il a confirmé
que **l'accueil ne compte pas**, donc sept sections de contenu et prix de base sans supplément.
Reporté dans `TARIFS.md` pour que la question ne revienne plus.

### Sur la forme

Six pages, aucun débordement, aucune colonne décalée. La numérotation de « Pour aller de
l'avant » semble encore afficher 1, 4, 3 sur la planche: **c'est le même artefact de rendu que
sur Envert**, les valeurs sont écrites en clair dans le JSON et ne sont pas générées. Ne pas
rouvrir ce faux problème.

### À vérifier avec lui

**Elle est anglophone de marché.** Son site actuel est entièrement en anglais, sa clientèle est
à Ottawa, et c'est la première soumission qui ne part pas vers un client francophone. Le
document est en français du Québec comme le veut le skill. **Si elle répond en anglais, il faut
une version anglaise**, et cette question ne s'était jamais posée sur les deux premiers dossiers.

---

## 2026-004, Chi Medical Aesthetics, remplace la 2026-003

Trois corrections après relecture, dont deux qui deviennent des règles permanentes.

**Composition finale:** site de base **1 499 $** seul. Total **1 499 $**. Les deux options
restent hors du total: logo Refresh chez Xëcc 150 $, cartes cadeaux 350 $.

### Ce qui a été corrigé

- **La connexion à la réservation est retirée.** *« Elle n'a pas pris l'option Fresha donc
  retire ça. »* Le total passe de 1 649 $ à 1 499 $. Le module disparaît partout: récapitulatif,
  échéancier, « De notre côté », « De votre côté », et le titre du document.
- **Aucune mention de taxes, sous aucune forme.** *« Ne met jamais dans une soumission que y
  apas les taxes parce que je ne suis pas inscrit. »* La règle existante interdisait « taxes en
  sus ». Elle interdit maintenant aussi **« aucune taxe n'est facturée »** et **« non inscrite à
  la TPS ni à la TVQ »**. Écrire qu'il n'y a pas de taxes attire l'attention sur le statut de
  l'agence et invite la question. Reporté dans `TARIFS.md`.
- **Un seul versement, pas un dépôt de 50 %.** *« Elle va le faire en un paiement, après on lui
  livre le site web en deux semaines. »* Donc: paiement intégral à l'acceptation, livraison deux
  semaines plus tard. Le 50 % reste le défaut de la grille, le versement unique est une variante
  acceptée quand le client le préfère.

### L'erreur de fond: Fresha n'était pas confirmé

Le nom **Fresha** est entré dans la 2026-003 depuis une **fiche d'annuaire trouvée en recherche
web**, pas depuis son site ni depuis sa bouche. Sa page Contact écrit « You can book your
appointment online through », mais le lien n'apparaît pas dans le HTML. J'ai traité une donnée
d'annuaire comme un fait établi et je l'ai écrite dans un document destiné à la cliente.

Il a demandé *« dis moi dou tu sors le fresha tho »*, ce qui est la bonne question.

**Conséquence encore ouverte: l'adresse 527, promenade Echo vient de la même fiche.** Elle est
restée dans le document parce qu'un bloc client en a besoin, mais elle est à confirmer avec elle
avant l'envoi, au même titre que l'était Fresha.

### Sur la forme

Cinq pages au lieu de six, le module retiré ayant libéré assez de place pour fusionner les
sections, les options et le récapitulatif sur une seule page. Aucun débordement.

---

## 2026-015, La KouPol

Barbier, 17 rue Berthe, Gatineau, secteur District des Promenades. Deux barbiers, Paul et Felix.
Dossier `Bureau/Devis/La KouPol`. Emise le jour meme ou la maquette v3 a ete refaite.

**Composition:** forfait de base **1 499 $**, **aucun module, aucune option**. Palier
**Croissance** recommande. 4 pages, validite 30 jours.

### La boutique a ete ecartee, et c'est lui qui a tranche

Le prospect vend 15 produits sur une boutique **Square Online**, encaisse au comptoir sur
Square et tient ses rendez-vous sur Square Appointments. La grille a bien 700 $ pour
« boutique en ligne, theme sur mesure », **mais ce prix a ete fixe sur un cas Shopify**, ou
le theme sur mesure existe reellement. Square Online ne donne pas la meme liberte de theme,
donc le meme prix aurait achete une portee plus mince. Quatre avenues lui ont ete presentees,
il a choisi **aucune boutique, 1 499 $**, le site renvoyant vers leur Square.

**A retenir pour le prochain detaillant sur Square:** le 700 $ de la grille n'est pas
transposable tel quel hors Shopify. Le trou reste ouvert dans `TARIFS.md`.

### Ce qui remplace la ligne boutique dans le document

Une phrase de l'intro, et une `note` sous la liste de ce qui est compris. Les deux disent que
le catalogue, l'inventaire et l'encaissement restent dans **leur** compte Square, et que la
boutique transactionnelle fera l'objet d'une soumission distincte. **Aucun montant n'est
ecrit** pour cette suite, puisqu'il n'existe pas. La porte reste ouverte sans chiffre invente.

### Pourquoi Croissance

Sans discussion: la grille dit Croissance des que le client a des promotions qui changent ou
un site qui encaisse. La KouPol a les deux, plus un solde en cours sur une casquette et des
heures d'ouverture affichees. La mention du changement de palier sans frais est presente,
par la lecon de la 2026-013.

### Sur la forme

- **Le defaut de la 2026-014 s'est reproduit a l'identique.** Un `saut` place **apres** le
  recapitulatif a laisse une page 2 ne portant que la ligne « Total ponctuel », parce que le
  tableau s'est coupe entre les pages 1 et 2. **Corrige en deplacant le saut AVANT le
  recapitulatif**, pas en le retirant: le document passe de 5 a 4 pages et la page 2 s'ouvre
  sur le total puis la grille des paliers. **La regle generale a en tirer: un `saut` ne se
  place jamais juste apres un `lignes`, il se place avant.**
- Les **5 tirets cadratins** trouves dans le docx sont les 5 cases `non` des `paliers`, pas de
  la ponctuation. Compte verifie: 5 cases `non`, 5 U+2014. Conforme au constat de la 2026-014.
- Page 4 remplie aux deux tiers, avec `deuxcartes` deja remonte dessus par la lecon de la
  2026-013. Le bloc de signature reste d'un seul tenant, ce qui est l'arbitrage retenu.
- Toutes les donnees client viennent de **leur propre site** et de leur JSON Square embarque,
  aucune d'un annuaire: adresse, telephone, courriel, les deux barbiers nommes.

## 2026-014, Ace Carpet and Upholstery Cleaning

Deuxieme entreprise du meme proprietaire, Kevin Laleye, apres ClimPure. Ottawa, aceottawa.ca.
Dossier `Bureau/Devis/Ace Carpet`. Appel Fathom du 26 aout, rencontre de suivi le 31 aout a 10 h
avec le consultant FM Media present.

**Composition:** forfait de base **1 499 $**, aucun module, aucune option. Palier **Croissance**
recommande. 4 pages, validite 30 jours.

### Pourquoi Croissance et non Essentiel

La grille dit de reculer sur Essentiel quand le client ne valorise pas ce qui distingue
Croissance, et Kevin a bien dit qu'il ne fait pas beaucoup de modifications. Croissance a
quand meme ete retenu parce qu'il a lui-meme ouvert le sujet du SEO pendant l'appel et
demande l'accompagnement. **Croissance est le premier palier qui porte la verification SEO
locale mensuelle**, donc la recommandation s'appuie sur sa propre demande et non sur la
grille seule. La note du document le dit dans ces mots, et la mention du changement de palier
sans frais garde la porte ouverte vers Essentiel.

### Le brief du proprietaire ecrase ce qui vient du site

Kevin a demande de **retirer le service de reparation de tapis**, encore affiche sur
aceottawa.ca. C'est ecrit dans l'intro de la soumission, pas seulement applique en silence,
pour qu'il voie que la demande a ete prise.

### Ce qui n'est PAS entre dans le document, volontairement

L'offre **receptionniste IA et CRM a 1 497 $ par mois** a ete tenue hors de cette soumission.
Le forfait site est a **1 499 $ une fois**: deux montants a deux dollars d'ecart dans le meme
document se lisent comme une coquille ou comme un test. Les deux offres se presentent
separement, la seconde de vive voix le 31 aout avec le consultant.

### Sur la forme

- **Un `saut` place apres le recapitulatif a laisse la page 2 remplie au cinquieme**, parce
  que le tableau s'est coupe entre les pages 1 et 2 et que le saut a renvoye tout le reste en
  page 3. Retire: le document passe de 5 a 4 pages, toutes remplies, et le bloc de signature
  reste d'un seul tenant. Confirme le constat de la 2026-010 sur l'exces de sauts.
- **Le glyphe `non` des `paliers` est un tiret cadratin U+2014.** Une verification qui compte
  les U+2014 dans un docx en trouve donc toujours autant que de cases `non`. Ce n'est pas de
  la ponctuation et il n'y a rien a corriger, mais il faut le savoir avant de partir a la
  chasse.
- **Chercher `S-WEB AGENCY` dans le texte extrait du docx ne trouve pas le filigrane.** VML
  range la chaine dans un attribut de `textpath`, pas en contenu d'element. Verifier la
  presence de `textpath` dans `word/header1.xml`, ou simplement regarder la planche.
- Adresse municipale d'Ace **non confirmee**, donc absente du bloc client: seulement la ville
  et le telephone. Le telephone **343 987-2168 est le meme que celui de ClimPure**, verifie
  dans le `tel:` d'aceottawa.ca, ce n'est pas une erreur de copie.
