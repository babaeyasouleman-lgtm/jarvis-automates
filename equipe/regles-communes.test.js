// Le test de coherence des consignes, cote PC. 11 septembre 2026.
//
// Pourquoi il existe : la meme raison que constantes.test.js cote agent.
// Le 8 septembre 2026, une liste vivait a six endroits du prompt du
// classifier, deux copies avaient diverge, et rien ne l'a signale pendant
// des semaines. Les regles communes de l'equipe vivent dans UN fichier,
// `_Équipe/Règles communes.md`, que chaque consigne de chef lit. Si une
// consigne en recopie une ligne, la copie finira par diverger, en silence.
// Ce test refuse la copie.
//
// Ce qu'il verifie, dans les deux sens :
//   1. Aucune consigne (`C:\Obsidian\<x>\consigne.md`) ne contient une ligne
//      des regles communes.
//   2. Les regles communes ne contiennent aucune ligne de leurs sources :
//      elles renvoient, elles ne recopient pas.
//   3. Les regles communes tiennent en moins de 150 lignes.
//
// Une « ligne » est comparee apres normalisation : minuscules, sans marques
// markdown, espaces repliees. Seules les lignes de 40 caracteres et plus
// comptent, en dessous les collisions sont fortuites.
//
// Lancer : node --test C:\Obsidian\equipe
// Aucun accent dans ce fichier, par la meme prudence que les .ps1.

'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

const OBSIDIAN = 'C:\\Obsidian';
const COFFRE = path.join(OBSIDIAN, 'Second Brain');
const EQUIPE = path.join(COFFRE, '_\u00c9quipe');
const REGLES = path.join(EQUIPE, 'R\u00e8gles communes.md');
const AGENT = 'C:\\Projets\\openwa-agent\\agent\\src';

const PLAFOND_LIGNES = 150;
const LONGUEUR_MIN = 40;

/** Les sources vers lesquelles les regles communes renvoient. */
const SOURCES = [
  path.join(AGENT, 'domain', 'voix.js'),
  path.join(OBSIDIAN, 'billets', 'mots.txt'),
  path.join(OBSIDIAN, 'billets', 'consigne.md'),
  path.join(EQUIPE, 'Charte de l\'\u00e9quipe.md'),
  path.join(EQUIPE, 'Gabarit d\'un chef.md'),
  path.join(COFFRE, '02 Projets', 'Plan Jarvis.md'),
];

/** Dossiers de C:\Obsidian qui ne portent pas de consigne. */
const DOSSIERS_IGNORES = new Set(['Second Brain', 'equipe', 'miroir', '.git']);

function lire(fichier) {
  return fs.readFileSync(fichier, 'utf8').normalize('NFC');
}

function normaliser(ligne) {
  return ligne
    .toLowerCase()
    .replace(/[`*_>#|]/g, ' ')
    .replace(/^\s*(\d+\.|-)\s+/, ' ')
    .replace(/\[\[|\]\]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Les lignes normalisees d'un fichier qui comptent, avec leur numero. */
function lignesUtiles(fichier) {
  const out = [];
  lire(fichier).split(/\r?\n/).forEach((brute, i) => {
    const l = normaliser(brute);
    if (l.length >= LONGUEUR_MIN) out.push({ ligne: l, numero: i + 1 });
  });
  return out;
}

function consignes() {
  return fs.readdirSync(OBSIDIAN, { withFileTypes: true })
    .filter((e) => e.isDirectory() && !DOSSIERS_IGNORES.has(e.name))
    .map((e) => path.join(OBSIDIAN, e.name, 'consigne.md'))
    .filter((f) => fs.existsSync(f));
}

/** Les lignes de `a` qui se retrouvent telles quelles dans `b`. */
function communes(a, b) {
  const dansB = new Map(lignesUtiles(b).map((x) => [x.ligne, x.numero]));
  return lignesUtiles(a)
    .filter((x) => dansB.has(x.ligne))
    .map((x) => ({ ligne: x.ligne, a: x.numero, b: dansB.get(x.ligne) }));
}

test('les regles communes existent et tiennent sous le plafond', () => {
  assert.ok(fs.existsSync(REGLES), `introuvable : ${REGLES}`);
  const n = lire(REGLES).split(/\r?\n/).length;
  assert.ok(n < PLAFOND_LIGNES, `${n} lignes, le plafond est ${PLAFOND_LIGNES}`);
});

test('au moins une consigne existe a cote des regles', () => {
  assert.ok(consignes().length > 0, 'aucune consigne.md trouvee dans C:\\Obsidian');
});

test('aucune consigne ne recopie une ligne des regles communes', () => {
  const fautes = [];
  for (const c of consignes()) {
    for (const d of communes(REGLES, c)) {
      fautes.push(`${path.basename(path.dirname(c))}\\consigne.md:${d.b} recopie les regles ligne ${d.a} : « ${d.ligne} »`);
    }
  }
  assert.deepEqual(fautes, [], '\n' + fautes.join('\n'));
});

test('les regles communes renvoient a leurs sources sans les recopier', () => {
  const fautes = [];
  for (const s of SOURCES) {
    assert.ok(fs.existsSync(s), `source introuvable : ${s}`);
    for (const d of communes(REGLES, s)) {
      fautes.push(`regles ligne ${d.a} recopie ${path.basename(s)}:${d.b} : « ${d.ligne} »`);
    }
  }
  assert.deepEqual(fautes, [], '\n' + fautes.join('\n'));
});
