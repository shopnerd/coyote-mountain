/* roots.js · planting in section: every species near a section line drawn with its root system, grown from published rooting depths and spreads (ROOT_DATA, with sources), in the ink of the root atlases (Weaver, Kutschera, Natura).
   two places: the plants at true scale in the profile, and under it a root chart, every species the section crosses at one scale against a depth ruler.
   loaded after topo.html's main script; uses its S, AGRO, AGRO_LIB, agroRadiusM, cs, fL, font, isFt, INK, INK2, INK3 */
(() => {
const ROOT_DATA = window.ROOT_DATA || {};   // from roots-data.js   // key → { common, latin, form, arch, h, spread, typ, max, lat, yrs, regen, conf, src }
let S, AGRO, AGRO_LIB, agroRadiusM, cs, fL, font, isFt, INK, INK2, INK3, PAPER, rootInfo;   // topo's, through window.__topo
const bind = () => ({ S, AGRO, AGRO_LIB, agroRadiusM, cs, fL, font, isFt, INK, INK2, INK3, PAPER, rootInfo } = window.__topo());
const TAU = Math.PI * 2, DOWN = Math.PI / 2, UP = -Math.PI / 2, SEPIA = '#4b3220', LEAF = '#5d6b45';

function rng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const hashStr = s => { let h = 2166136261; for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619); return h >>> 0; };

/* one root (or stem) walked out step by step: a little wander, a pull toward its preferred direction, branches along the way.
   P: { tgt: 'down' | 'up' | 'side' | angle, dip, grav, wig, gap, brA: [lo, hi], clen(s, len, R), brW, maxO, kid: P for the branches, inside(x, y) } */
function grow(R, out, x, y, a, len, w, o, P, budget) {
  const xs = [x], ys = [y], ws = [w], step = Math.max(len / 70, P.step || .004);
  let s = 0, nextBr = P.gap * (.2 + R() * .8);
  while (s < len && budget.n > 0) {
    const tgt = P.tgt === 'down' ? DOWN : P.tgt === 'up' ? UP : P.tgt === 'side' ? (Math.cos(a) >= 0 ? P.dip : Math.PI - P.dip) : P.tgt;
    a += (R() - .5) * P.wig + Math.sin(tgt - a) * P.grav;
    x += Math.cos(a) * step; y += Math.sin(a) * step; s += step; budget.n--;
    if (P.tgt !== 'up' && y < .01) { y = .01; a = Math.abs(a) % Math.PI || .2; }
    if (P.inside && !P.inside(x, y)) break;
    const ww = w * (1 - .82 * s / len); xs.push(x); ys.push(y); ws.push(ww);
    if (P.kid && o < P.maxO && s >= nextBr) { nextBr = s + P.gap * (.4 + R() * 1.2);
      const side = R() < .5 ? -1 : 1, ca = a + side * (P.brA[0] + R() * (P.brA[1] - P.brA[0])), cl = P.clen(s, len, R);
      if (cl > .01) grow(R, out, x, y, ca, cl, ww * P.brW, o + 1, P.kid, budget); }
  }
  if (xs.length > 1) out.push({ x: xs, y: ys, w: ws, o });
  return [x, y];
}

/* fine rootlets on everything: short, many, the hairy look of the atlases */
const FINE = (T, maxO) => ({ tgt: 'down', grav: .02, wig: .55, gap: Math.max(.012, T * .02), brA: [.7, 1.5], clen: (s, len, R) => Math.min(.12, T * .06) * (.3 + R()), brW: .6, maxO, step: .006 });

/* the root systems, by architecture; dims in metres at this age: T where most roots are, M deepest, Lr lateral reach, Wc crown or clump width, W0 the root collar */
function rootSys(arch, R, T, M, Lr, Wc, W0, form) {
  const out = [], budget = { n: form === 'tree' ? 26000 : 16000 }, lim = (mx, my) => (x, y) => Math.abs(x) < mx && y < my;
  const fine = FINE(T, 9);
  if (arch === 'taproot') {   // one deep main root, laterals strongest near the top
    const lat = { tgt: 'side', dip: .35, grav: .06, wig: .3, gap: Lr * .09, brA: [.5, 1.2], clen: (s, len, R) => (len - s) * .45 * (.4 + R()), brW: .55, maxO: 4, kid: { tgt: 'down', grav: .05, wig: .45, gap: T * .05, brA: [.6, 1.3], clen: (s, len, R) => (len - s) * .5 * (.4 + R()), brW: .5, maxO: 5, kid: fine }, inside: lim(Lr * 1.15, M) };
    grow(R, out, 0, .02, DOWN, M, W0 * .8, 0, { tgt: 'down', grav: .22, wig: .1, gap: M * .045, brA: [1, 1.45], clen: (s, len, R) => Lr * Math.max(.15, 1 - s / (T * 1.4)) * (.5 + R() * .6), brW: .45, maxO: 4, kid: lat, inside: lim(Lr * 1.2, M) }, budget);
    for (let i = 0; i < 4; i++) grow(R, out, (R() - .5) * W0, .03, DOWN + (i % 2 ? 1 : -1) * (.9 + R() * .4), Lr * (.6 + R() * .4), W0 * .35, 1, lat, budget);
  } else if (arch === 'heart') {   // several oblique main roots, a dome of branching, a few sinkers deeper
    const sub = { tgt: 'down', grav: .07, wig: .4, gap: T * .07, brA: [.5, 1.2], clen: (s, len, R) => (len - s) * .55 * (.4 + R()), brW: .55, maxO: 5, kid: fine, inside: lim(Lr * 1.1, M) };
    const main = { tgt: 'down', grav: .035, wig: .22, gap: T * .08, brA: [.4, 1.1], clen: (s, len, R) => (len - s) * .6 * (.4 + R()), brW: .55, maxO: 4, kid: sub, inside: lim(Lr * 1.1, M) };
    const n = 6 + (R() * 3 | 0); for (let i = 0; i < n; i++) { const f = i / (n - 1) - .5, a = DOWN + f * 2.2 + (R() - .5) * .2; grow(R, out, f * W0, .05, a, Math.hypot(T * 1.1, Lr * Math.abs(f) * 1.6) * (.75 + R() * .4), W0 * .5, 0, main, budget); }
    for (let i = 0; i < 3; i++) grow(R, out, (R() - .5) * Lr * .4, T * (.2 + R() * .2), DOWN, M * (.6 + R() * .4), W0 * .12, 1, { ...sub, grav: .2, inside: lim(Lr * 1.1, M) }, budget);
  } else if (arch === 'plate') {   // a wide shallow plate of laterals with sinkers dropping from it
    const sink = { tgt: 'down', grav: .18, wig: .25, gap: T * .08, brA: [.6, 1.4], clen: (s, len, R) => (len - s) * .4 * (.3 + R()), brW: .5, maxO: 4, kid: fine, inside: lim(Lr * 1.2, M) };
    const lat = { tgt: 'side', dip: .08, grav: .05, wig: .2, gap: Lr * .07, brA: [.9, 1.6], clen: (s, len, R) => R() < .45 ? T * (.5 + R() * .7) : (len - s) * .35 * (.4 + R()), brW: .5, maxO: 4, kid: sink, inside: lim(Lr * 1.15, M) };
    const n = 7 + (R() * 4 | 0); for (let i = 0; i < n; i++) { const side = i % 2 ? 1 : -1; grow(R, out, side * W0 * .4, .04 + R() * T * .15, side > 0 ? .1 + R() * .35 : Math.PI - .1 - R() * .35, Lr * (.55 + R() * .5), W0 * .45, 0, lat, budget); }
    for (let i = 0; i < 2; i++) grow(R, out, (R() - .5) * W0, .05, DOWN + (R() - .5) * .4, M * (.5 + R() * .5), W0 * .15, 1, sink, budget);
  } else if (arch === 'fibrous' || arch === 'fibrousDeep') {   // a bunchgrass: a mass of fine roots from the crown; the deep kind plunges as a narrow curtain (vetiver, switchgrass)
    const deep = arch === 'fibrousDeep', n = deep ? 150 : 120, fan = deep ? .45 : 1.5;
    const P = { tgt: 'down', grav: deep ? .1 : .05, wig: .28, gap: T * .035, brA: [.6, 1.5], clen: (s, len, R) => Math.min(.3, T * .14) * (.2 + R()), brW: .65, maxO: 2, step: .008, kid: { tgt: 'down', grav: .02, wig: .6, gap: T * .03, brA: [.6, 1.5], clen: (s, len, R) => Math.min(.08, T * .04) * (.3 + R()), brW: .6, maxO: 2, step: .005 }, inside: lim(Math.max(Lr, Wc), M) };
    for (let i = 0; i < n && budget.n > 0; i++) { const u = (i + R()) / n - .5, deepOne = R() < (deep ? .35 : .12), len = deepOne ? M * (.65 + R() * .35) : T * (.35 + R() * .85);
      grow(R, out, u * Wc, .01, DOWN + u * fan + (R() - .5) * .25, len, W0 * (.35 + R() * .4), 0, P, budget); }
  } else if (arch === 'rhizome') {   // a sod: runners just under the surface, a tuft of fibrous roots at every node
    const P = { tgt: 'down', grav: .06, wig: .35, gap: T * .05, brA: [.6, 1.5], clen: (s, len, R) => Math.min(.12, T * .1) * (.3 + R()), brW: .6, maxO: 2, step: .005, kid: fine, inside: lim(Lr * 1.3, M) };
    const runners = []; for (const side of [-1, 1]) for (let k = 0; k < 2; k++) { const d = .03 + R() * .1, xs = [], ys = [], ws = []; let x = 0; while (Math.abs(x) < Lr) { xs.push(x); ys.push(d + Math.sin(x * 9 + k) * .012); ws.push(W0 * .9); x += side * .02; } runners.push({ x: xs, y: ys, w: ws, o: 0 }); out.push(runners[runners.length - 1]); }
    for (const r of runners) for (let i = 4; i < r.x.length; i += 6 + (R() * 4 | 0)) for (let j = 0; j < 5 && budget.n > 0; j++) grow(R, out, r.x[i], r.y[i], DOWN + (R() - .5) * 1.1, R() < .1 ? M * (.6 + R() * .4) : T * (.3 + R() * .8), W0 * .4, 1, P, budget);
    for (let i = 0; i < 40; i++) grow(R, out, (R() - .5) * Wc, .01, DOWN + (R() - .5) * 1.2, T * (.3 + R() * .9), W0 * .4, 1, P, budget);
  } else if (arch === 'tuber') {   // a swollen storage root tapering into a fine taproot (tillage radish)
    const tl = Math.min(M * .4, .45), tw = Math.max(W0, .05); const xs = [], ys = [], ws = []; for (let t = 0; t <= 1.0001; t += .04) { xs.push(Math.sin(t * 5) * .004); ys.push(-.08 + t * tl); ws.push(tw * Math.sin(Math.PI * Math.min(1, .15 + t * .95)) + .004); } out.push({ x: xs, y: ys, w: ws, o: 0, body: true });
    grow(R, out, 0, tl - .08, DOWN, M - tl, tw * .18, 1, { tgt: 'down', grav: .2, wig: .18, gap: M * .04, brA: [.8, 1.4], clen: (s, len, R) => Lr * .5 * (.3 + R()), brW: .5, maxO: 3, kid: fine, inside: lim(Lr, M) }, budget);
    for (let i = 0; i < 30; i++) { const t = R(); grow(R, out, (R() < .5 ? -1 : 1) * tw * .3, t * tl, DOWN + (R() < .5 ? -1 : 1) * (.8 + R() * .6), Lr * (.2 + R() * .5), .002, 2, fine, budget); }
  } else {   // succulentShallow: a wide net just under the surface for catching light rain, a few deeper anchors
    const P = { tgt: 'side', dip: .04, grav: .08, wig: .25, gap: Lr * .05, brA: [.7, 1.5], clen: (s, len, R) => R() < .7 ? Math.min(.15, T * .5) * (.3 + R()) : (len - s) * .35 * (.3 + R()), brW: .55, maxO: 3, kid: fine, inside: lim(Lr * 1.1, M) };
    const n = 12 + (R() * 6 | 0); for (let i = 0; i < n; i++) { const side = i % 2 ? 1 : -1; grow(R, out, side * Wc * .2, .02 + R() * T * .4, side > 0 ? .03 + R() * .25 : Math.PI - .03 - R() * .25, Lr * (.5 + R() * .5), W0 * .3, 0, P, budget); }
    for (let i = 0; i < 3; i++) grow(R, out, (R() - .5) * Wc * .3, .05, DOWN + (R() - .5) * .5, M * (.4 + R() * .6), W0 * .15, 1, { ...P, tgt: 'down', grav: .15, clen: (s, len, R) => (len - s) * .3 * R() }, budget);
  }
  return out;
}

/* above ground, same hand: trees branch into a crown of leaf dabs; shrubs are many stems; grasses are blades and seed heads; forbs stems, leaves, flowers; succulents rosettes or pads */
const HEADS = { bigbluestem: 'turkeyfoot', littlebluestem: 'wisp', indiangrass: 'plume', switchgrass: 'panicle', sideoats: 'flag', bluegrama: 'eyelash', buffalograss: 'eyelash', needlegrass: 'awn', deergrass: 'spike', wildrye: 'spike', kernza: 'spike', saltgrass: 'wisp', lawn: 'panicle', vetiver: 'panicle' };
function topSys(key, form, R, H, Wc, W0) {
  const lines = [], dabs = [], flowers = [], leaves = [], budget = { n: 14000 };
  if (form === 'tree' || form === 'shrub') {
    const tree = form === 'tree', crownH = tree ? H * .62 : H * .9, cy = -(H - crownH / 2), rx = Wc / 2, ry = crownH / 2, inCrown = (x, y) => ((x / (rx * 1.05)) ** 2 + ((y - cy) / (ry * 1.08)) ** 2) < 1 || y > cy + ry * .2;
    const twig = { tgt: 'up', grav: .03, wig: .35, gap: Wc * .06, brA: [.3, .8], clen: (s, len, R) => (len - s) * .7 * (.4 + R()), brW: .6, maxO: 5, inside: (x, y) => y > -H * 1.02 && inCrown(x, y) }; twig.kid = twig;
    const stems = tree ? 1 : 4 + (R() * 4 | 0);
    for (let k = 0; k < stems; k++) { const a = UP + (tree ? (R() - .5) * .08 : (k / (stems - 1 || 1) - .5) * 1.2 + (R() - .5) * .2), trunkL = tree ? H - crownH * .75 : H * (.6 + R() * .35);
      const [tx, ty] = grow(R, lines, (k - stems / 2) * W0 * .3, 0, a, trunkL, tree ? W0 : W0 * .45, 0, { tgt: 'up', grav: tree ? .12 : .04, wig: .06, gap: trunkL * .25, brA: [.45, .9], clen: (s, len, R) => Math.max(rx, ry) * (.6 + R() * .5), brW: .55, maxO: 5, kid: twig }, budget);
      for (let j = 0; j < (tree ? 5 : 2); j++) grow(R, lines, tx, ty, UP + (j - 2) * .45 + (R() - .5) * .3, Math.max(rx, ry) * (.7 + R() * .5), (tree ? W0 : W0 * .45) * .55, 1, twig, budget); }
    for (const l of lines) if (l.o >= 2) { const n = l.x.length; for (let i = Math.floor(n * .35); i < n; i += 2) for (let q = 0; q < 2; q++) dabs.push([l.x[i] + (R() - .5) * Wc * .1, l.y[i] + (R() - .5) * Wc * .1, Wc * (.008 + R() * .014)]); }
    for (let i = 0; i < 500; i++) { const t = R() * TAU, r = Math.sqrt(R()); const x = Math.cos(t) * rx * r, y = cy + Math.sin(t) * ry * r; if (y < -H * .3) dabs.push([x, y, Wc * (.008 + R() * .014)]); }
  } else if (form === 'grass') {
    const n = 46, stiff = key === 'vetiver' ? .25 : 1, head = HEADS[key];
    for (let i = 0; i < n; i++) { const u = (i + R()) / n - .5, side = Math.sign(u) || 1, top = H * (.55 + R() * .45), out = u * Wc * (1.4 + R()) * stiff, xs = [], ys = [], ws = [];
      for (let t = 0; t <= 1.0001; t += .1) { const bend = t * t; xs.push(u * Wc * .25 + out * bend); ys.push(-top * (t - (1 - stiff) * 0 - .25 * bend * Math.abs(u) * (1 / stiff - .2))); ws.push(W0 * 1.5 * (1 - t * .85)); }
      lines.push({ x: xs, y: ys, w: ws, o: 0 }); }
    if (head) { const culms = key === 'vetiver' ? 3 : 7; for (let i = 0; i < culms; i++) { const x0 = (R() - .5) * Wc * .3, top = H * (1 + R() * .2), lean = (R() - .5) * Wc * .4; lines.push({ x: [x0, x0 + lean * .5, x0 + lean], y: [0, -top * .55, -top], w: [W0, W0 * .7, W0 * .4], o: 0 }); flowers.push([x0 + lean, -top, head, H]); } }
  } else if (form === 'forb') {
    const n = key === 'alfalfa' ? 9 : key === 'comfrey' ? 4 : key === 'compassplant' ? 2 : key === 'radish' ? 5 : 5;
    for (let i = 0; i < n; i++) { const a = UP + (i / (n - 1 || 1) - .5) * (key === 'compassplant' ? .2 : .9), L = H * (key === 'radish' ? .5 : .75 + R() * .3), st = { tgt: 'up', grav: .06, wig: .12, gap: L * .2, brA: [.4, .9], clen: (s, len, R) => (len - s) * .45, brW: .6, maxO: key === 'alfalfa' ? 3 : 1, inside: () => true }; st.kid = { ...st, kid: null };
      const [tx, ty] = grow(R, lines, (R() - .5) * Wc * .2, 0, a, L, W0, 0, st, budget); flowers.push([tx, ty, key, H]); }
    const nl = key === 'comfrey' ? 8 : key === 'radish' ? 10 : key === 'compassplant' ? 7 : 14;
    for (let i = 0; i < nl; i++) { const big = key === 'comfrey' || key === 'compassplant' || key === 'radish', y = big ? -H * (.04 + R() * .35) : -H * (.15 + R() * .65), side = R() < .5 ? -1 : 1; leaves.push([side * Wc * (.05 + R() * .15), y, side, (big ? Wc * .38 : Wc * .1) * (.7 + R() * .5), key === 'compassplant' ? 'cut' : 'oval']); }
  } else {   // succulents
    if (key === 'pricklypear') { const s0 = H * .13, pad = (x, y, a, s, d) => { leaves.push([x, y, a, s, 'pad']); if (d < 4) { const kids = d === 0 ? 2 : 1 + (R() < .55 ? 1 : 0); for (let k = 0; k < kids; k++) { const na = a + (kids === 1 ? (R() - .5) * .7 : (k - .5) * 1.1 + (R() - .5) * .3); pad(x + Math.cos(a) * s * .85 + Math.cos(na) * s * .95, y + Math.sin(a) * s * .85 + Math.sin(na) * s * .95, na, s * (.86 + R() * .1), d + 1); } } }; pad(0, -s0, UP, s0, 0); }   // pads stacked on pads from the ground up
    else { const n = 26; for (let i = 0; i < n; i++) { const u = i / (n - 1) - .5, a = UP + u * 2.6 + (R() - .5) * .1, L = H * (.7 + R() * .3) * (1 - Math.abs(u) * .45); lines.push({ x: [0, Math.cos(a) * L * .5, Math.cos(a) * L], y: [-.02, Math.sin(a) * L * .5, Math.sin(a) * L], w: [W0 * 3, W0 * 2, W0 * .2], o: 0, blade: true }); } }
  }
  return { lines, dabs, flowers, leaves };
}

/* the plant at an age: data scaled by growth; cached by species, age step and variant */
const CACHE = new Map();
function plantGeo(key, yr, variant) {
  const D = ROOT_DATA[key]; if (!D) return null;
  const gR = Math.max(.12, 1 - Math.exp(-3 * Math.max(0, yr) / Math.max(.5, D.yrs))), gH = Math.max(.08, 1 - Math.exp(-3 * Math.max(0, yr) / Math.max(.5, D.yrs * (D.form === 'tree' ? 1.4 : 1)))), k = `${key}|${Math.round(gR * 40)}|${Math.round(gH * 40)}|${variant}`;
  if (CACHE.has(k)) return CACHE.get(k); if (CACHE.size > 400) CACHE.clear();
  const R = rng(hashStr(key) ^ (variant * 2654435761)), H = D.h * gH, Wc = (AGRO_LIB[key] ? agroRadiusM(key, yr) * 2 : D.spread * gH), T = D.typ * gR, M = Math.max(T, D.max * gR), Lr = Math.max(D.lat * gR, Wc * .3);
  const W0 = D.form === 'tree' ? Math.max(.03, (.04 + .025 * H)) : D.form === 'shrub' ? Math.max(.015, .012 * H + .01) : D.form === 'succulent' ? .02 : .0035;
  const arch = (D.form === 'tree' || D.form === 'shrub') && D.arch === 'fibrous' ? 'plate' : D.arch;   // a tree's fibrous mat is a shallow plate of fine roots, not a bunchgrass
  const g = { key, D, H, Wc, T, M, Lr, roots: rootSys(arch, R, T, M, Lr, Math.max(Wc * (D.form === 'grass' ? .6 : .25), .05), W0, D.form), top: topSys(key, D.form, R, H, Wc, W0) };
  CACHE.set(k, g); return g;
}

/* ink: every line cut into short runs and bucketed by width, so a plant is a few dozen strokes however many roots it has */
function inkLines(c, lines, ox, oy, k, col, alpha, flip, clipY) {
  const B = new Map();
  const floor = [.6, .42, .3, .22, .16, .12];   // a hairline's strength by branching order: the finest roots stay visible, as in the atlases
  for (const r of lines) { const n = r.x.length, fl = floor[Math.min(5, r.o)] * (k < 4 ? k / 4 : 1); for (let i = 0; i < n - 1; i += 3) { const j = Math.min(n - 1, i + 3), wpx = r.w[i] * k; if (wpx < .45 && fl < .04) break;
    const lw = wpx < .45 ? .45 : Math.round(wpx * 4) / 4, af = wpx < .45 ? Math.max(fl, Math.round(wpx / .45 * 8) / 8) : 1, key = lw + '|' + af + '|' + (wpx >= 1.2 ? 1 : 0); let p = B.get(key); if (!p) { p = new Path2D(); B.set(key, p); }
    p.moveTo(ox + flip * r.x[i] * k, oy + r.y[i] * k); for (let q = i + 1; q <= j; q++) p.lineTo(ox + flip * r.x[q] * k, oy + r.y[q] * k); } }
  c.save(); c.strokeStyle = col; c.lineCap = 'round'; c.lineJoin = 'round';
  for (const [key, p] of B) { const [lw, af, solid] = key.split('|').map(Number); c.lineWidth = lw; c.globalAlpha = solid ? Math.min(1, alpha * 1.15) : alpha * af; c.stroke(p); }
  c.restore();
}
function drawTop(c, g, ox, oy, k, alpha, flip) {
  const t = g.top, X = x => ox + flip * x * k, Y = y => oy + y * k;
  if (g.D.form === 'tree' || g.D.form === 'shrub') {   // a pale wash for the crown's mass, then branches, then the leaf dabs in ink
    if (t.dabs.length && g.Wc * k > 6) { c.save(); c.globalAlpha = alpha * .07; c.fillStyle = LEAF; c.beginPath(); for (const d of t.dabs) { c.moveTo(X(d[0]) + d[2] * k * 3, Y(d[1])); c.arc(X(d[0]), Y(d[1]), d[2] * k * 3, 0, TAU); } c.fill(); c.restore(); }
  }
  inkLines(c, t.lines.filter(l => !l.blade), ox, oy, k, g.D.form === 'tree' || g.D.form === 'shrub' ? '#3a3935' : INK, alpha * (g.D.form === 'tree' || g.D.form === 'shrub' ? .75 : .85), flip);
  for (const l of t.lines) if (l.blade) { const n = l.x.length - 1, bx = ox, by = oy, tx = ox + flip * l.x[n] * k, ty = oy + l.y[n] * k, wv = l.w[0] * k * .9, nx = -(ty - by), ny = tx - bx, nl = Math.hypot(nx, ny) || 1; c.save(); c.beginPath(); c.moveTo(bx + nx / nl * wv, by + ny / nl * wv); c.quadraticCurveTo((bx + tx) / 2 + nx / nl * wv * .8, (by + ty) / 2 + ny / nl * wv * .8, tx, ty); c.quadraticCurveTo((bx + tx) / 2 - nx / nl * wv * .8, (by + ty) / 2 - ny / nl * wv * .8, bx - nx / nl * wv, by - ny / nl * wv); c.closePath(); c.globalAlpha = alpha * .16; c.fillStyle = LEAF; c.fill(); c.globalAlpha = alpha * .8; c.strokeStyle = INK; c.lineWidth = .7; c.stroke(); c.restore(); }
  if (t.dabs.length) { const r0 = g.Wc * k; if (r0 > 4) { c.save(); c.strokeStyle = INK2; c.lineWidth = Math.max(.35, Math.min(.8, r0 / 160)); c.globalAlpha = alpha * Math.min(.6, .15 + r0 / 300); c.beginPath(); const every = r0 < 40 ? 6 : r0 < 90 ? 3 : 1;
    for (let di = 0; di < t.dabs.length; di += every) { const d = t.dabs[di], r = Math.max(.6, d[2] * k), a0 = (d[0] * 97 + d[1] * 53) % TAU; c.moveTo(X(d[0]) + Math.cos(a0) * r, Y(d[1]) + Math.sin(a0) * r); c.arc(X(d[0]), Y(d[1]), r, a0, a0 + 2.6); } c.stroke(); c.restore(); } }
  if (t.leaves.length) { c.save(); c.strokeStyle = INK; c.fillStyle = LEAF; c.lineWidth = .7;
    for (const [x, y, side, s, kind] of t.leaves) { const px = X(x), py = Y(y), r = s * k; if (r < .8) continue; c.globalAlpha = alpha * .8; c.beginPath();
      if (kind === 'pad') { c.ellipse(px, py, r * .62, r, (side - UP) * flip, 0, TAU); c.globalAlpha = alpha * .18; c.fill(); c.globalAlpha = alpha * .8; c.stroke(); c.beginPath(); for (let i = 0; i < 6; i++) { const a = i * 1.1, d = r * .45; c.moveTo(px + Math.cos(a) * d * .6, py + Math.sin(a) * d); c.arc(px + Math.cos(a) * d * .6, py + Math.sin(a) * d, .5, 0, TAU); } c.stroke(); continue; }
      const dir = side * flip; c.moveTo(px, py); c.quadraticCurveTo(px + dir * r * .5, py - r * .45, px + dir * r, py - r * .1); c.quadraticCurveTo(px + dir * r * .5, py + r * .25, px, py);
      if (kind === 'cut') { for (let i = 1; i < 4; i++) { const qx = px + dir * r * i / 4; c.moveTo(qx, py - r * .1 * i); c.lineTo(qx + dir * r * .08, py - r * .3); } }
      c.globalAlpha = alpha * .15; c.fill(); c.globalAlpha = alpha * .75; c.stroke(); }
    c.restore(); }
  if (t.flowers.length) { c.save(); c.strokeStyle = INK; c.fillStyle = INK; c.lineWidth = .7; c.globalAlpha = alpha * .85;
    for (const [x, y, kind, H] of t.flowers) { const px = X(x), py = Y(y), s = Math.max(1.2, H * k * .09); if (H * k < 8) continue; c.beginPath();
      if (kind === 'turkeyfoot') { for (const a of [-.5, 0, .45]) { c.moveTo(px, py); c.lineTo(px + Math.sin(a) * s * 1.6, py - Math.cos(a) * s * 1.8); } }
      else if (kind === 'panicle' || kind === 'plume') { for (let i = 0; i < 9; i++) { const yy = py + i * s * .25, d = s * (kind === 'plume' ? .35 : .9) * (1 - i / 10); c.moveTo(px, yy); c.lineTo(px - d, yy + s * .35); c.moveTo(px, yy); c.lineTo(px + d, yy + s * .35); } }
      else if (kind === 'flag' || kind === 'eyelash') { c.moveTo(px, py); c.lineTo(px, py + s * 1.6); for (let i = 0; i < (kind === 'flag' ? 7 : 2); i++) { const yy = py + i * s * .22; c.moveTo(px, yy); c.lineTo(px + s * .7, yy + s * .1); } }
      else if (kind === 'awn') { for (let i = 0; i < 6; i++) { c.moveTo(px, py + i * s * .3); c.quadraticCurveTo(px + s, py + i * s * .3 - s * .3, px + s * 1.8, py + i * s * .3 + s * .6); } }
      else if (kind === 'spike' || kind === 'wisp') { for (let i = 0; i < 8; i++) { c.moveTo(px - s * .18, py + i * s * .26); c.lineTo(px + s * .18, py + i * s * .26 + s * .12); } }
      else if (kind === 'yarrow') { for (let i = 0; i < 9; i++) { const a = (i / 8 - .5) * 1.6; c.moveTo(px + Math.sin(a) * s * 1.3 + .8, py - Math.cos(a) * s * .5); c.arc(px + Math.sin(a) * s * 1.3, py - Math.cos(a) * s * .5, .8, 0, TAU); } }
      else if (kind === 'lupine') { for (let i = 0; i < 10; i++) { const yy = py + i * s * .28; c.moveTo(px - s * .3 + .9, yy); c.arc(px - s * .3, yy, .9, 0, TAU); c.moveTo(px + s * .3 + .9, yy + s * .14); c.arc(px + s * .3, yy + s * .14, .9, 0, TAU); } }
      else if (kind === 'compassplant' || kind === 'comfrey') { for (let i = 0; i < 10; i++) { const a = i / 10 * TAU; c.moveTo(px, py); c.lineTo(px + Math.cos(a) * s, py + Math.sin(a) * s); } }
      else if (kind === 'agave') { for (let i = 0; i < 5; i++) { const yy = py + i * s * .6, d = s * 1.4 * (1 - i / 6); c.moveTo(px, yy); c.lineTo(px - d, yy - s * .3); c.moveTo(px, yy); c.lineTo(px + d, yy - s * .3); } }
      else { c.moveTo(px + s * .5, py); c.arc(px, py, s * .5, 0, TAU); }
      c.stroke(); }
    c.restore(); }
}
function drawPlant(c, g, ox, oy, k, alpha, flip, groundClip) {   // groundClip(c): a path below the ground, so roots never poke out of a slope
  c.save(); if (groundClip) { groundClip(c); c.clip(); }
  const body = g.roots.filter(r => r.body); inkLines(c, g.roots.filter(r => !r.body), ox, oy, k, SEPIA, alpha * .92, flip);
  for (const r of body) { c.beginPath(); for (let i = 0; i < r.x.length; i++) c.lineTo(ox + flip * (r.x[i] - r.w[i] / 2) * k, oy + r.y[i] * k); for (let i = r.x.length - 1; i >= 0; i--) c.lineTo(ox + flip * (r.x[i] + r.w[i] / 2) * k, oy + r.y[i] * k); c.closePath(); c.globalAlpha = alpha * .25; c.fillStyle = SEPIA; c.fill(); c.globalAlpha = alpha * .9; c.strokeStyle = SEPIA; c.lineWidth = .8; c.stroke(); }
  c.restore(); drawTop(c, g, ox, oy, k, alpha, flip);
}

/* which planted species sit near a section line: along-line position t (0..1), distance off it in metres */
function plantsNear(sec) {
  const [a, b] = sec, dx = b[0] - a[0], dy = b[1] - a[1], L2 = dx * dx + dy * dy || 1, m = cs(), out = [];
  for (const st of S.strokes) { if (st.kind !== 'tree' || !st.sp || !ROOT_DATA[st.sp] || !st.c) continue;
    const t = ((st.c[0] - a[0]) * dx + (st.c[1] - a[1]) * dy) / L2; if (t < -.01 || t > 1.01) continue;
    const d = Math.abs((st.c[0] - a[0]) * dy - (st.c[1] - a[1]) * dx) / Math.sqrt(L2) * m, D = ROOT_DATA[st.sp], reach = Math.max(4, (st.r || 0) * m, D.form === 'grass' || D.form === 'forb' ? 2 : 0);
    if (d <= reach) out.push({ st, sp: st.sp, t: Math.max(0, Math.min(1, t)), d, reach, seed: hashStr(st.c[0].toFixed(2) + ',' + st.c[1].toFixed(2)) }); }
  return out.sort((p, q) => q.d - p.d);   // furthest first, so the nearest draw on top
}
window.__rootsNear = sec => { bind(); return plantsNear(sec); };

/* in the profile, at true scale: the furthest drawn faintest, as a section shows what lies beyond the cut */
window.__rootsProfile = (c, sec, X, Y, n, gnd, pxm, mini) => { bind();
  const P = plantsNear(sec); if (!P.length) return 0; const yr = AGRO ? AGRO.year : 10, gy = t => { const q = t * n, i = Math.min(n - 1, Math.floor(q)), f = q - i; return gnd[i] * (1 - f) + gnd[i + 1] * f; };
  const clip = cc => { cc.beginPath(); cc.moveTo(X(0), Y(gnd[0])); for (let q = 1; q <= n; q++) cc.lineTo(X(q), Y(gnd[q])); cc.lineTo(X(n), 1e5); cc.lineTo(X(0), 1e5); cc.closePath(); };
  let drawn = 0;
  for (const p of P) { const g = plantGeo(p.sp, yr, p.seed % 4); if (!g) continue; const hp = Math.max(g.H, g.T) * pxm; if (hp < 3) continue;
    drawPlant(c, g, X(p.t * n), Y(gy(p.t)), pxm, 1 - .55 * Math.min(1, p.d / p.reach), p.seed & 1 ? 1 : -1, clip); drawn++; }
  return drawn;
};

/* the root chart: each species the section crosses once, side by side at one scale, against a depth ruler, named, with how deep it goes */
let lastKey = null;
{ const T = window.__topo && window.__topo(); if (T) for (const [k, D] of Object.entries(ROOT_DATA)) if (!T.AGRO_LIB[k] && D.agro) {   // the restoration grasses, cover crops and desert shrubs join agroforestry's library: [name, kind, canopy m, years, L a week, flowers, harvest, bees, note]
  const kind = D.form === 'succulent' ? 'shrub' : D.form, y = Math.max(.5, D.yrs);
  T.AGRO_LIB[k] = [D.common, kind, [+(D.spread * .7).toFixed(2), +(D.spread * 1.2).toFixed(2)], [Math.max(1, Math.round(y * .7)), Math.max(1, Math.round(y * 1.3))], D.agro.water, D.agro.flowers, D.agro.harvest, D.agro.bee, D.regen.replace(/\.$/, '').toLowerCase()]; } }

function chartPanel(c, G, px0, pw, h, uf, un, narrow) {   // narrow (a phone): names only, slimmer columns, and room at the bottom for the plan / 3d / section switch
  const top = narrow ? 34 : 40, bot = narrow ? 76 : 64, avail = h - top - bot, rw = narrow ? 36 : 46, mL = px0 + rw;
  const above = Math.max(...G.map(g => g.H * 1.1)), deepT = Math.max(...G.map(g => g.T)); let below = Math.max(...G.map(g => Math.min(g.M, Math.max(g.T * 2.2, deepT * 1.25))));
  const minCol = narrow ? 64 : 118, k0 = avail / (above + below), colW = (g, k) => Math.max(minCol, g.Wc * k * .85 + 12);
  let k = k0; const fitW = pw - rw; if (G.length * minCol < fitW && G.reduce((s, g) => s + colW(g, k), 0) > fitW) { let lo = 0, hi = k0; for (let it = 0; it < 30; it++) { const m = (lo + hi) / 2; if (G.reduce((s, g) => s + colW(g, m), 0) > fitW) hi = m; else lo = m; } k = Math.max(lo, k0 * .45); }   // never flatter than about half height: neighbours overlap instead
  if (k < k0) below = Math.min(Math.max(...G.map(g => g.M)), avail / k - above);   // when the width sets the scale, the spare height shows deeper soil, not blank paper
  const tot = Math.min(fitW, G.reduce((s, g) => s + colW(g, k), 0)), gy0 = top + above * k, bottomY = gy0 + below * k;
  // the ruler: depth below ground, rules across the panel like the six-foot lines of the prairie chart
  let stepU = niceStep((below * uf) / 4); while (stepU / uf * k < 16) stepU = niceStep(stepU * 2.2); const stepM = stepU / uf; c.font = font(10); c.textAlign = 'right'; c.textBaseline = 'middle';
  for (let d = 0; d <= below + 1e-6; d += stepM) { const y = gy0 + d * k; c.strokeStyle = d ? 'rgba(40,40,36,.16)' : INK; c.lineWidth = d ? .8 : 1.4; c.setLineDash(d ? [2, 4] : []); c.beginPath(); c.moveTo(mL - 4, y); c.lineTo(px0 + pw, y); c.stroke(); c.setLineDash([]); c.fillStyle = INK2; c.fillText(d ? `${+(d * uf).toFixed(2)} ${un}` : '0', mL - 8, y); }
  let stepA = niceStep((above * uf) / 3); while (stepA / uf * k < 16) stepA = niceStep(stepA * 2.2); for (let u = stepA; u <= above * uf + 1e-6; u += stepA) { const y = gy0 - u / uf * k; c.fillStyle = INK3; c.fillText(`${+u.toFixed(2)}`, mL - 8, y); c.strokeStyle = INK3; c.lineWidth = .8; c.beginPath(); c.moveTo(mL - 4, y); c.lineTo(mL, y); c.stroke(); }
  c.strokeStyle = INK2; c.lineWidth = 1; c.beginPath(); c.moveTo(mL, top - 4); c.lineTo(mL, bottomY); c.stroke();
  // the plants, each in its own column; roots may run under a neighbour, as they do in the ground
  let x = mL + 4 + Math.max(0, (fitW - tot) / 2); c.save(); c.beginPath(); c.rect(mL + 1, top - 30, px0 + pw - mL - 1, bottomY - top + 30); c.clip();
  const cols = [], squeeze = Math.min(1, fitW / G.reduce((s, g) => s + colW(g, k), 0)); for (const g of G) { const cw = colW(g, k) * squeeze, cx = x + cw / 2; cols.push([g, cx, cw]); x += cw; }
  for (const [g, cx] of cols) drawPlant(c, g, cx, gy0, k, 1, 1, null); c.restore();
  c.textBaseline = 'top'; c.textAlign = 'center';
  for (const [g, cx, cw] of cols) { const D = g.D;
    if (g.M > below + 1e-6) { c.strokeStyle = SEPIA; c.lineWidth = 1; c.beginPath(); c.moveTo(cx, bottomY - 14); c.lineTo(cx, bottomY - 2); c.moveTo(cx - 3, bottomY - 6); c.lineTo(cx, bottomY - 2); c.lineTo(cx + 3, bottomY - 6); c.stroke(); }
    c.fillStyle = INK; c.font = font(11, 600); c.fillText(D.common, cx, bottomY + 6, cw - 6);
    if (narrow) continue;
    c.fillStyle = INK2; c.font = `italic ${font(10)}`; c.fillText(D.latin.replace(/\s*\(.*?\)/g, ''), cx, bottomY + 19, cw - 6);
    c.font = font(10); c.fillStyle = INK3; c.fillText(`most roots to ${fL(g.T, 1)}`, cx, bottomY + 32, cw - 6); c.fillText(`deepest ${fL(g.M, 1)}`, cx, bottomY + 44, cw - 6); }
}
const niceStep = v => { const p = Math.pow(10, Math.floor(Math.log10(v))), f = v / p; return (f < 1.5 ? 1 : f < 3.5 ? 2 : f < 7.5 ? 5 : 10) * p; };
window.__rootsChart = (c, w, h, sec) => { bind();
  const yr = AGRO ? AGRO.year : 10, uf = isFt() ? 3.28084 : 1, un = isFt() ? 'ft' : 'm', seen = new Map();
  for (const p of plantsNear(sec).sort((p, q) => p.t - q.t)) if (!seen.has(p.sp)) seen.set(p.sp, p);
  { const key = [...seen.keys()].join(); if (key !== lastKey) { lastKey = key; if (rootInfo) setTimeout(rootInfo); } }   // the layer's words follow what the line crosses
  c.save(); c.fillStyle = PAPER; c.fillRect(0, 0, w, h); c.strokeStyle = 'rgba(40,40,36,.25)'; c.lineWidth = 1; c.beginPath(); c.moveTo(0, .5); c.lineTo(w, .5); c.stroke();
  c.fillStyle = INK; c.font = font(12, 600); c.textAlign = 'left'; c.textBaseline = 'top';
  c.fillText(`${w < 640 ? 'roots' : 'roots along the section'} · ${yr === 0 ? 'planting day' : yr + ' year' + (yr === 1 ? '' : 's') + ' after planting'}`, w < 640 ? 10 : 64, 10);
  if (!seen.size) { c.fillStyle = INK2; c.font = font(11); c.fillText('no species planted near this section line. plant with shape · agroforestry, then draw the section through them.', 64, 32); c.restore(); return; }
  const G = [...seen.values()].map(p => plantGeo(p.sp, yr, 0)).filter(Boolean);
  // woody and herbaceous each get their own panel and scale, as the atlases do: a grass beside a 15 m oak would be a speck
  const woody = G.filter(g => g.D.form === 'tree' || g.D.form === 'shrub'), herb = G.filter(g => !(g.D.form === 'tree' || g.D.form === 'shrub')), groups = [woody, herb].filter(a => a.length);
  const narrow = w < 640, mL = narrow ? 8 : 64, mR = narrow ? 8 : 24, gap = groups.length > 1 ? (narrow ? 12 : 34) : 0, span = w - mL - mR - gap; let x0 = mL;
  const natural = grp => { const above = Math.max(...grp.map(g => g.H * 1.1)), deepT = Math.max(...grp.map(g => g.T)), below = Math.max(...grp.map(g => Math.min(g.M, Math.max(g.T * 2.2, deepT * 1.25)))), k = (h - 104) / (above + below); return (narrow ? 36 : 46) + grp.reduce((s, g) => s + Math.max(narrow ? 64 : 118, g.Wc * k * .85 + 12), 0); };
  const nat = groups.map(natural), natSum = nat.reduce((a, b) => a + b, 0), need = groups.map(grp => (narrow ? 36 : 46) + grp.length * (narrow ? 64 : 118)), needSum = need.reduce((a, b) => a + b, 0), extra = span - needSum;   // each panel gets room for its labels first, the rest by how wide its plants want to be
  groups.forEach((grp, gi) => { const share = groups.length > 1 ? (extra > 0 ? (need[gi] + extra * nat[gi] / natSum) / span : need[gi] / needSum) : 1, gw = gi === groups.length - 1 ? w - mR - x0 : span * share;
    chartPanel(c, grp, x0, gw, h, uf, un, narrow); x0 += gw + gap; });
  c.restore();
};

/* the layer's words: what each species near the line does for the land, and where the numbers come from */
window.__rootsInfo = (sec) => { bind(); const seen = new Map(); for (const p of (sec ? plantsNear(sec) : [])) seen.set(p.sp, ROOT_DATA[p.sp]); return [...seen.entries()]; };
})();
