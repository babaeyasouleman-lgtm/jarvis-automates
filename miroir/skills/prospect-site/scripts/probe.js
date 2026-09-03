/* probe.js - mesure une maquette dans le panneau de previsualisation.
 *
 * Usage: coller ce fichier dans javascript_tool, sur la page servie.
 * Balayer les largeurs avec resize_window: 375, 820, 1280, 1440, 1920.
 * VERIFIER out.w: le panneau ignore parfois le redimensionnement.
 *
 * Retourne un objet compact. Une cle absente veut dire "rien a signaler".
 * Ce que ce script NE peut PAS voir: les couleurs percues, le gout, la qualite d'une
 * photo, et les images en background CSS. Il prouve la geometrie, pas l'esthetique.
 *
 * Teste le 2026-08-12 sur Salon-Amina-Beaute-demo.html. Quatre bugs corriges a ce
 * moment-la: lignes de h1 sur titre assemble par caracteres, faux positif sticky sur
 * l'en-tete, document.fonts.check qui repond vrai pour une police absente, et les
 * assertions rythme et largeurs qui ne se declenchaient jamais.
 */
(function () {
  var out = { w: innerWidth };
  var vis = function (e) { return e.offsetParent !== null || getComputedStyle(e).position === 'fixed'; };
  var sel = function (e) {
    return e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') +
      (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  };
  var cap = function (a) { return a.slice(0, 8); };

  /* 1. debordement horizontal */
  var d = document.scrollingElement;
  if (d.scrollWidth > d.clientWidth + 1) {
    var wide = [];
    document.querySelectorAll('body *').forEach(function (e) {
      var r = e.getBoundingClientRect();
      if (r.width > 0 && (r.right > d.clientWidth + 1 || r.left < -1) && vis(e)) {
        wide.push(sel(e) + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
      }
    });
    out.overflow = { page: d.scrollWidth - d.clientWidth, coupables: cap(wide) };
  }

  /* 2. images affichees plus larges que leur source */
  var up = [];
  document.querySelectorAll('img').forEach(function (im) {
    var r = im.getBoundingClientRect();
    if (!r.width || !im.naturalWidth || !vis(im)) return;
    var k = r.width / im.naturalWidth;
    if (k > 1.05) up.push(sel(im) + ' ' + k.toFixed(2) + 'x (' + Math.round(r.width) + '/' + im.naturalWidth + ')');
  });
  if (up.length) out.imagesAgrandies = cap(up);
  var bg = 0;
  document.querySelectorAll('body *').forEach(function (e) {
    if (getComputedStyle(e).backgroundImage.indexOf('url(') === 0) bg++;
  });
  if (bg) out.fondsCssNonMesures = bg;

  /* 3. cibles tactiles sous 44px */
  var small = [];
  document.querySelectorAll('a,button,input,select,textarea,[role="button"]').forEach(function (e) {
    if (!vis(e)) return;
    var r = e.getBoundingClientRect();
    if (!r.width) return;
    if (r.height < 44 || r.width < 44) small.push(sel(e) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  });
  if (small.length) out.ciblesSous44 = { n: small.length, ex: cap(small) };

  /* 4. sticky tue par un ancetre scrollable.
     La regle "premier de sa fratrie" ne vaut que pour un panneau epingle dans une piste,
     pas pour un en-tete de page: on exclut header et nav. */
  var stuck = [];
  document.querySelectorAll('body *').forEach(function (e) {
    if (getComputedStyle(e).position !== 'sticky') return;
    var p = e.parentElement, bad = null;
    while (p && p !== document.body) {
      var c = getComputedStyle(p);
      if (['visible', 'clip'].indexOf(c.overflowY) < 0 || ['visible', 'clip'].indexOf(c.overflowX) < 0) {
        bad = sel(p) + ' overflow:' + c.overflow; break;
      }
      p = p.parentElement;
    }
    if (bad) stuck.push(sel(e) + ' <- ' + bad);
    var tag = e.tagName.toLowerCase();
    if (tag !== 'header' && tag !== 'nav' && e.previousElementSibling &&
        e.parentElement !== document.body && e.parentElement.children.length > 2) {
      stuck.push(sel(e) + ' n est pas premier de sa fratrie, il sera echoue en fin de piste');
    }
  });
  if (stuck.length) out.stickyCasse = cap(stuck);

  /* 5. polices reellement chargees.
     document.fonts.check repond vrai pour une famille absente, il est inutilisable ici.
     La mesure canvas est la seule methode fiable. */
  var ctx = document.createElement('canvas').getContext('2d');
  var probe = 'mmmmmmmmmmlliWWWW@#';
  var loaded = function (fam) {
    ctx.font = '72px monospace'; var base = ctx.measureText(probe).width;
    ctx.font = '72px "' + fam + '", monospace'; var test = ctx.measureText(probe).width;
    return Math.abs(test - base) > 0.5;
  };
  var fams = {}, badf = [];
  document.querySelectorAll('h1,h2,h3,p,body,a,li,span,div').forEach(function (e) {
    var f = getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '').trim();
    if (f) fams[f] = 1;
  });
  Object.keys(fams).forEach(function (f) {
    if (/^(serif|sans-serif|monospace|system-ui|ui-|Arial|Helvetica|Times)/i.test(f)) return;
    if (!loaded(f)) badf.push(f);
  });
  out.polices = Object.keys(fams);
  if (badf.length) out.policesRetombeesSurArial = badf;

  /* 6. echelle typographique: six crans maximum, trois usages minimum par cran */
  var sizes = {};
  document.querySelectorAll('body *').forEach(function (e) {
    if (!vis(e)) return;
    if (!Array.prototype.some.call(e.childNodes, function (n) { return n.nodeType === 3 && n.textContent.trim(); })) return;
    var s = Math.round(parseFloat(getComputedStyle(e).fontSize));
    sizes[s] = (sizes[s] || 0) + 1;
  });
  var keys = Object.keys(sizes).map(Number).sort(function (a, b) { return b - a; });
  out.crans = keys.map(function (k) { return k + 'px x' + sizes[k]; });
  if (keys.length > 6) out.tropDeCrans = keys.length + ' crans, le maximum est 6';
  var orph = keys.filter(function (k) { return sizes[k] < 3; });
  if (orph.length) out.cransOrphelins = orph.map(function (k) { return k + 'px x' + sizes[k]; });
  var mini = keys.filter(function (k) { return k < 16; });
  if (mini.length) out.sous16px = mini;

  /* 7. rythme vertical entre sections de premier niveau */
  var secs = [].filter.call(document.querySelectorAll('section,footer'), function (e) {
    return !e.parentElement.closest('section') && vis(e);
  });
  var gaps = [], emp = [];
  for (var i = 0; i < secs.length - 1; i++) {
    var a = secs[i].getBoundingClientRect(), b = secs[i + 1].getBoundingClientRect();
    gaps.push(Math.round(b.top - a.bottom));
    var ca = getComputedStyle(secs[i]), cb = getComputedStyle(secs[i + 1]);
    var pb = Math.round(parseFloat(ca.paddingBottom)), pt = Math.round(parseFloat(cb.paddingTop));
    if (pb > 0 && pt > 0) emp.push(sel(secs[i]) + ' pb' + pb + ' + ' + sel(secs[i + 1]) + ' pt' + pt + ' = ' + (pb + pt) + 'px');
  }
  var pads = secs.map(function (s) {
    var c = getComputedStyle(s);
    return Math.round(parseFloat(c.paddingTop)) + '/' + Math.round(parseFloat(c.paddingBottom));
  });
  out.sections = secs.length;
  out.paddings = pads;
  if (gaps.some(function (g) { return g > 4; })) out.margesEnPlusDuPadding = gaps;
  if (emp.length) out.paddingsEmpiles = cap(emp);
  var freq = {}, top = 0, topv = '';
  pads.forEach(function (p) { freq[p] = (freq[p] || 0) + 1; if (freq[p] > top) { top = freq[p]; topv = p; } });
  if (secs.length > 3 && top / secs.length >= 0.6) {
    out.rythmeUniforme = top + ' sections sur ' + secs.length + ' au meme padding (' + topv + '). Uniformite lue comme automatique.';
  }

  /* 8. le h1 en escalier.
     Grouper les rects par ligne, jamais par largeur: un titre assemble caractere par
     caractere renvoie un rect par span et donnait 38 fausses lignes. */
  var h1 = document.querySelector('h1');
  if (h1) {
    var rg = document.createRange(); rg.selectNodeContents(h1);
    var rows = [];
    /* La tolerance suit l'interligne, jamais une constante: un mot en italique dans une
       seconde famille decale son rect de plus de 6px et fabrique de fausses lignes.
       Vu le 2026-08-12 sur Elite Beauty Lab, ou 2 lignes reelles en donnaient 4. */
    var tol = parseFloat(getComputedStyle(h1).lineHeight) * 0.5 || 12;
    [].forEach.call(rg.getClientRects(), function (r) {
      if (r.width < 1 || r.height < 1) return;
      var hit = null;
      rows.forEach(function (x) { if (Math.abs(x.t - r.top) < tol) hit = x; });
      if (hit) { hit.l = Math.min(hit.l, r.left); hit.r = Math.max(hit.r, r.right); }
      else rows.push({ t: r.top, l: r.left, r: r.right });
    });
    rows.sort(function (a, b) { return a.t - b.t; });
    var lignes = rows.map(function (x) { return Math.round(x.r - x.l); });
    out.h1 = { px: Math.round(parseFloat(getComputedStyle(h1).fontSize)), lignes: lignes };
    if (lignes.length > 3) out.h1.probleme = 'plus de 3 lignes';
    else if (lignes.length > 1 && Math.min.apply(null, lignes) < 0.4 * Math.max.apply(null, lignes)) {
      out.h1.probleme = 'escalier, la ligne courte fait moins de 40% de la longue';
    }
  }

  /* 9. contenu vivant sous un masque, ou a opacite nulle.
     Une mesure geometrique seule ne le voit pas: c'est le piege DMcosmetique. */
  var msk = [];
  document.querySelectorAll('h1,h2,h3,p,img,figure').forEach(function (e) {
    if (!e.offsetParent && getComputedStyle(e).position !== 'fixed') return;
    var r = e.getBoundingClientRect();
    if (!r.width || !r.height) return;
    if (parseFloat(getComputedStyle(e).opacity) === 0) { msk.push(sel(e) + ' opacity:0'); return; }
    var p = e.parentElement;
    while (p && p !== document.body) {
      var c = getComputedStyle(p);
      if (c.overflow === 'hidden' || c.overflowY === 'hidden') {
        var pr = p.getBoundingClientRect();
        if (r.bottom < pr.top + 1 || r.top > pr.bottom - 1) { msk.push(sel(e) + ' hors de ' + sel(p)); break; }
      }
      p = p.parentElement;
    }
  });
  if (msk.length) out.contenuInvisible = cap(msk);

  /* 10. raccourci padding qui ecrase la marge du conteneur */
  var wraps = [];
  document.querySelectorAll('[class*="wrap"],[class*="container"]').forEach(function (e) {
    if (!vis(e)) return;
    if (parseFloat(getComputedStyle(e).paddingLeft) === 0 && e.getBoundingClientRect().width >= innerWidth - 1) {
      wraps.push(sel(e) + ' padding-left:0 en pleine largeur');
    }
  });
  if (wraps.length) out.conteneursSansMarge = cap(wraps);

  /* 11. largeurs de conteneur: au moins trois valeurs distinctes */
  var w = {};
  secs.forEach(function (s) {
    var inner = s.querySelector('[class*="wrap"],[class*="container"],[class*="inner"]') || s;
    w[Math.round(inner.getBoundingClientRect().width)] = 1;
  });
  out.largeurs = Object.keys(w).map(Number).sort(function (a, b) { return a - b; });
  if (out.largeurs.length < 3 && secs.length > 3) {
    out.largeurUnique = 'une seule mesure sur toute la page, le rythme est plat';
  }

  return out;
})();
