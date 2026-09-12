// Le tableau de bord du dimanche, ecrit par un script et sans un seul appel
// au modele. 11 septembre 2026, amelioration 4 de _Equipe/Etat de l art et nous.md.
//
// Il lit les journaux hebdo de chaque chef, _Equipe/<role>/AAAA-Sxx.md, y
// prend le bloc `chiffres:` du gabarit (champ 5), et les lignes de jour du
// chef de cabinet, deposees par captures.ps1 depuis les stats de l agent.
// Il ecrit _Equipe/Tableau de bord.md. Lance par passage.ps1 apres l export,
// ou a la main : node C:\Obsidian\equipe\tableau.js
'use strict';

const fs = require('fs');
const path = require('path');

const COFFRE = 'C:\\Obsidian\\Second Brain';
const EQUIPE = path.join(COFFRE, '_\u00c9quipe');
const CIBLE = path.join(EQUIPE, 'Tableau de bord.md');
const SEMAINES_GARDEES = 8;

function semaineIso(d = new Date()) {
  const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  const jour = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - jour);
  const debut = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  const n = Math.ceil((((date - debut) / 86400000) + 1) / 7);
  return `${date.getUTCFullYear()}-S${String(n).padStart(2, '0')}`;
}

/** Les blocs chiffres: d un journal hebdo, en objets. */
function chiffresDe(texte) {
  const out = [];
  const re = /chiffres:\s*\n((?:\s+\w+:.*\n?)+)/g;
  let m;
  while ((m = re.exec(texte))) {
    const o = {};
    for (const l of m[1].split('\n')) {
      const c = l.match(/^\s+(\w+):\s*(.*?)\s*(?:#.*)?$/);
      if (c) o[c[1]] = c[2];
    }
    out.push(o);
  }
  return out;
}

/** Les lignes de jour du chef de cabinet : - AAAA-MM-JJ : recus 14, envoyes 9, appels 38, ... 0.41 $ */
function joursDe(texte) {
  const out = [];
  for (const l of texte.split('\n')) {
    const m = l.match(/^- (\d{4}-\d{2}-\d{2}) : (.*)$/);
    if (!m) continue;
    const v = {};
    for (const [, cle, n] of m[2].matchAll(/(re\u00e7us|recus|envoy\u00e9s|envoyes|appels|tronqu\u00e9s|tronques|erreurs) (\d+)/g)) v[cle.normalize('NFD').replace(/[\u0300-\u036f]/g, '')] = Number(n);
    const cout = m[2].match(/([\d.,]+) \$/);
    v.cout = cout ? Number(cout[1].replace(',', '.')) : 0;
    out.push({ jour: m[1], ...v });
  }
  return out;
}

function lire() {
  const parSemaine = {};
  if (!fs.existsSync(EQUIPE)) return parSemaine;
  for (const role of fs.readdirSync(EQUIPE, { withFileTypes: true }).filter(e => e.isDirectory()).map(e => e.name)) {
    const dossier = path.join(EQUIPE, role);
    for (const f of fs.readdirSync(dossier).filter(f => /^\d{4}-S\d{2}\.md$/.test(f))) {
      const semaine = f.replace('.md', '');
      const texte = fs.readFileSync(path.join(dossier, f), 'utf8');
      parSemaine[semaine] = parSemaine[semaine] || { chefs: [], jours: [] };
      for (const c of chiffresDe(texte)) parSemaine[semaine].chefs.push({ chef: c.chef || role, ...c });
      if (role === 'cabinet') parSemaine[semaine].jours.push(...joursDe(texte));
    }
  }
  return parSemaine;
}

function rendre(parSemaine) {
  const semaines = Object.keys(parSemaine).sort().reverse().slice(0, SEMAINES_GARDEES);
  const l = ['---', 'type: r\u00e9f\u00e9rence', 'domaine: Personnel', `date: ${new Date().toISOString().slice(0, 10)}`, '---', '',
    '# Tableau de bord', '',
    `\u00c9crit par \`C:\\Obsidian\\equipe\\tableau.js\` \u00e0 chaque passage de nuit, sans mod\u00e8le, \u00e0 partir des blocs \`chiffres:\` des journaux hebdo et des lignes de jour du chef de cabinet. Semaine courante : ${semaineIso()}. Trois chiffres par chef, r\u00e8gle 6 du plan, et ce que l'agent a consomm\u00e9.`, ''];
  if (!semaines.length) l.push('Aucun journal hebdo encore. Le premier chef qui \u00e9crit le sien remplit ce tableau.');
  for (const s of semaines) {
    const { chefs, jours } = parSemaine[s];
    l.push(`## ${s}`, '');
    if (chefs.length) {
      l.push('| Chef | Produit | Sorti | Revenu | Co\u00fbt \u00e9quivalent |', '|---|---|---|---|---|');
      for (const c of chefs) l.push(`| ${c.chef} | ${c.produit ?? ''} | ${c.sorti ?? ''} | ${c.revenu ?? ''} | ${c.cout_usd ? `${c.cout_usd} $` : ''} |`);
      l.push('');
    }
    if (jours.length) {
      const t = jours.reduce((a, j) => ({ recus: a.recus + (j.recus || 0), envoyes: a.envoyes + (j.envoyes || 0), appels: a.appels + (j.appels || 0), tronques: a.tronques + (j.tronques || 0), erreurs: a.erreurs + (j.erreurs || 0), cout: a.cout + (j.cout || 0) }), { recus: 0, envoyes: 0, appels: 0, tronques: 0, erreurs: 0, cout: 0 });
      l.push(`**L'agent WhatsApp**, ${jours.length} jour(s) : ${t.recus} re\u00e7us, ${t.envoyes} envoy\u00e9s, ${t.appels} appels, ${t.tronques} tronqu\u00e9s, ${t.erreurs} erreurs, ${t.cout.toFixed(2)} $ \u00e9quivalent.`, '');
      l.push('| Jour | Re\u00e7us | Envoy\u00e9s | Appels | Co\u00fbt |', '|---|---|---|---|---|');
      for (const j of jours.sort((a, b) => a.jour.localeCompare(b.jour))) l.push(`| ${j.jour} | ${j.recus ?? 0} | ${j.envoyes ?? 0} | ${j.appels ?? 0} | ${(j.cout || 0).toFixed(2)} $ |`);
      l.push('');
    }
  }
  l.push('Reli\u00e9 \u00e0 : [[R\u00e8gles communes]], [[Gabarit d\'un chef]], [[\u00c9tat de l\'art et nous]]', '');
  return l.join('\n');
}

const texte = rendre(lire());
fs.writeFileSync(CIBLE, texte, 'utf8');
console.log(`Tableau de bord ecrit, ${Object.keys(lire()).length} semaine(s)`);
