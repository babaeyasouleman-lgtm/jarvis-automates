# External references

Repos checked against the GitHub API on 2026-07-29. Stars and last-push are real, not
taken from blog posts. All MIT licensed. Consult these for ideas; do not vendor their
code into a deliverable without checking the licence header.

## Worth installing

| Repo | Stars | Last push | Why it matters here |
|---|---|---|---|
| [bitjaru/styleseed](https://github.com/bitjaru/styleseed) | 853 | 2026-07 | Design *judgment*, not tokens. Its `engine/RULESETS.md` defines output grammars per product class; `expressive-marketing` is the one our demos belong to, and its reject-list names real AI visual tells. Already distilled into Step 3 of this skill. |
| [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) | 2,681 | 2026-07 | 49+ AI-ism pattern categories with detect / rewrite / edit-in-place modes. Broader coverage than the bundled `no-ai-slop`; worth pairing given how strongly the user reacts to AI-sounding copy. |
| [SawyerHood/dev-browser](https://github.com/SawyerHood/dev-browser) | 6,484 | 2026-07 | Full Playwright control so the agent screenshots and checks its own rendering. Directly fixes a real blocker: the built-in preview pane cannot screenshot, and it silently refuses files over ~1MB. |

## Worth reading, not installing

| Repo | Stars | Last push | Note |
|---|---|---|---|
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 51,264 | 2026-07 | The main hub. Its "Design & UI/UX" and "Writing & Prose Quality" sections are where the entries above came from. Re-check it when looking for something new. |
| [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) | 313 | 2026-06 | ~50 motion-graphics skills with a render → screenshot → verify loop. Aimed at video and WebGL, heavier than a static marketing page needs, but the verification pattern is worth copying. |
| [educlopez/ui-craft](https://github.com/educlopez/ui-craft) | 222 | 2026-07 | Design-engineering skill with 22 single-lens commands and CI gates. Overlaps StyleSeed; pick one rather than both. |
| [usaljs/usal](https://github.com/usaljs/usal) | 144 | 2026-07 | Small dependency-free scroll-animation library, Intersection Observer based. Our hand-written reveal code already does this in ~15 lines, so this is a fallback, not an upgrade. |

## Checked and rejected

- **mciastek/sal** (3,695 stars) is the library most blog posts recommend for scroll
  animation. **Last push January 2023**, roughly three and a half years stale. Do not use.
- **Business/trade website templates on GitHub.** Searched; nothing above 6 stars, all
  abandoned one-off student projects. Not a useful source. Build from the grammar in
  Step 3 instead.

## Dead end worth remembering

Awwwards and similar galleries cannot be mined by fetching them: the pages are
JavaScript-rendered, and even when text is extracted it describes the studio, not what
makes the design work. Visual inspiration has to arrive as **screenshots the user
supplies**, which the agent can actually see and analyse. ReactBits and similar
code-first sites are different: their source is readable and adaptable to plain CSS.

## Produire un PDF (soumission, devis, document client), 2026-08-06

Aucune bibliothèque PDF n'est installée sur cette machine et il ne faut pas en installer.
**Chrome headless fait le travail**, et il est déjà là:

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="C:/chemin/Sortie.pdf" "file:///C:/chemin/source.html"
```

`--no-pdf-header-footer` retire l'URL et la date que Chrome ajoute autrement en marge.
`pdftoppm` n'est pas installé non plus, donc **l'outil Read ne peut pas ouvrir un PDF ici**.

### Le vrai piège: la pagination

`@page{size:Letter;margin:0}` plus une div `.page` par feuille ne suffit pas. Si le contenu
d'une `.page` dépasse 11 pouces, Chrome la répartit sur **deux** feuilles et le document
double silencieusement. Un premier jet a rendu 6 pages au lieu de 3.

**Mesurer avant de corriger**, avec une sonde qui neutralise la hauteur fixe:

```html
<style>.page{height:auto !important}footer{margin-top:12px !important}</style>
<script>window.addEventListener('load',function(){var o=[];
document.querySelectorAll('.page').forEach(function(p,i){o.push('P'+(i+1)+'='+(p.scrollHeight/96).toFixed(2));});
document.title='NATURAL '+o.join(' ');});</script>
```

```bash
chrome --headless --virtual-time-budget=3000 --dump-dom "file:///.../probe.html" | grep -o '<title>[^<]*</title>'
```

96 pixels par pouce. Le budget utile est 11 pouces moins les marges verticales de `.page`.
Deux détails qui faussent la mesure si on les oublie: `min-height:11in` fait toujours
retourner au moins 11, donc il faut le neutraliser, et `margin-top:auto` sur le pied de page
colle celui-ci en bas, ce qui rend inutile toute mesure basée sur la position du dernier
enfant.

### Contrôle visuel

`--screenshot` avec `--window-size=816,<1056 x nb_pages>` capture tout le document d'un coup.
Le découper et le réduire en planche-contact avec System.Drawing permet de **voir les cinq
pages en une seule lecture d'image**, ce qui coûte bien moins cher que cinq captures.

### Polices

Ne pas utiliser Google Fonts dans un document destiné au PDF: si la requête échoue au moment
du rendu, Chrome intègre silencieusement une police de repli et rien ne le signale. Georgia
et Segoe UI sont sur toute machine Windows et s'intègrent proprement.

## Produire un .docx éditable, 2026-08-06

`pandoc` et LibreOffice ne sont pas installés, mais **Word 16 l'est**, et c'est ce qui permet
de fermer la boucle de vérification.

1. **Construire** avec la librairie `docx` de npm. Elle n'est pas préinstallée:
   `npm install docx` dans un dossier de travail du scratchpad, puis `node build.js`.
2. **Valider en ouvrant le fichier dans Word par COM**, ce qui est la preuve la plus forte
   qu'il n'est pas corrompu, et donne le nombre de pages réel:

```powershell
$w=New-Object -ComObject Word.Application; $w.Visible=$false; $w.DisplayAlerts=0
$d=$w.Documents.Open($chemin,$false,$true)
'{0} pages, {1} mots' -f $d.ComputeStatistics(2), $d.ComputeStatistics(0)
$d.ExportAsFixedFormat($pdfOut,17)   # 17 = wdExportFormatPDF
$d.Close($false); $w.Quit()
```

3. **Voir le rendu**: Chrome headless **ne rend pas les PDF**, la capture sort vide. Le moteur
   PDF de Windows le fait, via WinRT depuis PowerShell 5.1. Trois pièges:
   `Add-Type -AssemblyName System.Runtime.WindowsRuntime` est obligatoire sinon
   `System.WindowsRuntimeSystemExtensions` reste introuvable, `AsTask` a deux surcharges à
   distinguer (`IAsyncOperation<T>` et `IAsyncAction`), et `PdfPage` n'a pas de `Close`, c'est
   `Dispose`. Script conservé dans le scratchpad sous `pdf2png.ps1`.

### Pièges de la librairie docx

- Lettre US: `page:{size:{width:12240,height:15840}}` en DXA, sinon on obtient du A4.
- Les tableaux veulent **`columnWidths` sur le tableau ET `width` sur chaque cellule**, en DXA.
- `ShadingType.CLEAR`, jamais `SOLID`, qui rend noir.
- Pas de puce littérale: passer par une config `numbering` avec `LevelFormat.BULLET`.
- `ImageRun` exige `type:"png"`.
- `PageBreak` doit être dans un `Paragraph`.
- **Du texte blanc sur une cellule à fond clair disparaît.** Une pastille qui repose sur un
  fond coloré en CSS n'a pas d'équivalent simple en Word: colorer le texte plutôt que le fond.
- Le filigrane n'a pas d'API simple. Dans Word c'est Création puis Filigrane, un clic.

## E1. Elyse Residence, immobilier de luxe (familles CHA et PRO)

- **Source:** https://elyse-residence-dev.webflow.io/ , envoyee le 2026-08-20 pour Venturia.
- **Monde:** vitrine nocturne editoriale. Champ quasi noir, serif d'affichage creme, photo qui porte toute la lumiere.
- **Polices reelles, relevees dans leur CSS:** PP Fragment Serif et PP Fragment Glare
  (Pangram Pangram, **commerciales**) plus Inter 28pt en Thin a Regular.
  **Equivalent libre retenu: Instrument Serif** + son italique.
- **Pile:** GSAP + ScrollTrigger + SplitText + Splide. **Zero interaction native Webflow**, tout est ecrit a la main.

**Dispositifs a prendre:**
- Le **mot-symbole geant a cheval sur la photo**, qui deborde des deux bords de l'ecran.
- Le **titre empile roman et italique alternes**, une ligne droite, une ligne italique.
- Les **chiffres geants disperses** en composition asymetrique, chacun avec son unite en italique et sa legende en sans minuscule.
- Le **titre geant qui traverse par-dessus une rangee de trois photos**, type devant, photos derriere.
- Les **cartes de verre numerotees** posees sur un fond photo.
- La **barre de nav qui se retracte** pendant une section epinglee.

**Effets de defilement, valeurs exactes de leur code:**
- **Masque de lignes et de caracteres** (SplitText `mask:'lines'` et `mask:'chars'`): le texte monte de derriere un masque. Stagger 0,1 par lettre sur le mot-symbole, duree 2.
- **Parallaxe scrubee differentielle du heros:** photo `yPercent +30` et `scale 1 -> 1,1`, titre `yPercent -50` et `opacity 1-p`, colonne droite `yPercent -30` et `opacity 1-p*1,5`.
- **Revelation en 30 tranches horizontales:** un `linear-gradient(0deg)` de 30 bandes, chacune avec sa propre progression, pose en `mask-image` et pilote au defilement. **Le plus distinctif du lot.**
- Compteurs de 0 en 2 s avec `snap`.

**Attention.** C'est ce qui approche le plus la combinaison bannie (serif d'affichage geant plus nav foncee). Ce qui la sauve: aucun creme en fond, aucun champagne dore, et la photo reelle qui porte la page. **Le mot-symbole geant ne peut pas etre un `h1`**, sinon le plafond de 46px saute: le declarer decoratif et `aria-hidden`, et garder un vrai `h1` sous le plafond.

**Piege mesure, valable pour tout mot-symbole debordant:** `text-align:center` **ne centre pas** un contenu plus large que son bloc, il le pousse a droite seulement. Passer le conteneur en `display:flex; justify-content:center`, et poser `flex:0 0 auto` sur les lettres, faute de quoi elles se compressent pour tenir dans l'ecran au lieu de deborder.
