/*
 * S-WEB Agency, générateur de documents Word.
 *
 *   node build_docx.js spec.json sortie.docx
 *
 * Le spec JSON décrit le document; ce fichier ne contient aucun contenu client.
 * Voir MODELES.md pour la forme des blocs.
 *
 * Dépendance: npm install docx   (dans le dossier de travail, pas globalement)
 */
const fs = require("fs");
const path = require("path");

/* docx vit dans le skill lui-même, pas dans le dossier client.
   Un node_modules posé dans un dossier client sous OneDrive finit par disparaître, et le
   script échoue alors sans raison apparente. Node résout depuis le dossier du script, donc
   le premier require suffit; le repli sur le dossier de travail reste par sécurité. */
let D;
try {
  D = require("docx");
} catch (e) {
  try {
    D = require(path.join(process.cwd(), "node_modules", "docx"));
  } catch (e2) {
    console.error("La librairie docx est introuvable.");
    console.error("Lancer :  cd " + path.join(__dirname, "..") + "  &&  npm install docx");
    process.exit(1);
  }
}
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, BorderStyle, ShadingType, PageBreak,
  Header, Footer, PageNumber, LevelFormat, VerticalAlign,
} = D;

const INK = "1A1A1E", ORANGE = "FF5A1F", SOFT = "F6F4F1", DIM = "6B6660", LINE = "DEDAD4";
const SERIF = "Georgia", SANS = "Segoe UI";

const specPath = process.argv[2];
const outPath  = process.argv[3];
if (!specPath || !outPath) { console.error("usage: node build_docx.js spec.json sortie.docx"); process.exit(1); }
const S = JSON.parse(fs.readFileSync(specPath, "utf8"));
const LOGO = S.logo || path.join(__dirname, "..", "assets", "sweb-logo.png");

/* ---------- primitives ---------- */
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: none, bottom: none, left: none, right: none,
                    insideHorizontal: none, insideVertical: none };
const hair = (color = LINE, size = 4) => ({ style: BorderStyle.SINGLE, size, color });

function txt(text, o = {}) {
  return new TextRun({
    text, font: o.font || SANS, size: o.size || 21, bold: !!o.bold,
    color: o.color || INK, allCaps: !!o.caps, characterSpacing: o.spacing,
  });
}
/* **gras** dans une chaîne devient un run en gras */
function rich(s, o = {}) {
  const out = [];
  String(s).split(/(\*\*[^*]+\*\*)/g).forEach((piece) => {
    if (!piece) return;
    const m = piece.match(/^\*\*([^*]+)\*\*$/);
    out.push(m ? txt(m[1], Object.assign({}, o, { bold: true, color: o.boldColor || o.color || INK }))
               : txt(piece, o));
  });
  return out.length ? out : [txt("", o)];
}
function para(runs, o = {}) {
  return new Paragraph({
    children: Array.isArray(runs) ? runs : [runs],
    spacing: { before: o.before || 0, after: o.after === undefined ? 100 : o.after },
    alignment: o.align, border: o.border,
  });
}
const spacer = (n) => new Paragraph({ children: [], spacing: { after: n } });
const h1 = (t) => para(rich(t, { font: SERIF, size: 38, bold: true }), { before: 120, after: 140 });
const h2 = (t) => para(rich(t, { font: SERIF, size: 26, bold: true }), { before: 260, after: 60 });
const lbl = (t) => para(txt(t, { size: 17, bold: true, color: ORANGE, caps: true, spacing: 40 }), { after: 70 });
const sub = (t) => para(rich(t, { size: 19, color: DIM }), { after: 120 });
const note = (t) => para(rich(t, { size: 18, color: DIM, boldColor: DIM }), { before: 90, after: 60 });
const puce = (t) => new Paragraph({ children: rich(t, { size: 20 }),
  numbering: { reference: "puces", level: 0 }, spacing: { after: 70 } });

function cell(children, o = {}) {
  return new TableCell({
    width: { size: o.w, type: WidthType.DXA },
    children: Array.isArray(children) ? children : [children],
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
    margins: { top: o.mt === undefined ? 90 : o.mt, bottom: o.mb === undefined ? 90 : o.mb,
               left: o.ml === undefined ? 0 : o.ml, right: o.mr === undefined ? 0 : o.mr },
    verticalAlign: o.valign || VerticalAlign.TOP,
    borders: o.borders,
  });
}
function tbl(rows, widths) {
  return new Table({
    rows, columnWidths: widths,
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    borders: noBorders, layout: D.TableLayoutType.FIXED,
  });
}

/* ---------- blocs ---------- */
const B = {};

B.h2 = (b) => [h2(b.texte)];
B.sub = (b) => [sub(b.texte)];
B.para = (b) => [para(rich(b.texte, { size: 20, color: b.gris ? DIM : INK }), { after: 140 })];
B.note = (b) => [note(b.texte)];
B.puces = (b) => b.items.map(puce);
B.saut = () => [new Paragraph({ children: [new PageBreak()] })];
B.espace = (b) => [spacer(b.hauteur || 220)];

/* tableau de lignes: description à gauche, montant à droite */
B.lignes = (b) => {
  const W1 = 7680, W2 = 2400;
  const rows = [];
  if (b.entete) {
    const bd = { top: none, bottom: hair(INK, 6), left: none, right: none };
    rows.push(new TableRow({ children: [
      cell(para(txt(b.entete[0], { size: 16, bold: true, color: DIM, caps: true, spacing: 40 }), { after: 0 }),
           { w: W1, borders: bd, mb: 70 }),
      cell(para(txt(b.entete[1], { size: 16, bold: true, color: DIM, caps: true, spacing: 40 }),
                { align: AlignmentType.RIGHT, after: 0 }), { w: W2, borders: bd, mb: 70 }),
    ]}));
  }
  b.items.forEach((it) => {
    const bd = { top: none, bottom: hair(), left: none, right: none };
    const left = [para(rich(it.titre, { size: 21, bold: true }), { after: it.desc ? 40 : 0 })];
    if (it.desc) left.push(para(rich(it.desc, { size: 18, color: DIM, boldColor: DIM }), { after: 0 }));
    rows.push(new TableRow({ children: [
      cell(left, { w: W1, borders: bd, fill: it.fill ? SOFT : undefined, ml: it.fill ? 120 : 0 }),
      cell(para(txt(it.prix || "", { size: 21, bold: !!it.gras }), { align: AlignmentType.RIGHT, after: 0 }),
           { w: W2, borders: bd, fill: it.fill ? SOFT : undefined, mr: it.fill ? 120 : 0 }),
    ]}));
  });
  if (b.total) {
    const bd = { top: hair(INK, 12), bottom: none, left: none, right: none };
    rows.push(new TableRow({ children: [
      cell(para(txt(b.total.libelle, { font: SERIF, size: 26, bold: true }), { after: 0 }), { w: W1, borders: bd, mt: 140 }),
      cell(para(txt(b.total.montant, { font: SERIF, size: 26, bold: true }), { align: AlignmentType.RIGHT, after: 0 }),
           { w: W2, borders: bd, mt: 140 }),
    ]}));
  }
  return [tbl(rows, [W1, W2])];
};

/* encadré de prix mis en avant */
B.encadre = (b) => [tbl([new TableRow({ children: [
  cell([ para(txt(b.libelle, { size: 18, bold: true, color: DIM, spacing: 40 }), { after: b.sous ? 30 : 0 }),
         ...(b.sous ? [para(txt(b.sous, { size: 18, color: DIM }), { after: 0 })] : []) ],
       { w: 7680, fill: SOFT, ml: 200, mt: 200, mb: 200,
         borders: { top: none, bottom: none, right: none,
                    left: { style: BorderStyle.SINGLE, size: 18, color: ORANGE } } }),
  cell(para(txt(b.montant, { font: SERIF, size: 36, bold: true }), { align: AlignmentType.RIGHT, after: 0 }),
       { w: 2400, fill: SOFT, mr: 200, mt: 200, mb: 200, valign: VerticalAlign.CENTER, borders: noBorders }),
]})], [7680, 2400])];

/* grille comparative de paliers */
B.paliers = (b) => {
  const n = b.colonnes.length;
  const first = 10080 - n * 2160;
  const W = [first].concat(b.colonnes.map(() => 2160));
  const bdH = { top: none, bottom: hair(INK, 8), left: none, right: none };

  const headCells = [cell(para(txt(""), { after: 0 }), { w: W[0], borders: bdH })];
  b.colonnes.forEach((c) => {
    const inner = [];
    if (c.reco) {
      inner.push(para(txt("▲ RECOMMANDÉ", { size: 14, bold: true, color: ORANGE, spacing: 30 }),
        { align: AlignmentType.CENTER, after: 40 }));
    }
    inner.push(para(txt(c.nom, { font: SERIF, size: 22, bold: true }), { align: AlignmentType.CENTER, after: 30 }));
    inner.push(para(txt(c.prix, { size: 18, bold: true, color: ORANGE }), { align: AlignmentType.CENTER, after: 0 }));
    headCells.push(cell(inner, { w: 2160, borders: bdH, fill: c.reco ? SOFT : undefined, ml: 80, mr: 80 }));
  });
  const head = new TableRow({ children: headCells });

  const bd = { top: none, bottom: hair(), left: none, right: none };
  const rows = b.lignes.map((l) => {
    const cells = [cell(para(txt(l.nom, { size: 18, bold: true }), { after: 0 }),
      { w: W[0], borders: bd, mt: 70, mb: 70 })];
    l.valeurs.forEach((v, i) => {
      const oui = v === "oui" || v === "✓";
      const non = v === "non" || v === "—";
      const affiche = oui ? "✓" : (non ? "—" : v);
      const couleur = oui ? ORANGE : (non ? "B9B4AD" : INK);
      cells.push(cell(para(txt(affiche, { size: 18, bold: oui, color: couleur }),
        { align: AlignmentType.CENTER, after: 0 }),
        { w: 2160, borders: bd, fill: b.colonnes[i].reco ? SOFT : undefined,
          ml: 60, mr: 60, mt: 70, mb: 70 }));
    });
    return new TableRow({ children: cells });
  });

  return [tbl([head].concat(rows), W)];
};

/* échéancier */
B.etapes = (b) => [tbl(b.items.map((it) => {
  const bd = { top: none, bottom: hair(), left: none, right: none };
  return new TableRow({ children: [
    cell(para(txt(it.quand, { font: SERIF, size: 20, bold: true }), { after: 0 }), { w: 1800, borders: bd }),
    cell(para(rich(it.quoi, { size: 20 }), { after: 0 }), { w: 8280, borders: bd, ml: 160 }),
  ]});
}), [1800, 8280])];

/* deux cartes côte à côte */
B.deuxcartes = (b) => {
  const col = (c) => cell([
    para(txt(c.titre, { font: SERIF, size: 24, bold: true }), { after: 90 }),
    ...c.items.map(puce),
  ], { w: 4920, fill: SOFT, ml: 200, mr: 200, mt: 200, mb: 200,
       borders: { top: none, bottom: none, right: none,
                  left: { style: BorderStyle.SINGLE, size: 18, color: ORANGE } } });
  return [tbl([new TableRow({ children: [col(b.gauche), cell([spacer(0)], { w: 240 }), col(b.droite)] })],
              [4920, 240, 4920])];
};

/* lignes vierges pour prise de notes: un filet clair par ligne */
B.notes = (b) => {
  const n = b.lignes || 4;
  const out = [];
  for (let i = 0; i < n; i++) {
    out.push(new Paragraph({
      children: [txt(" ", { size: 20 })],
      spacing: { before: 0, after: 190 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 4 } },
    }));
  }
  return out;
};

/* case a cocher suivie d'un libelle */
B.cases = (b) => b.items.map((t) => new Paragraph({
  children: [txt("❑  ", { size: 24, color: "B9B4AD" })].concat(rich(t, { size: 20 })),
  spacing: { after: 130 },
}));

/* lignes de signature */
B.signature = (b) => {
  const one = (who) => cell([
    para(txt(who, { size: 17, bold: true, color: DIM, caps: true, spacing: 40 }), { after: 700 }),
    new Paragraph({ children: [], spacing: { after: 60 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: INK, space: 1 } } }),
    para(txt("Signature et date", { size: 17, color: DIM }), { after: 0 }),
  ], { w: 4920 });
  return [spacer(700), tbl([new TableRow({ children: [one(b.gauche), cell([spacer(0)], { w: 240 }), one(b.droite)] })],
                           [4920, 240, 4920])];
};

/* ---------- assemblage ---------- */
const children = [];

if (S.client) {
  children.push(tbl([new TableRow({ children: [
    cell([lbl(S.client.libelle || "Présentée à"),
          para(txt(S.client.nom, { size: 22, bold: true }), { after: 30 }),
          ...(S.client.lignes || []).map((l, i, a) =>
            para(txt(l, { size: 20 }), { after: i === a.length - 1 ? 0 : 20 }))], { w: 5040 }),
    cell([lbl("Préparée par"),
          para(txt(S.agence.nom, { size: 22, bold: true }), { after: 30 }),
          ...(S.agence.lignes || []).map((l, i, a) =>
            para(txt(l, { size: 20 }), { after: i === a.length - 1 ? 0 : 20 }))], { w: 5040 }),
  ]})], [5040, 5040]));
  children.push(new Paragraph({ children: [], spacing: { before: 220, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: ORANGE, space: 1 } } }));
}
if (S.titre) children.push(h1(S.titre));
if (S.intro) children.push(para(rich(S.intro, { size: 20, color: DIM, boldColor: INK }), { after: 200 }));

(S.blocs || []).forEach((b) => {
  const fn = B[b.type];
  if (!fn) { console.error("bloc inconnu: " + b.type); process.exit(1); }
  fn(b).forEach((el) => children.push(el));
});

const titreDoc = (S.type || "Document").toUpperCase();
const doc = new Document({
  creator: S.agence.nom,
  title: titreDoc + " " + (S.numero || ""),
  numbering: { config: [{ reference: "puces", levels: [{
    level: 0, format: LevelFormat.BULLET, text: "▪", alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 300, hanging: 200 } }, run: { color: ORANGE, size: 20 } },
  }]}]},
  styles: { default: { document: { run: { font: SANS, size: 21, color: INK } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 },
                          margin: { top: 1080, right: 1080, bottom: 900, left: 1080 } } },
    headers: { default: new Header({ children: [
      tbl([new TableRow({ children: [
        cell(new Paragraph({ children: [new ImageRun({ data: fs.readFileSync(LOGO), type: "png",
              transformation: { width: 150, height: 53 } })], spacing: { after: 0 } }),
          { w: 5040, borders: { top: none, bottom: hair(INK, 12), left: none, right: none }, mb: 120 }),
        cell([ para(txt(titreDoc, { font: SERIF, size: 22, bold: true, spacing: 60 }),
                    { align: AlignmentType.RIGHT, after: 20 }),
               para(txt("No " + (S.numero || "") + "  |  " + (S.date || ""), { size: 17, color: DIM }),
                    { align: AlignmentType.RIGHT, after: 0 }) ],
             { w: 5040, borders: { top: none, bottom: hair(INK, 12), left: none, right: none }, mb: 120 }),
      ]})], [5040, 5040]),
      spacer(220),
    ]})},
    footers: { default: new Footer({ children: [new Paragraph({
      spacing: { before: 120, after: 0 },
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 6 } },
      children: [
        txt(S.agence.nom, { size: 16, bold: true, color: DIM }),
        txt("   |   " + (S.agence.contact || "") + "          Page ", { size: 16, color: DIM }),
        new TextRun({ children: [PageNumber.CURRENT], size: 16, color: DIM, font: SANS }),
        txt(" de ", { size: 16, color: DIM }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: DIM, font: SANS }),
      ],
    })]})},
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outPath, buf);
  console.log("ecrit: " + outPath + "  " + (buf.length / 1024).toFixed(0) + " Ko");
});
