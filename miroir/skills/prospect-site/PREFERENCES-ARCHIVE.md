# Preferences: prospect demo sites

Accumulated from real feedback. Read before building; update after every delivery.
Only record what the user actually said. Never invent a preference.

Last updated: 2026-07-29. Prospects so far: Alictro Electric (Ottawa, electrician),
Les Entreprises Ouimette & Fils (Gatineau, HVAC).

He plans to build a gallery of reference screenshots for visual direction. When that
folder exists, read it before designing: screenshots are the one form of design
inspiration that actually transfers, since galleries like Awwwards cannot be scraped
usefully (see REFERENCES.md).

## Scope: a mockup, not a finished site

**The deliverable is a visual direction, not the client's content rebuilt.** Confirmed
2026-08-03, after the Gabon embassy build took roughly 45 minutes: *"Quand je te demande
une maquette tu prends 45min pourtant j'ai juste besoin d'une maquette et pas de toute
l'information complète d'un site web. Je veux une vue globale ou pouvoir présenter au
client, quelque chose de faisable en 5-10 min."*

So: 5 to 7 sections, a heading and a sentence or two each, 40 to 70 translatable strings,
3 to 5 images. Where their real page has a wall of content, show the **shape** of the
section and note that the detail comes from their existing material. Building their full
content up front is the work he gets paid for after the pitch, not before it.

What actually burned the time on the Gabon build, so watch for these: 173 translated
strings for a mockup, seven subpages fetched, ten images opened one at a time, and a long
argument with the preview pane that proved nothing.

## Delivery format

- **ONE self-contained `.html` file. No ZIP.** Confirmed 2026-07-29: "vu que c'est une
  demo en general je n'aurais pas besoin d'un zip mais juste du html que j'envoie."
  He emails the file straight to the owner. Do not produce a ZIP unless he asks.
- Keep the working folder (`index.html` + `assets/`) on the Desktop for iteration, but
  the thing he is handed is the single file.
- Save output to the Desktop, in a folder named after the prospect.

## Language

- **English by default, French available via a toggle.** Requested for the first
  prospect and treated as the standing default for these Ottawa/Gatineau businesses.
- Canadian French, not France French: *soumission* (not devis), *courriel* (not email),
  *main-d'œuvre*, *territoire desservi*.
- The FR toggle is a selling point in the pitch, mention it when delivering so he can
  demo it live to the owner.

## What he is actually selling (affects every demo)

The package is the website **plus** a free consultation with a marketing consultant, a
professional photo shoot, and a reel shot by a photographer. Told 2026-07-29.

So: **demos need photo placeholders**, not stock images. Stock undercuts the shoot he is
selling and makes the page look cheap. Keep the prospect's own real job photos, replace
every stock image with a branded placeholder panel, and include one reel/video slot.

## Content and imagery

- **Use the prospect's real logo**, pulled from their live site. Not a recreation, not
  a text substitute.
- **Use real photographs.** His words: "Avec des vrais images même si il le faut."
  Their own job-site photos are worth more than stock. Illustrated/SVG placeholder
  visuals were replaced on request, do not default to them.
- Use their real business facts (phone, email, licence number, service area, years).
- Match the prospect's actual brand colour, sampled from their logo.

## Animation

- **Rich, polished animation is expected.** He explicitly compared against the
  prospect's existing site and asked to go further: "Their current website is better
  en terme d'animation, essaie de t'inspirer de ça aussi pour le rendre encore meilleur."
- What landed: full-bleed hero photo with slow Ken Burns, staggered hero entrance,
  animated counters, directional scroll reveals, auto-scrolling work gallery that
  pauses on hover, lightbox, hover lift on cards.
- Still must respect `prefers-reduced-motion`.

## Purpose and tone

- These are **pitch pieces shown to the business owner** before any contract:
  "I'll showcase it to the owner so I want something amazing before building the
  proper website." Bias toward impressive over minimal.
- Be honest in the artifact itself about what is placeholder (sample testimonials,
  non-functional form), he is showing it to a real person who will ask.

## Communication

- He writes mixed French/English. Reply in French when he writes in French.
- He asks for exact file paths when he needs to find something, give the full path
  and a one-line command to open the folder.

## Avoid

- **The generic "AI luxury" look.** 2026-08-03, on the first Maro build: *"le site que tu
  viens de me faire a tout d'un site IA, des couleurs choisies à la police choisie."* What
  produced it: a huge light-weight display serif heading, cream plus champagne gold plus
  near-black, a dark nav, and decorative framing. That combination is the visual house
  style of AI-generated spa landing pages. Take the palette and the lettering from the
  prospect's own logo instead, and prefer the typeface family their brand already uses.
- **Never ship a platform placeholder logo.** Same build: Duda served
  `logo-header.svg`, which renders as a generic circled "L" next to the word "LOGO", and it
  went out in the mockup. *"Tu n'as pas extrait leur logo."* Their real logo was a
  different file entirely. **Confirm the logo before using it:** read the `alt` text in
  their HTML (it described the real one precisely), look for the element with the header
  logo class, and open the file to check it is a real wordmark.
- **Large empty side margins and orphan grid cells.** *"Je ne comprends pas tout l'espace
  que tu as laissé sur les côtés."* Two causes: a 1160px container inside a very wide
  viewport with a narrow left-aligned text column and nothing on the right, and a lead card
  spanning 2 of 3 columns so the third cell stretched into a tall empty box. Use a wider
  container, lay section headings across the full width (title left, intro right), and pick
  grid counts that divide evenly (10 items as 1 full-width band plus a 3x3, 4 items as a
  4-column row).
- **Never build on an unverified prospect identity.** 2026-08-04 he sent "Divine MedSpa
  d'Ottawa, 613-807-8111, ce prospect n'a pas de site web". Four searches showed the number
  is publicly listed to **Lemonade Beauty MedSpa** in Stittsville, and that they **do** have
  a site. He then confirmed it as a rebrand, with a "je pense". Had I built on the brief as
  given, he would have emailed a real business a page carrying the wrong name.
  **Before writing anything for a prospect with no URL: search the phone number.** It
  resolves the business in one query. If the name and the number disagree, ask him before
  building, and keep the business name as a single i18n key so it can be swapped in one line.
- **Editorial notes written onto the page.** 2026-08-04: *"retire les inscriptions qui sont
  comme des commentaires du genre there is no single photo on their website online"*, and
  separately *"retire aussi l'inscription Mockup from their website"*. The mockup must read
  like a finished site, not an annotated draft. **Put the caveats in the chat message
  instead.** The only note that stays on the page is the form's "demonstration form,
  nothing was sent", because that one prevents a real expectation.
- **The open-now badge on every build.** 2026-08-04: *"le open right now tu le mets sur tous
  les sites mais c'est vraiment vraiment pas nécessaire."* It was on Gabon, Maro and Divine.
  Do not reach for it by default. A live clock is only worth it when the hours are the
  actual selling point, and even then a static hours row usually says it better.
- **Filler badges.** The "Open seven days a week" pill was called out as useless. If a
  badge does not tell the visitor something they would act on, leave it out.
- **Em dashes (the long dash, U+2014). Zero. Non-negotiable.** 2026-07-29: "il y a des tirets qui font IA
  sur le site de alictro... Je ne veux plus jamais ça. Je veux qu'on enlève tout ce qui
  fait générique IA." The first Alictro build shipped with 38 of them and he spotted it
  immediately. Use commas, periods, or a colon before a list. This applies to the site
  copy **and** to how you write to him in chat.
- **Generic AI marketing vocabulary.** No seamless, robust, leverage, elevate,
  transformative, streamline, unlock, empower, cutting-edge, harness, delve.
  Testimonials especially: a real contractor says "they work well with our other trades,"
  not "they coordinate seamlessly."
- **Hollow parallel slogans.** "Real projects, real results" was replaced with what the
  photos actually show: "Panel upgrades, service work and new builds." Name the concrete
  thing instead of a rhythmic abstraction.
- ZIP archives for demo delivery (see Delivery format).
- **The rounded-card template look. This is the current definition of "ça fait IA".**
  2026-08-04, on the first Paysagiste Envert build: *"Tu viens de me fournir un autre site IA
  generated."* He sent rierastudio.com as the counter-example. The exact ingredients he was
  reacting to, all in one page: 16 to 22px rounded cards, soft drop shadows, 100px pill
  buttons, a row of four equal cards, and the same label plus heading plus intro paragraph
  rhythm repeated in five consecutive sections. Individually each one is defensible, together
  they are the generic template signature.
  **The fix that worked: hard rectangles.** `border-radius:0` on everything, no shadows at
  all, borders that actually show, section content laid on a visible rule rather than inside a
  card. One `border-radius` declaration should exist in the finished file and its value should
  be `0`. Grep for it before delivering.
  **This overrides the "soft shapes and pill buttons for home services" line in SKILL.md
  Step 3.** That guidance produced the build he rejected. His explicit direction wins.
- **Heading sizes. He reads oversized type as unpolished, not as bold.** 2026-08-05, on the
  Riera rebuild: *"regarde les tailles des polices? tu trouves ca normal? je veux quelque
  chose d'epurer moderne et qui attire les clients."* The offending values were `h1` up to
  **116px**, section `h2` up to **72px** and a marquee at **42px**. Fixed at h1 50px, h2 33px,
  marquee 15px, body 16px. **Ceiling for these mockups: h1 around 50px, h2 around 34px.**
  A `clamp()` third value above ~56px on a heading needs a reason.
- **No black.** 2026-08-05: *"J'aime pas le noir du site."* This killed the near-black
  `#141613` nav, the dark bands and the dark contact block. What replaced it: a light page
  throughout, and text set in a deep green-grey `#2E3A31` instead of black. Grep the delivered
  file for `#000`, `#111` and any near-black before sending.
- **Photos: small, square, and sliding.** Same message: *"fais en sorte que les photos defile
  et que ce soit des plus petit format et genre 3 ou 4 carre qui defile a chaque fois."* Big
  static photo panels are out. Build a rail of 1:1 tiles, 4 visible on desktop, that advances
  one full page at a time and loops.
- **La pastille qui explique que les avis ne sont pas traduits. Sur aucun site.**
  2026-08-05: *"retire Avis réels, laissés dans la langue de leur auteur cest necessaire sur
  aucun site."* La règle de fond ne change pas, un vrai avis reste dans sa langue et n'est
  jamais traduit, mais **cela ne se commente pas sur la page**. Le nom du client et la mention
  «Avis Google» sous la citation suffisent. C'est la même famille que les notes éditoriales
  écrites sur la page, déjà bannies plus haut.
- **La note Google en double, une fois dans le héros et une fois dans les avis.**
  2026-08-05: *"retire les etoiles google du debut il ne doit apparaitre qu'aec les avis plus
  bas."* La note se montre **une seule fois**, dans la section des avis. Le héros porte le
  métier et l'action, pas la preuve sociale.
- *(Add each new dislike here as it comes up, with the date and his words.)*

## Liked / validated

- **Show the rating, hide the count when the count is small.** 2026-08-04: *"enlève le
  nombre d'avis Google parce que 21 c'est pas conséquent même si on laisse l'étoile."*
  Five stars and "5.0" read as strong; "21 reviews" reads as a small business. Keep the
  score and the stars, drop the tally unless it is genuinely impressive.
- **A restrained palette still needs touches of colour.** Same day: *"trouve quelque chose
  pour donner plus de vie au site, genre mettre un peu de touches de couleur à certains
  endroits."* Pared back does not mean monochrome. What worked on Divine: one accent per
  role rather than one accent overall. Clay on every italic accent word, a different keyed
  colour per service family shown as a dot and as the hover ring, and two warm surface
  tints (blush, butter) alternating with the neutral sand.
- **Do not reuse a closed predecessor business's photos, above all a portrait.**
  2026-08-04, on Divine MedSpa: *"on ne sait pas pourquoi Lemonade Beauty est permanently
  closed et pourquoi ils ont changé de nom, peut-être que c'est pas directement le même
  owner."* He is right and it outranks the visual gain. Google keeps reviews through a
  rename **and** through a sale, so reviews naming the old brand prove nothing about
  ownership. A named person's face is the worst case: putting the previous owner on the new
  owner's site is a real error, not a stylistic one. Rule: **archived photos are usable only
  when the business identity is continuous and verified.** Generic interiors carry some
  risk; a portrait carries too much.
- **No AI-generated photos of people on these mockups.** Asked about on the same day. Two
  reasons to decline: synthetic faces are the exact "ça fait IA" tell he has rejected all
  along, and on a medical or beauty prospect they imply real clients and real outcomes.
  **What works instead: visuals drawn in CSS.** Soft overlapping colour fields, one hue per
  section, animated slowly. Colourful, clearly decorative, honest about being decoration,
  and they weigh nothing. Divine went from 0.55 MB with photos to 34 KB without, and looks
  more alive rather than less.
- **Recovering a blocked prospect's photos from the Wayback Machine landed well** as a
  technique, but see the ownership caveat directly above before using what it returns. It turned
  a photo-less page into one with the founder's real portrait. Method in INSPIRATION.md.
- Robustness guards he benefits from silently: real counter values in the HTML so
  nothing ever reads "0+", and the `.js` flag so the page never renders blank.
- **Match the display size to the source resolution.** 2026-08-03, on the Gabon diaspora
  portraits: *"Est-ce que pour les gabonais talentueux de la diaspora tu ne pourrais pas
  trouver des meilleures photos?"* The files were 199x276 to 498x555 snapshots with the
  city name baked into a white band at the bottom, shown at 270px. Fix that worked: crop
  the baked band off, then show them as 104px circles instead of enlarging them. He
  accepted it and kept the build as is. Upscaling a small file adds no information, it
  only makes the blur bigger.
- Sourcing better portraits of **real named people** from third-party sites was raised and
  deliberately not done: the rights belong to the university or photographer, not the
  prospect, and a wrong match would put a stranger's face on a client's site. Offered it
  as his call rather than doing it silently; he chose to keep the existing photos.
- **Ask the four Step 0.5 questions as plain text in chat, not only through the question
  panel.** 2026-08-04 he asked *"quand est ce que tu mas pose les question?"*. The
  `AskUserQuestion` call had been made, before any file was written, and it returned "the user
  did not answer" instantly without ever pausing, so the panel evidently never reached him and
  questions 2 to 4 were never asked. Writing the four questions out as numbered text, with the
  suggested options, costs one short message and cannot silently fail.
- **When he sends a reference site, use both channels.** 2026-08-04 he sent rierastudio.com as
  a URL **and** a screenshot. `inspect_motion.py` returned almost nothing useful, because the
  motion sat inside GSAP internals, while the screenshot handed over the entire design: hard
  rectangles, a nav split into bordered cells, botanical line art, scattered photo offsets, an
  exposed column grid. **The screenshot was worth more than the code.** Ask for one every time
  he names a reference.
- **A reference whose palette is wrong is still a good reference.** Same day: *"C'est beaucoup
  trop vert mais je veux quelque chose de plus originale et moderne comme celui la."* Riera is
  a dark green site and the prospect's brand is also green. What worked: take the structure and
  the illustration idea, move the green off the canvas and onto the line work, then add one
  warm second accent so the page is not monochrome. Take the composition, leave the palette.
- **He wants real photography, and he authorized sourcing it online.** 2026-08-05:
  *"N'oublie pas que cest des paysagistes... Mets des vrais fleurs... Des vrais exterieurs
  meme dans le background. Tu peux trouver des belles photos sur interenet pour ca."*
  **This overrides the "never put a stock photo in the mockup" rule in SKILL.md Step 4**, but
  only for backgrounds and ambiance. Keep the split strict: the projects rail carries **only
  the prospect's own photos**, so stock is never presented as their work.
  **Where to get it:** `images.unsplash.com/photo-<id>?w=1500&q=80` fetches fine with plain
  curl, and the Unsplash licence allows commercial use with no attribution. Their search pages
  and `napi` endpoints are bot-blocked, so IDs cannot be scraped. What worked: probe a batch of
  candidate IDs with curl, keep the 200s, composite them into one contact sheet and Read that
  single image to see the subjects. Pexels is JS-rendered and returns nothing. Openverse works
  and is licence-clean but returns amateur Flickr work that does not look expensive enough.
- **When the brief is "showcase the work", crawl every gallery subpage.** 2026-08-05, on
  Paysagiste Envert: *"cest un site qui doit mieux showcase the work they already did."* The
  homepage exposed 3 template stock slides; the 12 gallery subpages held **94 real
  photographs**. The skill's "never crawl subpages" budget rule is about avoiding wasted
  fetches, and it is wrong for this brief specifically. Fetch them all, then **composite 30 to
  40 thumbnails into one contact sheet and Read that single image**, which costs one image read
  instead of forty.
- **Sourced stock is a stand-in for an archive you have not found yet.** The v3 Unsplash photos
  were deleted at v4 because the prospect's own flowering gardens did the same job and doubled
  as proof of work. Look for their archive before reaching for stock.
- **Trim aggressively, it is a mockup.** 2026-08-05, mid-build: *"Non pas besoin de toutes les
  photos cest juste un mockup. Choisis les plus belles."* Thirteen processed images were cut to
  eight while he was watching. Pick the best few rather than showing everything found.
- **Les avis doivent défiler, pas s'aligner.** 2026-08-05: *"Selectionne des avis pertinanat
  que tu peux fair defiler."* Deux blocs de citation côte à côte se lisent comme une liste;
  un rail horizontal avec flèches, `scroll-snap`, retour au début en fin de course et une
  avance automatique qui s'arrête au survol se lit comme une fiche vivante. Sur Paramédika la
  **carte de note ouvre le rail** et les citations suivent, ce qui donne trois éléments réels
  au lieu de deux et évite d'en inventer.
  **Quand les avis complets manquent, ne pas remplir le rail.** Seuls deux avis Paramédika
  sont récupérables entiers sur 429, les autres sont coupés par un «read more». Un rail court
  et vrai vaut mieux qu'un rail plein et faux, et coller la fiche Google réglait tout sur
  Divine.
- **La typo de Divine avec la ville en couleur, redemandée explicitement.** 2026-08-05:
  *"Inspire toi de la police du texte de divine avec la ville dans une autre couleur."*
  Ce que cela veut dire concrètement: **Manrope en famille unique**, titres en 800 avec
  `letter-spacing:-.035em`, et **le nom de la ville détaché du reste du titre**, en serif
  italique léger et dans la couleur de marque. Le reste du titre ne prend aucune couleur.
- *(Add confirmed wins here.)*

- **Marquer la maquette au nom de S-WEB Agency, sur tous les sites.** 2026-08-05, sur
  Paysagiste Beaudoin: *"ajoute toujours au demo que cest fait pr S-WEB AGENCY et que cest
  notre propriete (a ajouter au skill)"*. Le contexte comptait: *"Je ne veux pas qu'il puisse
  l'utiliser."* La règle et ses trois marques sont dans SKILL.md, juste avant l'étape 5.
  Ce n'est pas une note éditoriale au sens banni, c'est une mention de propriété.
- **Un prospect dont le site est tenu par la famille se gagne sans critiquer le site actuel.**
  Même message: *"quelqu'un de sa famille s'en occupe actuellement et il ne veut pas blesser
  cette personne."* Donc aucune comparaison, aucune allusion à l'ancien site sur la page ni
  dans le message de livraison au propriétaire. L'argument est la maquette elle-même.
- **Une calculatrice dont le taux est laissé vide vaut mieux qu'un taux d'exemple.** Même
  build. Un taux prérempli est un nombre inventé sur une offre de financement, ce qui est la
  pire catégorie. Champ vide, grande ligne qui affiche le montant et la durée en attendant, et
  le calcul qui se déclenche dès la saisie. En prime, taper le taux en direct devant le
  propriétaire est un bon moment de démo.

- **Quand le brief vient de la cliente en personne, il écrase tout ce qui a été déduit du
  site.** 2026-08-05, Paramédika: trois maquettes bâties depuis leur site ont été remplacées
  par une quatrième bâtie depuis sa parole. Palette, référence, équipe et fonctions venaient
  d'elle. **Consigner le brief dans un fichier du dossier prospect** avant de construire,
  avec ce qui est confirmé, ce qui est à confirmer, et ce qui devient inutilisable.
- **Un changement d'équipe se traite par grep, pas de mémoire.** Même build: la médecin et
  l'infirmière sont parties. Les noms étaient dans le HTML, dans le dictionnaire anglais et
  dans un fichier d'assets. Vérifier par `grep -ci` sur chaque nom dans le fichier livré.
- **Une section équipe sans noms fournis se construit sans aucun nom.** Rôles génériques et
  portraits en aplat. Ne jamais combler avec un prénom plausible.

- **Il peut demander des photos de banque, et alors on en met. Mais uniquement sous licence
  vérifiée.** 2026-08-05, Paramédika: *"remplace par une photo que tu as trouvé sur
  internet... si tu peux trouver d'autres photos pour combler certaines parties du site."*
  Cela renverse la règle «jamais de stock» pour ce build, sur sa demande. Ce qui ne se
  renverse pas: **une image prise au hasard sur un site quelconque ne va jamais sur la page
  d'un client**, c'est un risque de droit d'auteur réel pour lui et pour le propriétaire.
  **La méthode qui marche:** Unsplash et Pexels bloquent l'automatisation (bot check, 403).
  **Openverse répond sans clé**: `api.openverse.org/v1/images/?q=...&license=cc0&size=large`.
  Filtrer sur **cc0**, qui autorise le commercial sans attribution. Les meilleurs résultats
  viennent de StockSnap. Toujours **fabriquer une planche-contact** et la regarder avant de
  publier, une seule lecture d'image pour tout le lot.
- **Jamais de visage de banque dans une section équipe.** Même build. Cela ferait passer des
  inconnus pour ses employées. Les portraits restent des emplacements réservés, ce qui vend
  aussi la séance photo. Les photos de banque vont dans les zones d'ambiance.
- **Un énoncé centré sur plusieurs lignes se lit comme «pas uniforme».** Même jour:
  *"c'est pas très uniforme dans les écrits... tu pourrais par exemple mettre la photo à
  droite et les écrits sur le côté."* Un bloc centré à lignes de longueurs inégales attire
  l'œil sur le déchiquetage. Deux colonnes, texte aligné à gauche, image à droite.

- **La bascule de langue va dans la barre collante, jamais dans une rangée qui défile.**
  2026-08-05, Paramédika: *"elle disparaît quand on scrolle donc on ne peut pas mettre le
  compte en anglais après."* Une rangée utilitaire non collante emporte le sélecteur avec
  elle. C'est un vrai défaut, pas un détail: la bascule est **l'argument de vente qu'il
  démontre en direct**, elle doit rester atteignable partout dans la page.
- **Une rangée utilitaire ne doit répéter aucun lien de la nav.** Même message: *"il y a des
  informations qui se doublent juste sur la ligne du bas."* La rangée du haut porte ce qui
  n'est pas dans le menu, téléphone et raccourcis, rien d'autre.
- **Le nombre d'avis se retire, la note reste.** 2026-08-05: *"retire le nombre d'avis c'est
  pas pertinent et ça peut changer tout le temps."* Cela **remplace** l'ancienne règle du
  2026-08-04 qui disait de cacher le compte seulement quand il est petit. Désormais: jamais
  de compte, la note et les étoiles suffisent.

- **Un élément qui n'apparaît pas se diagnostique par ce qu'il a en commun, pas au hasard.**
  2026-08-05, Paramédika: deux photos manquaient, et c'étaient précisément les deux seules à
  porter la classe de révélation clip-path. La troisième photo, sans cette classe, s'affichait.
  **Croiser la liste des éléments signalés avec leurs classes** trouve la cause en une
  commande, sans voir la page rendue.

## Ajouts du 2026-08-06, sur Inovo Medical

- **Le titre du héros va sur la photo, pas à côté.** *"le titre peut etre ecrit sur l'image avec
  la photo en fond."* Le panneau de couleur latéral avec la photo à côté a été rejeté, alors même
  qu'il venait de la référence qu'il avait envoyée. Ce qu'il retient d'une référence, c'est
  **texte par-dessus photographie**, pas la grille. Poser le titre sur un voile en dégradé.
- **Une bande de faits juste sous le héros se fait retirer.** *"ces informations n'ont rien a
  faire la."* Les accréditations, l'adresse et les mentions techniques appartiennent aux sections
  qui les portent déjà, pas à une rangée de rappel sous l'accueil.
- **Une liste de services gagne une description au survol.** *"Quand on passe sur les traitements
  on pourrait voir poper une petite description de ce que c'est."* Sur un prospect médical la
  description ne dit **que ce qui se passe physiquement**, jamais un résultat ni une durée. Et
  sous `@media (hover:none)` elles restent toutes visibles, sinon le téléphone perd la moitié du
  contenu.
- **Le slot reel n'est pas sacré.** *"retire le coin reel il prend de l'espace inutilement."*
  Il vend la séance vidéo, mais quand il coûte un bloc entier pour un rectangle vide, il saute.
  Un seul emplacement réservé sur une page suffit à porter l'offre.
- **Une photo posée sous un voile trop dense ne compte pas comme une photo.** Il a demandé «une
  photo pour our approach» alors qu'il y en avait déjà une, invisible sous `brightness(.66)` et
  un voile à .78. Si l'image doit se voir, le voile plafonne autour de .55 et le texte se protège
  par une ombre portée plutôt que par l'assombrissement de toute l'image.
- **Plafond de résolution StockSnap: 960px, sans contournement.** Toutes les variantes de largeur
  et le chemin `original/` renvoient 404, et la page de destination ne publie pas le fichier
  complet. Donc **jamais de héros pleine largeur avec une image StockSnap**: sur son écran de
  1356px cela fait déjà 1,4x, soit le flou qu'il avait reproché sur Maro. Cadrer la bande dans le
  conteneur et laisser une cellule de couleur prendre le reste.

## Ajouts du 2026-08-06, sur Chi Medical Aesthetics

- **Une grande surface de couleur saturée fait mal aux yeux, même claire.** *"je trouve que la
  couleur est trop claire donc ca fait mal aux yeux trouve une solution poyr ca."* Le coupable
  était un teal cyan vif (`#007F7E` vers `#4FAAA5`) étalé sur tout un héros et sur un panneau
  pleine largeur. Sa réponse au choix proposé: **teal plus foncé et moins saturé, mêmes
  surfaces**. Ce qui a marché: descendre à `#093B39` vers `#2C665F`, puis un gris-vert assourdi
  `#6E938C` et `#8FAAA4` au lieu du cyan. La couleur de marque reste, elle passe juste des
  aplats géants aux petits éléments. **Règle: échantillonner le logo donne la teinte, pas la
  luminosité ni la saturation d'un fond plein écran.**
- **Une liste de prix ne se présente pas comme un menu de restaurant.** *"pour les prix je veux
  pas un menu comme celui dun resataurant(actuel) je prefere des casses qui defillent avec les
  prix pour chauque service."* Donc: un rail horizontal de cartes, une par service, le prix en
  gros bas de carte, flèches, `scroll-snap`, avance automatique qui s'arrête au survol. Les
  rangées nom-point-prix sont mortes.
- **Avant et après veut dire un curseur qui glisse, pas deux cases côte à côte.** *"je veux
  quon est un layout qui glisse dun cote a un autre du genre pour passer du before au after et
  vice versa."* Réalisation: un `input type=range` transparent posé sur toute la zone, qui pilote
  un `clip-path:inset(0 0 0 var(--x))` sur le calque «après» et la position de la poignée. Gratuit
  au clavier et au tactile, aucun code de glisser à écrire.
- **Des bulles qui flottent doivent graviter vers le centre.** *"fais en sorte que les bulles
  gravites beaucoup plus faire le centre."* Elles étaient à 2 et 9 % des bords, elles sont
  passées entre 12 et 34 %. Il faut alors **augmenter la hauteur du panneau** pour qu'elles ne
  touchent pas le texte, pas les repousser vers les bords.
- **La pastille d'étiquette au-dessus du titre du héros se retire.** *"Retire le Medical
  aesthetics in Ottawa."* Même famille que la bande de faits d'Inovo: ce qui précède le titre
  vole de la place à ce qui compte.
- **Le texte du héros doit courir sur des lignes longues, pas être empilé sur quatre lignes
  courtes.** *"Esaaie d'ecrire le texte plus bas sur plus de longeures pour que la photo de linda
  se voit directment quand on rentre sur le site."* Le but derrière la demande est toujours le
  même: **ce qui compte doit être visible sans défiler.** Un titre centré à 15ch produit quatre
  lignes et repousse tout vers le bas.
- **Un portrait dans le héros va à côté du texte, pas dessous, et se recadre au buste.**
  *"la photo est trop longue essaie de la faire plus courte."* Choix confirmé par question:
  photo plus petite et décalée à droite du texte. **Cela nuance la règle d'Inovo du 2026-08-06**
  qui disait titre par-dessus photo: elle valait pour une photo de lieu en bande, pas pour un
  portrait détouré.
- **Une section équipe ou fondateur se construit sans photo même quand la photo existe.**
  *"Tu peux ne pas mettre de photo ici et dire que cest reserve pour le shooting quon v afaire."*
  La vraie photo est déjà dans le héros; répéter la même image ne sert à rien, alors que
  l'emplacement réservé vend la séance photo. Un seul emploi par photo.

## Ajouts du 2026-08-07, sur Enterprise Spa

- **Le nombre d'avis ne se mentionne nulle part, y compris dans un titre de section.**
  *"Ne mentionne jamais le nombre d'avis google sur un site."* Cela **durcit** la règle du
  2026-08-05, qui ne visait que la pastille de compte. Le titre «Deux avis, cinq étoiles sur
  cinq» tombait dessus et a été remplacé par «Cinq étoiles sur cinq». Rien qui compte les
  avis, ni chiffre, ni mot, ni «deux», ni «plus de».
- **La couleur du logo donne la teinte, pas forcément la bonne famille.** *"Retire le rose du
  site. J'irais plus sur du bleu comme leur site actuel."* Le rose `#E8408F` était bien
  échantillonné dans leurs deux barres de logo, et il a quand même été rejeté sur un métier de
  réparation d'équipement aquatique. **Quand le métier a une couleur naturelle évidente, elle
  bat l'échantillonnage du logo.** L'eau veut du bleu. Le logo reste la source par défaut,
  il cesse de l'être quand le résultat se bat avec le sujet.
- **Aucun certificat scanné sur une maquette.** *"Retire le certificat acredit gECKO."* Le
  document était réel, nommait le propriétaire et portait une date, et il faisait quand même
  tache: une photo de papier encadré dans une page moderne se lit comme une pièce jointe, pas
  comme un élément de design. **L'accréditation peut rester en texte si le prospect la publie
  lui-même**, l'image du diplôme non.
- **Une photo authentique mais mauvaise vaut moins qu'une photo de banque correcte.**
  *"Retire les photos qui viennent de son site precedents et trouve des photos libre de droit
  qui rendrait son site plus vivant."* Leurs deux vraies photos étaient un bloc de contrôle en
  gros plan et un spa mal cadré, prises au téléphone. **Cela nuance la règle «garder les vraies
  photos du prospect»**: elle vaut quand la photo est présentable. Quand elle ne l'est pas, on
  passe en photos libres de droit **en ambiance seulement**, et la section réalisations devient
  entièrement des emplacements réservés plutôt que d'habiller du stock en «leur travail».
- **Un titre de héros qui casse en lignes inégales se lit comme un défaut.** Il a envoyé la
  capture: *"tu vas voir que le titre n'est pas symétrique donc réécris-le."* La cause était
  `max-width:15ch` sur un titre de 52 caractères, qui produisait quatre lignes en escalier.
  Correctif: raccourcir le titre, ouvrir la mesure à ~23ch, et poser `text-wrap:balance`.
- **Il veut une photo de couverture avec des gens dedans.** *"Je veux une famille dans un spa
  ou quelque chose de ce genre-là."* À savoir avant de chercher: **aucune photo de famille en
  spa n'existe en CC0**, ni sur Openverse, ni sur StockSnap, ni sur Wikimedia. Vérifié sur une
  dizaine de requêtes. Ce qui existe et qui est bon: `Jacuzzi-g6cec77a76_1920.jpg` sur
  Wikimedia, un vrai spa en teck et eau turquoise en 1920x1285. **Wikimedia refuse un
  User-Agent générique**, il faut un UA descriptif sinon le fichier revient en page d'erreur
  de 1966 octets.

- **Un prompt d'image se juge sur son négatif autant que sur sa description.** 2026-08-07,
  Enterprise Spa: sa première génération est sortie en chalet chaleureux, guirlandes et bain de
  bois en douves, alors que le site est froid et technique. Ce qui a corrigé le tir en une passe:
  nommer le **spa acrylique moderne** avec ses sièges moulés et ses buses, exiger l'heure bleue et
  un étalonnage froid, **bannir nommément** guirlandes, lanternes, bougies, feu, lumière dorée et
  bain en douves, et **imposer le sujet dans le tiers droit avec la moitié gauche vide** pour le
  titre. Sans le négatif, tout modèle redescend vers le cliché chaleureux.
- **La pastille AI de Gemini se cadre hors champ, elle ne se retouche pas.** Une étoile claire à
  quatre branches est incrustée en bas à droite de chaque sortie. **Zoomer le coin inférieur droit
  de la source avant d'exporter**, puis choisir le recadrage pour l'exclure. Sur Enterprise Spa
  elle était à x≈2522 y≈1301 sur une source de 2752x1536, et un recadrage arrêté à y=1250 l'a
  réglée sans perdre l'image.

- **Une image générée pour une section qui parle des gens du métier se fait en mains seulement.**
  2026-08-07, Enterprise Spa: la section «L'entreprise» portait une terrasse vide, qui ne disait
  rien du travail. Remplacée par une baie technique ouverte avec les mains d'un technicien au
  multimètre, **sans visage, sans tête, sans épaules**. C'est ce qui la rend tenable: un visage
  généré dans une section qui parle de ses techniciens ferait passer un inconnu pour son employé.
  La règle du «jamais de visage de banque dans une section équipe» couvre aussi les visages générés.
- **Deux lignes de négatif obligatoires sur toute image d'équipement:** aucun texte, logo,
  étiquette ni plaque de série, sinon le modèle écrit des noms de marque inventés sur le matériel
  et cela met un faux logo sur le site d'un client. Et aucune rouille, moisissure ni pièce cassée,
  parce que la section vend la compétence, pas la panne.
- **La pastille Gemini se localise par balayage de luminance, pas à l'œil, et se sort par le
  cadrage.** Même jour: une première retouche par recopie de pixels voisins a laissé un fantôme,
  le centre estimé à vue était à 44px du vrai. La bonne méthode est de prendre le pixel le plus
  lumineux de la zone, puis de choisir un recadrage qui exclut la pastille avec une marge. Sa
  luminance varie beaucoup d'une sortie à l'autre, 123 sur l'une contre bien plus sur une autre,
  donc **chercher un maximum local, jamais un seuil absolu**.
- **Un visuel destiné au panneau scrubé se vérifie sous un masque circulaire avant livraison.**
  Le panneau démarre à 200px de rayon et à 86 % d'échelle, donc tout ce qui compte doit tenir
  dans le cercle inscrit du carré. Une seule lecture d'image le prouve.


## Ajouts du 2026-08-09, sur Sarah Spa Esthétique

- **Quand il envoie des références, il veut la structure, pas la palette.** *"C'est pas tellement
  les couleurs dont je veux que tu t'inspires. C'est vraiment beaucoup plus le côté moderne et
  épuré qui casse du site web IA classique."* Il avait envoyé trois captures (un site de vin noir
  à bords déchirés, un template skincare taupe, un site de soins capillaires en blocs pastel).
  Ce qu'il fallait en tirer: nav à logo centré, bandeau défilant, titres de section centrés,
  blocs pleine largeur qui alternent aplat et photographie, micro-capitales très espacées.
  **Poser la question tôt évite de refaire la palette**: la première passe avait supposé qu'il
  fallait reprendre le taupe et le pastel.
- **Ni blanc, ni crème, en fond de page.** Deux refus successifs le même jour: *"le fond blanc ne
  donne pas bien et ça ne semble pas assez moderne"*, puis, après passage sur une vraie crème,
  *"finalement le crémeux n'est pas mieux"*. Ce qu'il a retenu à la place: **des champs de couleur
  plats qui alternent** au lieu d'un fond unique. Blanc légèrement verdi, un champ teal pâle, un
  champ blush, et les blocs foncés dans la couleur du logo. La couleur vient de l'alternance, pas
  du canevas. C'est la leçon HURR, et elle règle aussi le reproche du «pas assez moderne».
- **Le pied de page va dans la couleur du logo.** *"Pour le bas du site où y a les heures et les
  réseaux on ira sur la couleur du logo aussi."* L'espresso neutre y a été refusé.
- **Il a validé le serif d'affichage, après l'avoir rejeté deux fois.** Question posée directement
  en lui rappelant Maro et Divine, réponse *"serif d'affichage, comme les refs"*. Donc la règle
  n'est pas «jamais de serif», c'est **jamais de serif d'affichage dans le combo AI luxury**
  (serif léger géant plus crème plus champagne plus nav foncée). Un serif dense comme Prata, sur
  une page à blocs colorés, passe.
- **Il accepte de jeter les vrais visuels du prospect quand ils sont mauvais.** *"Nous pouvons ne
  pas utiliser les photos et vidéos qui sont sur son site actuel, c'est moche de toute façon."*
  Même famille qu'Enterprise Spa. Ce qui ne change pas: le stock et le généré restent en ambiance,
  la section sur la personne garde un emplacement réservé sans visage, et chaque image qui n'est
  pas d'elle porte la légende «photo temporaire, séance photo professionnelle incluse».
- **Il génère volontiers sur Gemini si on lui donne le prompt.** *"Sinon je vais générer sur gemini
  si tu me donnes le prompt de ce dont tu as besoin."* Les deux prompts livrés (épilation au
  spatule, microblading au brow) ont donné des images utilisables du premier coup, en 2048x2048.
  Recette qui a marché, identique à Enterprise Spa: cadrage serré nommé, mains gantées seulement,
  aucun visage entier, et un négatif explicite contre le texte, les logos, la rougeur et le
  registre médical.
- **Chercher les fichiers avant de les demander, mais chercher large.** Un `find -newermt` limité à
  Downloads, Bureau et Images n'a rien renvoyé alors qu'ils y étaient une demi-heure plus tard.
  Ce qui marche: `Get-ChildItem -Recurse` sur Downloads, OneDrive, Pictures, Documents et Desktop,
  trié par `LastWriteTime` décroissant, quinze premiers. Les fichiers Gemini gardent leur nom
  `Gemini_Generated_Image_*.png`.
- **La pastille Gemini ne se trouve pas par maximum de luminance quand le fond est clair.** La
  méthode d'Enterprise Spa a échoué ici: sur une serviette crème et un rideau surexposé, le pixel
  le plus lumineux de la zone est le décor, pas la pastille. Ce qui marche: **repérer la pastille
  sur une vignette, convertir en coordonnées source, et recadrer largement au-dessus.** Sur deux
  sources 2048x2048 elle était vers (1805, 1795), un carré de 1760 pris en (0,0) la sort avec de
  la marge et garde tout le sujet. Vérifier par une seule lecture d'image après recadrage.

## Ajouts du 2026-08-10, sur Bauduy Roofing

- **Une vidéo générée ne s'accélère pas, elle se coupe.** *"La video vers la fin a des
  incompatibilite donc juste prend les 6 premieres seconde et pas besoin de le mettre en vitesse
  x2."* Le `setpts=0.78*PTS` avait été choisi pour gagner un quart des octets, et il a été vu tout
  de suite. **Deux règles séparées:** la fin d'une sortie Veo dérive, donc on regarde les dernières
  secondes avant de livrer et on coupe ce qui déraille, et **on ne modifie jamais le tempo d'un
  plan filmé** pour tenir un budget de poids. Le poids se règle au recadrage, à la durée et au crf.
- **La qualité de la vidéo passe avant le poids du fichier.** *"je veux que la qualite de la video
  soit optimal parce cest flou sur le sit actuelle."* Le crf 33 de la première passe donnait
  520 kbit/s sur un plan de drone plein de feuillage, ce qui est très en dessous. Passé à **crf 23,
  1,8 Mbit/s**, et le fichier livré est monté de 1,37 à **2,40 Mo**. Il ne s'en est pas plaint et
  c'est très loin des limites de courriel. **Le plafond de 1,5 Mo du skill vaut pour des images,
  pas pour un héros vidéo.**
- **Garder la pleine hauteur plutôt qu'un 16:9 quand on recadre pour sortir une pastille IA.**
  Le héros est en `object-fit:cover`, donc le navigateur recadre déjà verticalement: livrer
  1120x720 au lieu de 1120x630 rend 90 lignes de pixels gratuites. Le format de la source n'a pas
  à être celui de l'affichage.
- **La pastille Veo se localise à l'œil sur un zoom du coin, pas par maximum de luminance.** Même
  échec qu'à Sarah Spa: sur un plan de drone, l'herbe éclairée et le ciel battent la pastille en
  luminance, et le maximum sautait de (1036,603) à (1279,640) selon l'image. Ce qui marche:
  `crop=300:220:980:500,scale=2x` sur cinq images en une planche, la pastille saute aux yeux et se
  situe à (1160, 599) avec un rayon de 23 px, stable d'un bout à l'autre du plan.
- **Un prix remporté et une offre de référencement se montrent en haut du site, pas seulement dans
  le héros.** *"cest un gros outil marketing ca doit se voir tres rapidement quand on rnetre sur
  le site, le referenement et les 100$ aussi doivent se voir, ca pourrait etre un un trait
  publicite aen haut du site comme sur la pluspart des sites."* Réalisation: une **bande promo
  défilante** au-dessus de la barre collante, trois messages en boucle, et le badge du héros passé
  d'un filet de 13 px à un panneau avec médaille, «TOP 10» en 30 px et la source du classement.
  À proposer par défaut dès qu'un prospect a un prix, un classement ou une prime de référence.
- **Les réalisations défilent en continu, elles ne sautent pas d'une page à l'autre.** *"pour les
  realisation je veux un effet defilant pour les photos et un rendu plus classe."* Cela **nuance
  la règle du 2026-08-05** qui demandait quatre carrés avançant d'une page entière: le rail à
  flèches convient aux avis, pas aux photos. Ce qui a marché: marquee infinie, deux copies
  identiques et `translateX(-50%)`, tuiles 4:5 de 306 px, **une tuile sur deux décalée de 34 px
  vers le bas**, dégradés de masque aux deux bords pour que les photos entrent et sortent en
  fondu, légende qui monte au survol, et arrêt au survol. Le décalage vertical et le masque sont
  ce qui fait le «plus classe», pas la taille des images.
  **Piège:** avec `gap` sur la piste, `-50%` rate d'un intervalle. Mettre l'écart en
  `padding-right` sur chaque tuile et laisser la piste sans `gap`.
- **Une photo de moins de 900 px ne se pose pas en bande pleine largeur.** Il a renvoyé la capture
  de la bande de bardeau `img_0804` à 820 px étirée sur tout le conteneur: *"sur le deuxieme screen
  je veux que tu retirs ctte photo."* Même famille que le plafond StockSnap d'Inovo. La bande
  décorative pleine largeur est le pire emploi possible d'un fichier court, parce que rien ne la
  justifie.
- **Pas de photo dans la colonne d'information du formulaire.** *"Retire la photo a lafin du site
  ua niveau du formulaire."* La colonne porte le téléphone, le courriel et le territoire; une image
  en bas de liste n'ajoute rien et rallonge la page juste avant le pied de page.

## Ajouts du 2026-08-11, sur TOP Construction Design

La session la plus longue du skill, une quinzaine de passes correctives sur un seul
prospect. La leçon dominante n'est pas esthétique: c'est qu'il travaille désormais par
**passes courtes et cadrées**, et qu'il exige un compte rendu vérifiable à chaque fois.

### Sa méthode de travail, à respecter sans qu'il la redemande

Il ouvre maintenant chaque demande par le même préambule de règles. Elles sont dans
`SKILL.md`, mais l'esprit tient en une phrase: *"Ne fais QUE ce que la passe demande.
Aucune amélioration spontanée, aucun refactoring opportuniste."*

- **Compter les balises avant et après, et s'arrêter en cas d'écart.** Sa formulation:
  *"Si un compte ne correspond pas, ARRÊTE et signale-le sans tenter de réparer."*
  Il ne veut pas d'une réparation improvisée par-dessus un dégât non compris.
- **Signaler les contradictions plutôt que de trancher en silence.** Plusieurs de ses
  consignes décrivaient un état du fichier déjà dépassé par la passe précédente
  (un dégradé latéral qui n'existait plus, deux déclarations `.team-card p` dans l'ordre
  inverse de sa description, un `.f-bottom` absent de ses deux listes). À chaque fois,
  dire ce qu'on observe, appliquer l'intention, expliquer l'écart.
- **Signaler aussi ce qu'on n'a pas pu faire.** Il accepte très bien un « impossible avec
  ces valeurs, voici pourquoi et voici l'option »: il a gardé la malle blanche dans le
  héros après une démonstration chiffrée.

### Ce qu'il rejette, en design

- **L'uniformité lue comme automatique.** *"Cette uniformité parfaite est une signature
  de génération automatique."* Padding identique partout, `.wrap` à 1280px partout, même
  gap partout: il veut un rythme irrégulier mais justifiable, et des largeurs alternées
  (1280 / pleine largeur / 880).
- **Une échelle dont un seul cran porte tout.** *"Une échelle ne sert à rien si un seul
  de ses crans porte tout le contenu."* Il a compté lui-même: 20 usages de `--t-small`,
  16 de `--t-micro`, 2 de `--t-body`. Un cran, un rôle.
- **`--t-micro` sur des minuscules.** *"Onze pixels ne sont lisibles qu'en capitales
  espacées, sur une ligne courte."* Règle générale, à appliquer partout.
- **L'italique dorée répétée.** *"Répétée, elle cesse d'être un accent et devient un
  tic."* Un seul mot ou groupe de mots en serif italique par page, dans le h1 du héros.
- **Un mot fantôme qui répète son titre.** *"Un mot fantôme n'est justifié que s'il porte
  une information que le titre ne porte pas."* Le fantôme porte la catégorie, le titre
  porte la promesse. Règle absolue: aucun mot du fantôme ne doit apparaître dans son h2.
- **Un centrage isolé.** *"Un centrage qui réapparaît au hasard d'une section sur trois
  se lit comme une inconséquence."* Le héros centré est la seule exception admise.
- **La pastille d'accroche dans le héros.** *"Cette pastille est le tic visuel n°1 des
  sites d'entrepreneurs, elle tue l'effet haut de gamme dès la première seconde."*
  Estimation gratuite sous 48h en badge: supprimé.
- **Trois appels à l'action dans un héros.** *"C'est un de trop."*
- **Un écran d'introduction noir.** *"Un effet qui sonne emprunté"* sur un entrepreneur
  en rénovation. Retiré entièrement, il retarde le numéro de téléphone.
- **Un décalage arbitraire.** *"Un décalage n'est perçu comme voulu que s'il obéit à une
  règle visible."* Les décalages de galerie sont des multiples d'une seule unité.

### Ce qu'il veut, en design

- **Le contraste par le haut, pas seulement par le bas.** Titres de section en graisse
  500 plutôt que 800, corps à 16px, accroches à 21px. *"Un h2 en 800 à 58px est ce qui
  fait bloc de constructeur; en 500 à 40px, ça devient éditorial."*
- **Le texte du héros petit et long.** *"Une police plus petite et que ce soit plus en
  longueur sans pour autant aller au bout."* Résultat retenu: 34px maximum, mesure de
  34ch, deux lignes de longueur quasi identique.
- **Le logo fondu dans la photo du héros.** `filter:brightness(0) invert(1) drop-shadow()`
  sur un PNG détouré, header transparent au-dessus de l'image, retour à l'opaque au
  défilement avec 40px d'hystérésis.
- **Le téléphone dans l'en-tête, pas un bouton de formulaire.** *"Un entrepreneur en
  rénovation se fait appeler, pas remplir un formulaire."* Sur mobile, c'est le bouton
  Soumission qui disparaît, jamais le téléphone.
- **Des faits vérifiables plutôt que des statistiques rondes.** *"Un numéro de licence à
  10 chiffres est mille fois plus crédible qu'un 100%."* Les 1 / 4 / 100% ont été
  remplacés par la licence RBQ, les numéros de kiosque et l'adresse.
- **Une section équipe plutôt que des avis vides.** *"Trois cartes Exemple vides, c'est
  l'aveu qu'il n'y a pas de contenu."* Quand le prospect n'a aucun avis Google, nommer
  les gens est plus honnête et plus différenciant. Le badge Google se réduit à une ligne
  sous le formulaire.

### Sur les données du client

- **Aucune année de fondation sans confirmation.** *"N'écris AUCUNE année de fondation:
  elle n'est pas vérifiée."* Et supprimer « récemment établie », qui affaiblit.
- **Aucune mention non vérifiée**, même plausible: « salle d'exposition » a été retiré
  partout parce que rien ne le confirmait.
- **Les vraies photos du client avant tout.** Ses fichiers nommés n'existaient pas, mais
  leur WordPress hébergeait une quarantaine de photos de chantier réelles, dont des
  exports Instagram. Une planche-contact en une seule lecture d'image a suffi à trier.
  *"AUCUNE image ne doit apparaître deux fois sur la page. C'est le signal le plus
  visible d'une démo vide."*
- **Pas de faux avant/après.** *"Supprime la section entière plutôt que de simuler un
  avant/après."* Un panneau placeholder du côté « avant » ne compte pas comme une paire.

## Ajout du 2026-08-12, sur Salon Amina beauté

- **Il choisit trois effets de mouvement quand la question en propose deux. Troisième fois.**
  Sarah Spa le 2026-08-09, Salon Amina et DMcosmetique le 2026-08-12: la question est posée «deux maximum» et
  il coche trois cases. Donc **le plafond de deux du skill est un plancher pour lui**, pas une
  limite. Ce qui reste vrai: les trois effets doivent occuper des zones différentes pour ne pas
  se battre. Sur ce build, curseur global, marquee sur la galerie, titre assemblé dans le héros.
  Ne pas ramener à deux sans le lui dire.

## Ajouts du 2026-08-12, passe finition de DMcosmetique

- **Une mesure géométrique ne prouve pas qu'un contenu est visible.** Le h1 du héros est resté
  invisible deux passes entières: ses lignes vivaient sous un masque `overflow:hidden` et
  `getBoundingClientRect` sur le h1 renvoyait quand même une hauteur correcte, parce que ce sont
  les blocs de ligne qui occupent l'espace. **Dès qu'un contenu vit sous un masque, comparer la
  position de l'intérieur à celle du masque**, ou regarder une capture. Les captures d'écran du
  panneau fonctionnent désormais, et c'est ce qui l'a trouvé.
- **Le panneau ne décode aucune image.** Il sert la page en `data:`, donc `assets/*.jpg` ne
  résout pas et `naturalWidth` vaut 0 partout. Les captures montrent typographie, mise en page
  et couleurs, jamais les photos. Le dire à chaque livraison.
- **Un élément posé après le `<script>` qui le cherche renvoie `null` et tue tout le reste du
  script.** Ici la barre collante mobile a fait disparaître les 29 images d'un coup, filet de
  sécurité compris puisqu'il vivait dans le code devenu mort. Placer les éléments fixes avant le
  script, et garder les `getElementById` de plomberie.
- **`/products.json?limit=250` répond sur un myshopify.com** et donne tout le catalogue avec les
  prix, les collections et les images CDN. À essayer systématiquement sur un prospect Shopify.
- **Vérifier à pleine résolution avant de conclure sur des photos produit.** Les codes
  fournisseur et les filigranes d'un tiers ne se voient pas sous 200 px. Sur ce prospect, une
  partie du catalogue portait le filigrane `Mengsha-Keym` et des références de gros incrustées.
- **Quand un chiffre demandé n'est pas vérifiable, en faire un champ éditable**, jamais une
  valeur plausible. Confirmé une troisième fois, après Beaudoin et Salon Amina.
- **Un audit de contraste se fait en parcourant le DOM, pas à l'œil.** Trois échecs réels sur ce
  build, dont un texte à 1,28 de ratio, et aucun n'était visible en relisant le CSS: ils venaient
  de restes de versions précédentes où la section était sombre.

- **Une page qui ne fait pas assez soignee se diagnostique en comptant les combinaisons
  taille / graisse / famille / casse rendues.** Sur DMcosmetique: 19 tailles et 30 combinaisons,
  dont neuf tailles entre 12 et 16,5px et 14,5px en quatre versions. Au-dela d une dizaine de
  combinaisons, ce n est plus une echelle, c est de la derive, et cela se voit sans se nommer.
  Le correctif est une echelle courte en jetons CSS, un role par cran, verifiee par le meme
  balayage: 8 tailles pour 8 combinaisons.
- **Une reference de commerce dense sert a corriger une page epuree.** Il a envoye LUXERA Paris,
  qui a un bandeau noir, des aplats sombres et une grille de six produits. Rien de cela ne
  devait entrer. **On prend le systeme typographique, on laisse la structure**, comme pour
  Riera et vicpark avant.
  **Renverse le meme jour, voir la section suivante:** il a renvoye la meme capture en demandant
  la structure. Cette regle ne vaut que la premiere fois qu'une reference arrive.
- **Une regle d element descendant bat une regle de classe.** Le selecteur `.gbox p` (0,2,0)
  ecrasait `.gg` (0,1,0) et imposait la mauvaise taille au mot-symbole Google. Meme famille que
  le conflit de media queries de la passe 2. Invisible au grep, visible au balayage du DOM.

## Ajouts du 2026-08-12, refonte boutique de DMcosmetique

### La règle la plus importante de cette passe: une référence renvoyée deux fois est un brief

À la passe 6, il envoie une capture de **LUXÉRA Paris** en parlant de typographie. Conclusion
écrite alors, et elle était juste: on prend le système, on laisse la structure. À la passe 7,
**il renvoie exactement la même capture** avec *«voici mon inspiration, fais quelque chose de
beau et luxe»*. Cette fois il voulait la structure entière, celle qui avait été écartée:
bandeau d'annonces sombre, en-tête à icônes avec compteur de panier, quatre tuiles de
catégories, grille de six produits à badges et seconde image au survol, bande promotionnelle
sombre, témoignages en trois cartes, bande Instagram, pied de page sombre en colonnes.

**La leçon:** la première fois qu'une référence arrive, elle corrige un défaut précis et on
n'en prend que le système. **Quand elle revient une seconde fois, ce n'est plus une humeur,
c'est le brief.** Ne pas rejouer la retenue de la passe précédente, et ne pas lui faire
répéter une troisième fois. Sa consigne de fond, *maison de couture, du vide, enlever plutôt
qu'ajuster*, reste vraie **à l'intérieur** de la structure demandée, pas contre elle.

### Version sombre

Il l'a demandée en une phrase, *«je veux également une version sombre de leur boutique»*.
C'est un argument de vente devant le client: on bascule les deux ambiances en un clic pendant
la présentation. Comment la faire tenir:

- **Uniquement des jetons.** `:root` porte la palette claire, `:root[data-theme="dark"]` ne
  redéfinit que des couleurs, jamais une structure. Aucun jeton défini seulement dans le bloc
  sombre.
- **Un script avant le premier rendu** qui pose l'attribut depuis `localStorage`, sinon depuis
  `prefers-color-scheme`, sinon un écran clair apparaît une fraction de seconde.
- **Quatre choses cassent en sombre et sont à vérifier à chaque fois:**
  1. un bouton sombre sur une page presque noire perd sa forme, il faut **inverser** en fond
     crème et texte sombre;
  2. une bande ou un pied de page qui partage le noir de la page a besoin d'**un filet 1px**,
     sinon la zone disparaît;
  3. **le filigrane doit changer d'encre**, une encre à 0,05 est invisible sur fond noir, il
     faut la même tuile en crème;
  4. les photos demandent un léger `brightness` en moins, sinon elles brûlent la page.

### Auditer l'existant avant de refaire

Nouvelle étape qu'il a demandée explicitement: *«tu notes tout ce qui ne fonctionne pas en le
parcourant»*, **puis** on refait. L'audit sert deux fois: il corrige la nouvelle version, et
il devient l'argument de vente devant le client. Classer par gravité, et mettre en tête ce qui
coûte une vente, pas ce qui gêne un développeur. Sur ce prospect, les cinq premiers points
étaient un titre de section qui contredisait les produits affichés, deux produits au nom
identique côte à côte, deux chiffres vides rendus en pointillés, une section d'avis annonçant
qu'il n'y en a aucun, et un bouton d'avis qui pointait vers le formulaire de rendez-vous.

### Servir la maquette en local plutôt que la donner au panneau

**Ceci corrige la limite notée plus haut le même jour** («le panneau ne décode aucune image»).
Le panneau sert la page en `data:`, donc `assets/*.jpg` ne résout jamais. **Un serveur statique
local règle tout:** une entrée dans `.claude/launch.json` qui lance
`python -m http.server <port> --directory <dossier>`, puis `preview_start` par son nom. Les
images se décodent, les polices se chargent, les captures deviennent réelles. Vérifié ici: 32
images sur 32 décodées, `naturalWidth > 0` partout.

Deux réserves sur le panneau, à connaître:

- **Il ne rend fidèlement qu'à sa largeur native.** Dès qu'on émule une fenêtre plus large, la
  capture place la page dans le coin supérieur gauche d'un cadre bien plus grand et tout
  devient minuscule. Donc: **mesurer en JS à la largeur émulée, photographier à la largeur
  native.** Le zoom CSS ne contourne pas le problème, les media queries n'en tiennent pas
  compte.
- **La capture est parfois en retard d'un pas.** Si l'image ne correspond pas à l'action qu'on
  vient de faire, redemander une capture avant de conclure à un bogue.

### Pièges techniques payés dans cette passe

- **Un sélecteur descendant nu attrape les emballages internes.** `.trust div` visait trois
  colonnes et touchait aussi le bloc de texte à l'intérieur de chacune, qui héritait d'un
  second filet et d'un second rembourrage: colonnes à 142px au lieu de 91. Écrire
  `.trust .wrap > div`. **Troisième fois qu'un sélecteur trop large frappe sur ce prospect**,
  après `.gbox p` et le conflit de media queries.
- **Cacher un encart par `translateY` seul ne le cache pas.** `#toast` en `translateY(140%)`
  avec `bottom:70px` dépassait toujours du bas de l'écran, puisque 140% de sa propre hauteur
  est inférieur à 70px. Ajouter `opacity` et `visibility`, et retarder `visibility` à la
  fermeture.
- **`getComputedStyle` pendant une transition renvoie la valeur intermédiaire.** Deux fois de
  suite, le thème sombre a paru ne pas s'appliquer alors qu'il était en train de s'animer.
  **Attendre la fin de la transition avant de conclure qu'une règle ne prend pas.**
- **Le remplissage automatique du navigateur n'émet pas d'`input`.** L'étiquette flottante
  reste alors posée sur la valeur déjà inscrite. Resynchroniser les champs au `load` et au
  `pageshow`, pas seulement sur `input`.
- **La rangée d'icônes d'en-tête déborde sous 430px.** Mot-symbole plus thème, recherche,
  favoris, panier, langue et menu demandaient 481px pour 375 disponibles. **La recherche et
  les favoris sautent en premier**, le panier, la langue et le menu portent la conversion.

### Un bloc de témoignages quand le client n'a aucun avis

La structure demandée en exige un, et le prospect n'a rien à y mettre. Ni inventer des
citations, ni afficher un état vide en pleine page comme à la passe 1. **Garder les trois
cartes dessinées, marquer chacune d'un «Exemple» discret**, et écrire sous le titre que les
emplacements se remplissent depuis leur vraie fiche Google. Le design se présente, rien de
faux n'est donné pour vrai, et le vide devient un argument de vente.
