/* roots.js · planting in section: every species near a section line drawn with its root system, grown from published rooting depths and spreads (ROOT_DATA, with sources), in the ink of the root atlases (Weaver, Kutschera, Natura).
   two places: the plants at true scale in the profile, and under it a root chart, every species the section crosses at one scale against a depth ruler.
   loaded after topo.html's main script; uses its S, AGRO, AGRO_LIB, agroRadiusM, cs, fL, font, isFt, INK, INK2, INK3 */
(() => {
const ROOT_DATA = window.ROOT_DATA || {};   // from roots-data.js   // key → { common, latin, form, arch, h, spread, typ, max, lat, yrs, regen, conf, src }
let S, AGRO, AGRO_LIB, agroRadiusM, cs, fL, font, isFt, INK, INK2, INK3, PAPER, rootInfo, sectionProfile;   // topo's, through window.__topo
const bind = () => ({ S, AGRO, AGRO_LIB, agroRadiusM, cs, fL, font, isFt, INK, INK2, INK3, PAPER, rootInfo, sectionProfile } = window.__topo());
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
    const ww = P.keepW ? w : w * (1 - .82 * s / len); xs.push(x); ys.push(y); ws.push(ww);
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
  } else if (arch === 'palm') {   // palms: hundreds of roots of one thickness from a ball at the base; no taproot, no thickening; most shallow, some far out, a few deep
    const P = { tgt: 'side', dip: .45, grav: .035, wig: .22, gap: Math.max(.08, T * .2), brA: [.7, 1.4], clen: (s, len, R) => Math.min(.35, T * .3) * (.3 + R()), brW: .7, maxO: 2, keepW: true, kid: fine, inside: lim(Lr * 1.1, M) };
    for (let i = 0; i < 140 && budget.n > 0; i++) { const r = R(), deep = r < .12, far = !deep && r < .45, a = deep ? DOWN + (R() - .5) * .5 : DOWN + (R() < .5 ? -1 : 1) * (.35 + R() * 1.1), len = deep ? M * (.5 + R() * .5) : far ? Lr * (.5 + R() * .5) : T * (.4 + R() * .9);
      grow(R, out, (R() - .5) * W0 * 30, .02 + R() * .3, a, len, W0, 0, { ...P, tgt: deep ? 'down' : 'side' }, budget); }
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

/* ---------- the grown engine: space colonization (Runions et al. 2007) for crowns and roots, Leonardo's rule for thickness, lit foliage ----------
   branches grow toward points scattered through the space the plant fills: the crown's envelope above, and below a cloud whose depth follows the species'
   measured root profile (Gale & Grigal 1987: the fraction of roots above depth d is 1 − β^d, β fitted so 85% lie above "most roots to"). a limb's thickness then
   comes from what it carries: r^n of a fork = the sum of r^n of its branches (n 2.4), so the trunk is as heavy as its twigs require */
const LOOK = {   // for the painter: leaf, bark and form, in a phrase
  oak: 'broad dome of small cupped, spiny-edged, glossy dark-green evergreen leaves, crooked heavy limbs, furrowed grey bark',
  olive: 'gnarled, twisted silver-grey trunk, open rounded crown of narrow grey-green leaves silver beneath',
  fig: 'smooth pale grey bark, broad low crown of large deeply three-to-five-lobed leaves', pomegranate: 'multi-stemmed shrubby tree, small glossy narrow leaves, red flowers and fruit',
  carob: 'dense rounded evergreen crown of glossy dark pinnate leaves, stout trunk', mesquite: 'low spreading multi-stemmed tree, feathery bipinnate pale-green leaves, dark rough bark',
  paloverde: 'smooth blue-green bark and branches, airy crown of tiny leaves', desertwillow: 'open crown of long narrow willow-like leaves, trumpet flowers',
  lemon: 'rounded evergreen crown of glossy oval leaves with yellow fruit', avocado: 'large dense crown of big glossy oval leaves', almond: 'open vase-shaped crown of narrow pointed leaves',
  jujube: 'zigzag thorny branches, small glossy oval leaves', moringa: 'slender pale trunk, wispy crown of finely divided leaves',
  elder: 'multi-stemmed, flat clusters of cream flowers, pinnate leaves', guava: 'dense shrub of grey-green oval leaves', grape: 'twisting woody vine on a trellis, lobed leaves',
  rosemary: 'dense shrub of needle-like dark leaves', ceanothus: 'dense shrub of small dark leaves, blue flower clusters', toyon: 'dense evergreen shrub, toothed leathery leaves, red berries',
  sage: 'mound of silvery-white broad leaves, tall flower spikes', vetiver: 'tall stiff upright clump of narrow leaves', bigbluestem: 'tall bunchgrass with three-branched turkey-foot seed heads',
  agave: 'rosette of thick grey-green spine-tipped leaves', pricklypear: 'stacked flat oval pads with spines and areoles',
};
const HABIT = {   // per species: the crown's shape (centre height and half-height as fractions of the tree's height, lowest limbs), leaf texture, foliage tones shaded to lit
  oak: { crown: { cy: .55, ry: .45, base: .14, rx: 1 }, lean: .12, leaf: 'scallop', clump: .05, tones: ['#4c5638', '#7d8a5c', '#c3c8a4'], bark: '#3b3832' },
  olive: { crown: { cy: .58, ry: .4, base: .32, rx: 1 }, trunks: 2, trunkSplay: .5, gnarl: 3, lean: .3, scaffolds: 5, splay: 2.1, leaf: 'fine', clump: .045, tones: ['#56604c', '#8d9880', '#cdd3c2'], bark: '#625b51' },
  carob: { crown: { cy: .56, ry: .44, base: .2, rx: 1 }, lean: .1, scaffolds: 5, leaf: 'glossy', clump: .055, tones: ['#36432a', '#566a3e', '#97a97a'], bark: '#4e4840' },
  fig: { crown: { cy: .55, ry: .4, base: .22, rx: 1.08 }, trunks: 2, trunkSplay: .7, lean: .15, scaffolds: 5, splay: 2.2, leaf: 'broad', clump: .065, tones: ['#465c30', '#71904c', '#b4c88a'], bark: '#9b978d' },
  almond: { crown: { cy: .62, ry: .36, base: .3, rx: 1, taper: .45 }, lean: .08, scaffolds: 4, splay: 1.5, leaf: 'fine', clump: .04, tones: ['#4a5a36', '#7a8d58', '#bcc79a'], bark: '#4a433b' },
  pomegranate: { crown: { cy: .52, ry: .45, base: .1, rx: 1 }, trunks: 4, trunkSplay: .8, gnarl: 1.5, lean: .2, scaffolds: 4, leaf: 'fine', clump: .04, tones: ['#40532e', '#6b8448', '#aec07f'], bark: '#5a5248' },
  lemon: { crown: { cy: .5, ry: .48, base: .08, rx: 1 }, lean: .1, scaffolds: 5, leaf: 'glossy', clump: .05, tones: ['#2f4425', '#50683a', '#93a977'], bark: '#5a5550' },
  avocado: { crown: { cy: .55, ry: .45, base: .12, rx: 1 }, lean: .1, scaffolds: 5, leaf: 'glossy', clump: .06, tones: ['#2f4223', '#4f6837', '#8fa66f'], bark: '#4f4a43' },
  jujube: { crown: { cy: .58, ry: .4, base: .25, rx: 1 }, gnarl: 2, lean: .2, scaffolds: 4, leaf: 'feather', clump: .04, tones: ['#465a32', '#738c50', '#b6c690'], bark: '#4a4038' },
  mesquite: { crown: { cy: .6, ry: .32, base: .2, rx: 1.12 }, trunks: 3, trunkSplay: .7, gnarl: 2.5, lean: .35, scaffolds: 6, splay: 2.4, leaf: 'feather', clump: .045, tones: ['#56663e', '#869a62', '#c6d1a4'], bark: '#3e362e' },
  paloverde: { crown: { cy: .58, ry: .38, base: .2, rx: 1.05 }, trunks: 2, trunkSplay: .6, lean: .2, scaffolds: 5, splay: 2.2, leaf: 'feather', clump: .035, tones: ['#6f8a4a', '#9cb46e', '#d3dfae'], bark: '#7f9c64' },
  desertwillow: { crown: { cy: .58, ry: .4, base: .25, rx: 1 }, trunks: 2, trunkSplay: .5, gnarl: 1.5, lean: .25, scaffolds: 4, leaf: 'fine', clump: .04, tones: ['#4f6238', '#7d9356', '#bfcd9a'], bark: '#5a5045' },
  moringa: { crown: { cy: .62, ry: .34, base: .35, rx: .9 }, lean: .15, scaffolds: 4, splay: 1.6, leaf: 'feather', clump: .035, tones: ['#5a7040', '#8aa462', '#c8d7a2'], bark: '#a29a8a' },
  ironwood: { crown: { cy: .58, ry: .38, base: .2, rx: 1.05 }, trunks: 2, trunkSplay: .7, gnarl: 2, lean: .25, scaffolds: 5, splay: 2.2, leaf: 'feather', clump: .04, tones: ['#5b6a52', '#8a9a80', '#c4cdb8'], bark: '#5d5650' },
  stonepine: { crown: { cy: .82, ry: .17, base: .62, rx: 1.1 }, lean: .1, scaffolds: 5, splay: 2.3, leaf: 'needle', clump: .05, tones: ['#2f3f2a', '#4d6342', '#8ea27e'], bark: '#7b5d45' },
  cypress: { crown: { cy: .5, ry: .5, base: .04, rx: 1, taper: -.75 }, leader: true, lean: .02, leaf: 'scale', clump: .09, tones: ['#253222', '#3d5135', '#71876a'], bark: '#5a4a3d' },
  corkoak: { crown: { cy: .56, ry: .42, base: .2, rx: 1.05 }, gnarl: 2, lean: .2, scaffolds: 5, splay: 2, leaf: 'scallop', clump: .05, tones: ['#3f4c33', '#677852', '#a9b58f'], bark: '#8d7a63' },
  bay: { crown: { cy: .52, ry: .48, base: .06, rx: .8, taper: -.3 }, trunks: 3, trunkSplay: .3, lean: .08, scaffolds: 5, splay: 1.2, leaf: 'glossy', clump: .05, tones: ['#2e3f26', '#4d6440', '#8ea47c'], bark: '#4d4a44' },
  pistachio: { crown: { cy: .55, ry: .42, base: .2, rx: 1.05 }, trunks: 2, trunkSplay: .5, gnarl: 1.5, lean: .2, scaffolds: 5, leaf: 'broad', clump: .05, tones: ['#4b5c38', '#7a8f5c', '#bccb98'], bark: '#7d7466' },
  strawberrytree: { crown: { cy: .55, ry: .45, base: .12, rx: 1 }, trunks: 3, trunkSplay: .6, gnarl: 1.5, lean: .2, scaffolds: 5, leaf: 'glossy', clump: .045, tones: ['#344528', '#55703f', '#97ad7a'], bark: '#8a4a32' },
};
const SHRUB = { crown: { cy: .5, ry: .5, base: .03, rx: 1 }, trunks: 5, trunkSplay: 1.3, lean: .2, scaffolds: 7, splay: 2.4, leaf: 'fine', clump: .07, tones: ['#4c5a3e', '#7c8c66', '#bcc6a8'], bark: '#5a5248' };
const SHRUBS = {   // shrubs that differ from the default mound: tone, leaf and stance
  saltbush: { tones: ['#7b8170', '#a5ab98', '#d6d9cb'] }, jojoba: { leaf: 'glossy', tones: ['#56634c', '#808f72', '#b8c2a8'] }, creosote: { crown: { cy: .55, ry: .45, base: .12, rx: 1, taper: .35 }, trunks: 7, trunkSplay: 1.5, leaf: 'glossy', clump: .05, tones: ['#3d4a2c', '#62733f', '#a2b07a'] },
  sage: { tones: ['#8e9688', '#b8beb2', '#e3e6dc'], leaf: 'broad' }, rosemary: { leaf: 'needle', tones: ['#33402c', '#566649', '#909e83'] }, lavender: { leaf: 'needle', tones: ['#6f7a6a', '#98a291', '#c9cfc2'] },
  ceanothus: { leaf: 'glossy', tones: ['#2f3d27', '#4f6240', '#8a9c78'] }, toyon: { leaf: 'glossy', crown: { cy: .5, ry: .5, base: .08, rx: 1 }, tones: ['#2f4226', '#4f6a3e', '#8ea77a'] },
  guava: { leaf: 'glossy', tones: ['#5d6b54', '#87957c', '#bcc6b0'] }, elder: { leaf: 'feather', tones: ['#44582f', '#6f8a4c', '#b0c58c'] }, lupine: { leaf: 'feather', tones: ['#6f7d68', '#9aa891', '#cdd5c4'] },
  myrtle: { leaf: 'glossy', tones: ['#2e3f27', '#4b6340', '#8aa27c'] }, lentisk: { leaf: 'glossy', tones: ['#33452a', '#536a43', '#93a77f'] }, thyme: { leaf: 'needle', tones: ['#5a6650', '#84907a', '#b9c1ad'] },
  pigeonpea: { leaf: 'feather', tones: ['#4f6338', '#7a915a', '#b6c793'] }, grape: { leaf: 'broad', trunks: 1, gnarl: 3, tones: ['#4c6232', '#79934f', '#b9cc8d'] },
};
const habitFor = (key, D) => HABIT[key] || (D && D.form === 'shrub' && !FORM[key] ? { ...SHRUB, ...(SHRUBS[key] || {}) } : null);
function colonize(R, nodes, ax, ay, P) {   // nodes: {x, y, p}; grows in place
  const cell = P.di, grid = new Map(), live = new Uint8Array(ax.length).fill(1), key = (x, y) => (Math.floor(x / cell) + 4096) * 8192 + Math.floor(y / cell) + 4096;
  const add = i => { if (nodes[i].ng) return; const k = key(nodes[i].x, nodes[i].y);   // ng: the trunk, which carries the limbs but sprouts nothing itself
 let a = grid.get(k); if (!a) grid.set(k, a = []); a.push(i); };
  nodes.forEach((_, i) => add(i)); let nLive = ax.length;
  for (let it = 0; it < P.maxIt && nLive > 0 && nodes.length < P.maxN; it++) {
    const sx = new Map();
    for (let j = 0; j < ax.length; j++) { if (!live[j]) continue; const x = ax[j], y = ay[j], gx = Math.floor(x / cell) + 4096, gy = Math.floor(y / cell) + 4096; let best = -1, bd = P.di * P.di;
      for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) { const L = grid.get((gx + a) * 8192 + gy + b); if (L) for (const i of L) { const d = (nodes[i].x - x) ** 2 + (nodes[i].y - y) ** 2; if (d < bd) { bd = d; best = i; } } }
      if (best < 0) continue; if (bd < P.dk * P.dk) { live[j] = 0; nLive--; continue; }
      const d = Math.sqrt(bd), v = sx.get(best) || [0, 0, 0]; v[0] += (x - nodes[best].x) / d; v[1] += (y - nodes[best].y) / d; v[2]++; sx.set(best, v); }
    if (!sx.size) break;
    for (const [i, v] of sx) { const n = nodes[i], pd = n.p >= 0 ? [n.x - nodes[n.p].x, n.y - nodes[n.p].y] : [0, P.trop[1]], pl = Math.hypot(pd[0], pd[1]) || 1;
      let dx = v[0] / v[2] + P.trop[0] * P.tw + pd[0] / pl * P.inertia + (R() - .5) * P.jit, dy = v[1] / v[2] + P.trop[1] * P.tw + pd[1] / pl * P.inertia + (R() - .5) * P.jit; const l = Math.hypot(dx, dy); if (l < 1e-6) continue; dx /= l; dy /= l;
      const nx = n.x + dx * P.D, ny = n.y + dy * P.D; if (n.kids && n.kids.some(k => Math.hypot(nodes[k].x - nx, nodes[k].y - ny) < P.D * .35)) continue;   // no twin twigs from two attractors pulling the same way
      if (P.floor != null && ny < P.floor) continue;
      nodes.push({ x: nx, y: ny, p: i }); (n.kids || (n.kids = [])).push(nodes.length - 1); add(nodes.length - 1); }
  }
  return nodes;
}
function warp(nodes, amp, R) {   // a slow bend through the whole system, stronger further from the stem: roots and limbs wander as they do in the ground and the air
  const f1 = 2.3 / (amp * 18), f2 = 1.7 / (amp * 18), p1 = R() * TAU, p2 = R() * TAU;
  for (const nd of nodes) { if (nd.ng) continue; const d = Math.min(1, Math.hypot(nd.x, nd.y) / (amp * 8)); nd.x += Math.sin(nd.y * f1 + p1) * amp * d; nd.y += Math.sin(nd.x * f2 + p2) * amp * d * .6; }
}
function pipe(nodes, rTrunk, n, rMin) {   // Leonardo: thickness from the tips back to the trunk
  const tips = new Float64Array(nodes.length); for (let i = nodes.length - 1; i >= 0; i--) { if (!tips[i]) tips[i] = 1; const p = nodes[i].p; if (p >= 0) tips[p] += tips[i]; }
  const r0 = rTrunk / Math.pow(tips[0], 1 / n); for (let i = 0; i < nodes.length; i++) nodes[i].r = Math.max(rMin, r0 * Math.pow(tips[i], 1 / n));
  for (let s = 0; s < 2; s++) for (let i = 1; i < nodes.length; i++) { const nd = nodes[i], p = nodes[nd.p]; if (nd.kids && nd.kids.length === 1 && p) { const c = nodes[nd.kids[0]]; nd.x = nd.x * .5 + (p.x + c.x) * .25; nd.y = nd.y * .5 + (p.y + c.y) * .25; } }   // ease the steps out of the chains
  return nodes;
}
function scTree(key, R, D, H, Wc, T, M, Lr, W0) {
  const hb = habitFor(key, D), cr = hb.crown, rx = Wc / 2 * cr.rx, ry = H * cr.ry, cy = -H * cr.cy, base = -H * cr.base;
  // above: attractors through the crown, thinner at its heart so the outside carries the leaves
  const nA = D.form === 'tree' ? 4200 : 2600, ax = [], ay = []; let tries = 0; while (ax.length < nA && tries++ < 40000) { const u = R() * 2 - 1, v = R() * 2 - 1, r2 = u * u + v * v; if (r2 > 1 || (r2 < .25 && R() < .6)) continue; const tp = cr.taper || 0, f = tp > 0 ? 1 - tp * (v + 1) / 2 : 1 + tp * (1 - v) / 2; if (Math.abs(u) > f) continue; const x = u * rx, y = cy + v * ry * (v > 0 ? .85 : 1); if (y > base) continue; ax.push(x); ay.push(y); }
  const crown = [{ x: 0, y: 0, p: -1, ng: true }], nT = hb.trunks || 1, tops = []; for (let t = 0; t < nT; t++) { let y = 0, x = 0, i = 0, a = UP + (nT > 1 ? (t / (nT - 1) - .5) * (hb.trunkSplay || .5) : (R() - .5) * hb.lean); const step = H / 60, g = (hb.gnarl || 0) * .05;
    const stop = hb.leader ? -H * .9 : base * (nT > 1 ? .85 + R() * .15 : 1); while (y > stop + step) { a += (R() - .5) * g + Math.sin(UP - a) * .02; x += Math.cos(a) * step; y += Math.sin(a) * step; crown.push({ x, y, p: i, ng: !hb.leader || y > base });   /* a leader runs up the middle and sprouts all the way */ (crown[i].kids || (crown[i].kids = [])).push(crown.length - 1); i = crown.length - 1; } tops.push(i); }
  { const nS = hb.leader ? 0 : hb.scaffolds || 4, D = H / 95; for (let k = 0; k < nS; k++) { const top = tops[k % tops.length]; let a = UP + ((k + .5) / nS - .5) * (hb.splay || 1.7) + (R() - .5) * .3 + (crown[top].x) / (rx || 1) * .4, i = top, x = crown[top].x, y = crown[top].y; const L = Math.max(rx, ry) * (.6 + R() * .25);
    for (let s = 0; s < L; s += D) { a += (R() - .5) * (.35 + (hb.gnarl || 0) * .12) + Math.sin(UP - a) * .03; x += Math.cos(a) * D; y += Math.sin(a) * D; if (y < cy - ry * .6) break; crown.push({ x, y, p: i }); (crown[i].kids || (crown[i].kids = [])).push(crown.length - 1); i = crown.length - 1; } } }
  colonize(R, crown, ax, ay, { D: H / 95, di: H / 8, dk: H / 40, trop: [0, -1], tw: .08, inertia: .15, jit: .55, maxIt: 420, maxN: 14000 });
  warp(crown, Math.max(rx, ry) * .05 * (1 + (hb.gnarl || 0) * .4), R); pipe(crown, W0 / 2 / Math.sqrt(nT), 2.4, .004);
  // below: the measured profile. β from "most roots to"; lateral reach narrowing with depth
  const beta = Math.pow(.15, 1 / Math.max(.05, T)), bx = [], by = [];
  while (bx.length < nA) { const d = Math.min(M, Math.log(1 - R() * .999) / Math.log(beta)); if (d < .03) continue; const reach = D.arch === 'taproot' ? Lr * Math.max(.04, Math.exp(-d / (T * .9))) : Lr * Math.max(.05, 1 - Math.pow(d / M, .55)),   /* a taproot species spreads wide only near the surface */ x = (R() < .5 ? -1 : 1) * reach * Math.pow(R(), 1.25); bx.push(x); by.push(d); }
  const roots = [{ x: 0, y: 0, p: -1 }, { x: 0, y: .05, p: 0 }]; roots[0].kids = [1];
  if (D.arch === 'taproot') { let x = 0, y = .05, i = 1, a = DOWN; const st = Math.max(Lr, T * 2.5) / 230 * 2; while (y < M * .97) { a += (R() - .5) * .25 + Math.sin(DOWN - a) * .12; x += Math.cos(a) * st; y += Math.sin(a) * st; roots.push({ x, y, p: i, ng: !((roots.length % 9 === 0) || (y < T * .6 && roots.length % 3 === 0)) }); (roots[i].kids || (roots[i].kids = [])).push(roots.length - 1); i = roots.length - 1; } }   // side roots leave the taproot at intervals, closer together near the top
  const S0 = D.arch === 'taproot' ? Math.max(Lr, T * 2.5) : Lr + M;   // a taproot already reaches the depth; the rest of the system is sized by its spread
  colonize(R, roots, bx, by, { D: S0 / 230, di: S0 / 11, dk: S0 / 110, trop: [0, 1], tw: .07, inertia: .12, jit: .7, maxIt: 520, maxN: 16000, floor: .02 });
  warp(roots, (Lr + M) * .03, R); pipe(roots, W0 * .55, 2.3, .0025);
  const fine = [], fb = { n: 40000 }, fl = Math.max(.15, (Lr + M) / 28), FP = { ...FINE(fl, 4), wig: .7, gap: fl * .18 }; FP.clen = (s, len, R) => fl * .3 * (.3 + R()); FP.kid = { ...FINE(fl, 4), clen: (s, len, R) => fl * .12 * (.3 + R()) };
  const rFine = Math.min(...roots.map(n => n.r)) * 4; for (let i = 2; i < roots.length; i++) { const nd = roots[i]; if (nd.r > rFine || R() < .25) continue; for (let j = 0; j < 3 && fb.n > 0; j++) { const a = Math.atan2(nd.y - roots[nd.p].y, nd.x - roots[nd.p].x) + (R() < .5 ? -1 : 1) * (.6 + R() * .9); grow(R, fine, nd.x, nd.y, a, fl * (.4 + R()), nd.r * 1.2, 2, FP, fb); } }
  // leaves: a clump at every crown tip, its tone from the light coming from the upper left
  const twigs = [], tb = { n: 9000 }, tl = Wc * .045, TW = { tgt: 'up', grav: .02, wig: .6, gap: tl * .4, brA: [.4, .9], clen: (s, len, R) => (len - s) * .6, brW: .6, maxO: 2, step: tl / 6 }; TW.kid = TW;
  const ends = []; for (const nd of crown) if (!nd.kids && nd.y < base * .6) for (let j = 0; j < 3 && tb.n > 0; j++) { const a = Math.atan2(nd.y - crown[nd.p].y, nd.x - crown[nd.p].x) + (R() - .5) * 1.6; ends.push(grow(R, twigs, nd.x, nd.y, a, tl * (.5 + R()), nd.r * 1.4, 1, TW, tb)); }
  const rLeaf = Math.min(...crown.map(n => n.r)) * 3.5, inner = crown.filter(n => !n.ng && n.r < rLeaf && n.kids && n.y < base * .7 && R() < .3).map(n => ({ x: n.x, y: n.y }));
  const tips = ends.map(([x, y]) => ({ x, y })).concat(inner), Lx = -.55, Ly = -.83;
  const clumps = []; for (const nd of tips) { const u = nd.x / rx, v = (nd.y - cy) / ry, s0 = .5 + .55 * (u * Lx + v * Ly); for (let q = 0; q < 2; q++) { const a = R() * TAU, d = Wc * hb.clump * .5 * R(), s = Math.max(0, Math.min(1, s0 + (R() - .5) * .3 - (q === 0 ? .12 : 0))); clumps.push([nd.x + Math.cos(a) * d, nd.y + Math.sin(a) * d * .8, Wc * hb.clump * (.22 + R() * .22), s]); } }
  clumps.sort((a, b) => a[3] - b[3]);
  return { crown, roots, clumps, hb, fine, twigs };
}
const mix = (a, b, t) => { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)), A = p(a), B = p(b); return `rgb(${A.map((v, i) => Math.round(v + (B[i] - v) * t)).join(',')})`; };
function scWood(c, nodes, ox, oy, k, flip, col, shade, alpha) {   // every segment at its own thickness, opaque, thick over thin; a darker band down the shaded side of anything wide enough
  const B = new Map(); for (let i = 1; i < nodes.length; i++) { const nd = nodes[i], p = nodes[nd.p], w = nd.r * 2 * k; if (w < .25) continue; const q = w < 1 ? Math.round(w * 8) / 8 : Math.round(w * 2) / 2; let a = B.get(q); if (!a) B.set(q, a = []); a.push(p.x, p.y, nd.x, nd.y); }
  const ws = [...B.keys()].sort((a, b) => a - b); c.save(); c.lineCap = 'round'; c.lineJoin = 'round';
  for (const w of ws) { const a = B.get(w), path = new Path2D(); for (let i = 0; i < a.length; i += 4) { path.moveTo(ox + flip * a[i] * k, oy + a[i + 1] * k); path.lineTo(ox + flip * a[i + 2] * k, oy + a[i + 3] * k); }
    c.globalAlpha = alpha * (w < .6 ? .45 + w * .9 : 1); c.strokeStyle = col; c.lineWidth = Math.max(.5, w); c.stroke(path);
    if (w >= 3) { c.save(); c.translate(w * .22, 0); c.strokeStyle = shade; c.lineWidth = w * .42; c.globalAlpha = alpha * .85; c.stroke(path); c.restore(); c.save(); c.translate(-w * .28, 0); c.strokeStyle = 'rgba(255,255,255,.18)'; c.lineWidth = w * .14; c.stroke(path); c.restore(); } }
  c.restore();
}
function scLeaves(c, sc, ox, oy, k, flip, alpha) {
  const t = sc.hb.tones; c.save();
  c.fillStyle = t[0]; c.globalAlpha = alpha * .35; c.beginPath(); for (const [x, y, r] of sc.clumps) { const px = ox + flip * x * k + r * k * .3, py = oy + y * k + r * k * .35, rr = r * k * 1.05; if (rr < .4) continue; c.moveTo(px + rr, py); c.arc(px, py, rr, 0, TAU); } c.fill();
  for (const [x, y, r, s] of sc.clumps) { const px = ox + flip * x * k, py = oy + y * k, rr = r * k; if (rr < .4) continue; c.globalAlpha = alpha * .9; c.fillStyle = s < .5 ? mix(t[0], t[1], s * 2) : mix(t[1], t[2], (s - .5) * 2); c.beginPath(); c.arc(px, py, rr, 0, TAU); c.fill(); }
  // the leaves themselves: small scallops, crowded where the crown is in shadow, sparse in the light; an outline only on the lit side of each clump
  c.strokeStyle = '#2b2e22'; c.lineWidth = Math.max(.35, Math.min(.8, k * .03)); c.beginPath();
  for (const [x, y, r, s] of sc.clumps) { const px = ox + flip * x * k, py = oy + y * k, rr = r * k; if (rr < 1.6) continue; const m = Math.round(1 + (1 - s) * 5), lr = Math.max(.8, rr * .2);
    for (let i = 0; i < m; i++) { const a = (x * 131 + y * 71 + i * 2.4) % TAU, d = rr * Math.sqrt((i * .618 + Math.abs(x) * 3) % 1), qx = px + Math.cos(a) * d, qy = py + Math.sin(a) * d * .8, lf = sc.hb.leaf, o = (i * 1.7 + x * 5) % TAU;
      if (lf === 'fine' || lf === 'needle') { for (let j = -1; j <= 1; j++) { const b = o + j * .5, l = lr * (lf === 'needle' ? 1.6 : 1.3); c.moveTo(qx, qy); c.lineTo(qx + Math.cos(b) * l, qy + Math.sin(b) * l); } }   // narrow leaves, needles: short strokes in a spray
      else if (lf === 'feather') { const l = lr * 1.6; c.moveTo(qx - Math.cos(o) * l, qy - Math.sin(o) * l); c.lineTo(qx + Math.cos(o) * l, qy + Math.sin(o) * l); for (let t = -.8; t <= .8; t += .4) { const bx = qx + Math.cos(o) * l * t, by = qy + Math.sin(o) * l * t; c.moveTo(bx, by); c.lineTo(bx + Math.cos(o + 1.1) * l * .35, by + Math.sin(o + 1.1) * l * .35); c.moveTo(bx, by); c.lineTo(bx + Math.cos(o - 1.1) * l * .35, by + Math.sin(o - 1.1) * l * .35); } }   // pinnate: a midrib with leaflets
      else if (lf === 'glossy') { c.moveTo(qx + lr, qy); c.ellipse(qx, qy, lr, lr * .5, o, 0, TAU); c.moveTo(qx - lr * .3, qy - lr * .15); c.lineTo(qx + lr * .1, qy - lr * .3); }   // oval leaves with a glint
      else if (lf === 'broad') { const l = lr * 1.5; c.moveTo(qx, qy + l * .5); for (let j = 0; j < 5; j++) { const b = -Math.PI / 2 + (j - 2) * .55; c.lineTo(qx + Math.cos(b) * l, qy + Math.sin(b) * l * .8); c.lineTo(qx + Math.cos(b + .27) * l * .45, qy + Math.sin(b + .27) * l * .35); } }   // lobed, like a fig
      else if (lf === 'scale') { c.moveTo(qx - lr, qy); c.quadraticCurveTo(qx, qy - lr * .9, qx + lr, qy); }   // overlapping scales, a cypress's sprays
      else { c.moveTo(qx - lr, qy); c.quadraticCurveTo(qx - lr * .5, qy + lr * .9, qx, qy + lr * .1); c.quadraticCurveTo(qx + lr * .5, qy + lr * .9, qx + lr, qy); } }
    if (s > .45) { c.moveTo(px + Math.cos(3.4) * rr, py + Math.sin(3.4) * rr); c.arc(px, py, rr, 3.4, 4.9); } }
  c.globalAlpha = alpha * .55; c.stroke();
  if (LINE) { c.beginPath(); for (const [x, y, r, s] of sc.clumps) { const px = ox + flip * x * k, py = oy + y * k, rr = r * k; if (rr < 1) continue; const a0 = 2.6 + s * .6; c.moveTo(px + Math.cos(a0) * rr, py + Math.sin(a0) * rr); c.arc(px, py, rr, a0, a0 + 3.4 + (1 - s) * 1.6); } c.globalAlpha = alpha * .7; c.strokeStyle = INK; c.lineWidth = Math.max(.35, Math.min(.7, k * .025)); c.stroke(); }   // scalloped edges round every leaf mass, fuller on the shaded side
  c.restore();
}

/* ---------- palms and cacti: drawn from their parts, not grown ----------
   a palm is a column and a crown of fronds (fan or feather), sometimes a skirt of dead ones; a cactus is a ribbed column with arms, a barrel, a chain of joints,
   a fountain of whips, or a rosette of leaves. every dimension comes from the species' height and spread; a seed per plant varies the rest */
const FORM = {   // per species: what to draw above ground
  fanpalm: { t: 'palm', frond: 'fan', trunkW: .9, skirt: .55, n: 28, bark: '#8a7a62' }, mexfanpalm: { t: 'palm', frond: 'fan', trunkW: .4, skirt: .25, n: 24, bark: '#8f8270' },
  datepalm: { t: 'palm', frond: 'feather', trunkW: .5, boots: true, n: 26, fruit: true, bark: '#7d6a50' }, medfanpalm: { t: 'palm', frond: 'fan', trunkW: .22, stems: 4, n: 14, bark: '#6f6250', boots: true },
  bluehesper: { t: 'palm', frond: 'fan', trunkW: .45, skirt: .2, n: 20, bark: '#8d8578', leaf: '#9fb3b4' }, guadalupepalm: { t: 'palm', frond: 'fan', trunkW: .4, n: 18, bark: '#8a8070' },
  cardon: { t: 'column', w: .7, arms: 6, ribs: 13 }, saguaro: { t: 'column', w: .6, arms: 3, ribs: 13 }, barrel: { t: 'barrel', ribs: 22 }, cholla: { t: 'cholla' }, ocotillo: { t: 'whips', n: 18 },
  yucca: { t: 'rosette', n: 90, narrow: true, round: true, stalk: 'white' }, mojaveyucca: { t: 'rosette', n: 40, narrow: true, trunk: true }, shawagave: { t: 'rosette', n: 28, broad: true },
  americana: { t: 'rosette', n: 30, broad: true, recurve: true }, agave: { t: 'rosette', n: 30, broad: true }, aloe: { t: 'rosette', n: 16, teeth: true, stalk: 'orange', stems: 6 }, dudleya: { t: 'rosette', n: 22, broad: true, chalk: true },
};
const fillStroke = (c, fill, a, lw) => { c.globalAlpha = a; c.fillStyle = fill; c.fill(); c.globalAlpha = Math.min(1, a + .25); c.strokeStyle = INK; c.lineWidth = lw; c.stroke(); };
function drawForm(c, g, ox, oy, k, alpha, flip, seed) {
  const F = FORM[g.key], R = rng(hashStr(g.key) ^ (seed || 0)), H = g.H, Wc = g.Wc, X = x => ox + flip * x * k, Y = y => oy + y * k, lw = Math.max(.4, Math.min(1, k * .02)), green = F.leaf || '#7f9068';
  c.save(); c.lineJoin = 'round'; c.lineCap = 'round';
  if (F.t === 'palm') {
    const fl = Math.max(.8, Wc / 2), stems = F.stems || 1;
    for (let s = 0; s < stems; s++) { const sx = stems > 1 ? (s / (stems - 1) - .5) * Wc * .35 : 0, h = stems > 1 ? H * (.45 + R() * .5) : H, th = Math.max(.3, h - fl * .45), bend = (R() - .5) * th * .12 + (stems > 1 ? sx * .5 : 0), tw = F.trunkW * (stems > 1 ? 1 : Math.min(1, .35 + h / 20));
      const px = t => sx + bend * t * t, wAt = t => tw * (1.35 - .35 * Math.min(1, t * 3)) * (1 - .25 * t);
      // trunk: a filled column, then its texture: crossed leaf bases (boots) or rings
      c.beginPath(); for (let i = 0; i <= 20; i++) { const t = i / 20; c.lineTo(X(px(t) - wAt(t) / 2), Y(-th * t)); } for (let i = 20; i >= 0; i--) { const t = i / 20; c.lineTo(X(px(t) + wAt(t) / 2), Y(-th * t)); } c.closePath(); fillStroke(c, F.bark, alpha * .75, lw);
      c.beginPath(); const step = Math.max(.12, tw * .35);
      for (let y = step; y < th; y += step) { const t = y / th, w = wAt(t) / 2, x0 = px(t); if (F.boots) { c.moveTo(X(x0 - w), Y(-y)); c.lineTo(X(x0), Y(-y - step * .6)); c.lineTo(X(x0 + w), Y(-y)); } else { c.moveTo(X(x0 - w), Y(-y)); c.quadraticCurveTo(X(x0), Y(-y + step * .25), X(x0 + w), Y(-y)); } }
      c.globalAlpha = alpha * .55; c.strokeStyle = INK; c.lineWidth = lw * .8; c.stroke(); c.save(); c.beginPath(); for (let i = 0; i <= 20; i++) { const t = i / 20; c.lineTo(X(px(t) + wAt(t) * .15), Y(-th * t)); } for (let i = 20; i >= 0; i--) { const t = i / 20; c.lineTo(X(px(t) + wAt(t) / 2), Y(-th * t)); } c.globalAlpha = alpha * .22; c.fillStyle = '#2a241c'; c.fill(); c.restore();
      const ax = px(1), ay = -th;
      // the skirt: dead fronds hanging down the trunk, straw coloured
      if (F.skirt) { const sl = th * F.skirt, sw = fl * .55; c.beginPath(); c.moveTo(X(ax - sw * .55), Y(ay)); c.quadraticCurveTo(X(ax - sw * .6), Y(ay + sl * .6), X(ax - tw * .7), Y(ay + sl)); c.lineTo(X(ax + tw * .7), Y(ay + sl)); c.quadraticCurveTo(X(ax + sw * .6), Y(ay + sl * .6), X(ax + sw * .55), Y(ay)); c.closePath(); fillStroke(c, '#c2ab7a', alpha * .8, lw);
        c.beginPath(); for (let i = 0; i < 40; i++) { const u = (i / 39 - .5) * 2, x = ax + u * sw * .5 * (1 - .4 * R()), len = sl * (.55 + R() * .45); c.moveTo(X(x), Y(ay + R() * sl * .1)); c.lineTo(X(x * .95 + ax * .05), Y(ay + len)); } c.globalAlpha = alpha * .5; c.strokeStyle = '#5a4a30'; c.lineWidth = lw * .7; c.stroke(); }
      // fronds: from the apex, the youngest up, the oldest drooping
      const n = Math.round(F.n * (stems > 1 ? .6 : 1)), frs = [];
      for (let i = 0; i < n; i++) { const u = i / (n - 1), a = -Math.PI - .55 + u * (Math.PI + 1.1) + (R() - .5) * .18, droop = Math.max(.1, (1 - Math.abs(Math.sin(a))) * .8 + (Math.sin(a) > 0 ? .5 : 0)); frs.push([a, droop, R(), .25 + R() * .75]); }
      frs.sort((p, q) => Math.abs(Math.sin(q[0])) - Math.abs(Math.sin(p[0])));   // side fronds behind, upright ones in front
      for (const [a, droop, r, face] of frs) {
        if (F.frond === 'feather') {   // a long arching rachis with leaflets in a V
          const L = fl * (.85 + r * .3), ex = ax + Math.cos(a) * L, ey = ay + Math.sin(a) * L * .7 + droop * L * .55, cx = ax + Math.cos(a) * L * .55, cy = ay + Math.sin(a) * L * .55 - L * .08;
          c.beginPath(); c.moveTo(X(ax), Y(ay)); c.quadraticCurveTo(X(cx), Y(cy), X(ex), Y(ey)); c.globalAlpha = alpha * .9; c.strokeStyle = '#4a5233'; c.lineWidth = Math.max(.5, .035 * k); c.stroke();
          c.beginPath(); for (let t = .18; t < 1; t += .045) { const qx = (1 - t) ** 2 * ax + 2 * (1 - t) * t * cx + t * t * ex, qy = (1 - t) ** 2 * ay + 2 * (1 - t) * t * cy + t * t * ey, dx = 2 * (1 - t) * (cx - ax) + 2 * t * (ex - cx), dy = 2 * (1 - t) * (cy - ay) + 2 * t * (ey - cy), dl = Math.hypot(dx, dy) || 1, lf = L * .2 * (1 - t * .7);
            for (const sd of [-1, 1]) { const nx = -dy / dl * sd, ny = dx / dl * sd; c.moveTo(X(qx), Y(qy)); c.lineTo(X(qx + (nx * .8 + dx / dl * .45) * lf), Y(qy + (ny * .8 + dy / dl * .45) * lf + lf * .25)); } }
          c.globalAlpha = alpha * .8; c.strokeStyle = green; c.lineWidth = Math.max(.4, .02 * k); c.stroke(); }
        else {   // a fan: a petiole, then segments radiating from its end, their tips drooping
          const pl = fl * .5, bx = ax + Math.cos(a) * pl, by = ay + Math.sin(a) * pl + droop * pl * .3, br = fl * (.55 + r * .2), seg = 22;
          c.beginPath(); c.moveTo(X(ax), Y(ay)); c.lineTo(X(bx), Y(by)); c.globalAlpha = alpha * .9; c.strokeStyle = '#4d5236'; c.lineWidth = Math.max(.5, .03 * k); c.stroke();
          c.beginPath(); c.moveTo(X(bx), Y(by)); const tips = []; for (let j = 0; j <= seg; j++) { const b = a + (j / seg - .5) * 2.1 * face, tx = bx + Math.cos(b) * br, ty = by + Math.sin(b) * br * .8 + droop * br * .35 + (j % 2) * br * .04; tips.push([tx, ty]); c.lineTo(X(tx), Y(ty)); } c.closePath(); fillStroke(c, green, alpha * .55, lw * .7);
          c.beginPath(); for (const [tx, ty] of tips) { c.moveTo(X(bx), Y(by)); c.lineTo(X(bx + (tx - bx) * .82), Y(by + (ty - by) * .82)); c.moveTo(X(bx + (tx - bx) * .82), Y(by + (ty - by) * .82)); c.lineTo(X(tx + (R() - .5) * br * .05), Y(ty + br * .12)); } c.globalAlpha = alpha * .45; c.strokeStyle = INK; c.lineWidth = lw * .6; c.stroke(); } }
      if (F.fruit) { c.beginPath(); for (let i = 0; i < 4; i++) { const fx = ax + (i - 1.5) * fl * .12, fy = ay + fl * .15; for (let j = 0; j < 14; j++) { const qx = fx + (R() - .5) * fl * .1, qy = fy + R() * fl * .3; c.moveTo(X(qx) + 1.4, Y(qy)); c.arc(X(qx), Y(qy), Math.max(.8, .03 * k), 0, TAU); } } c.globalAlpha = alpha * .8; c.fillStyle = '#b8742c'; c.fill(); }
    }
  } else if (F.t === 'column' || F.t === 'barrel') {   // ribbed columns: a rounded top, ribs drawn as curves across the cylinder, spines as ticks, the shaded side darker
    const col = (x0, y0, w, h, lean) => { const hw = w / 2, top = y0 - h, body = new Path2D(); body.moveTo(X(x0 - hw), Y(y0)); body.lineTo(X(x0 - hw + lean), Y(top + hw)); body.quadraticCurveTo(X(x0 + lean), Y(top - hw * .15), X(x0 + hw + lean), Y(top + hw)); body.lineTo(X(x0 + hw), Y(y0)); body.closePath();
      c.globalAlpha = alpha * .8; c.fillStyle = '#7f9268'; c.fill(body); c.save(); c.clip(body); c.globalAlpha = alpha * .25; c.fillStyle = '#26301c'; c.fillRect(X(x0 + hw * .25) - (flip < 0 ? Math.abs(X(x0 + hw) - X(x0 + hw * .25)) : 0), Y(top - hw), Math.abs(X(x0 + hw) - X(x0 + hw * .25)) + 2, Math.abs(Y(y0) - Y(top - hw)));
        c.beginPath(); const nr = Math.min(9, F.ribs / 2 | 0); for (let i = 1; i < nr; i++) { const u = Math.sin((i / nr - .5) * Math.PI) * hw; c.moveTo(X(x0 + u), Y(y0)); c.lineTo(X(x0 + u + lean), Y(top + hw * (1 - Math.cos((i / nr - .5) * Math.PI)) * .5)); for (let yy = y0 - .1; yy > top + hw * .3; yy -= Math.max(.06, w * .12)) { const sx = x0 + u + lean * (y0 - yy) / h; c.moveTo(X(sx - .02), Y(yy)); c.lineTo(X(sx + .02), Y(yy - .02)); } }
        c.globalAlpha = alpha * .55; c.strokeStyle = INK; c.lineWidth = lw * .7; c.stroke(); c.restore(); c.globalAlpha = alpha; c.strokeStyle = INK; c.lineWidth = lw; c.stroke(body); };
    if (F.t === 'barrel') { const w = Math.max(.3, Wc), h = H; col(0, 0, w, h, 0); c.beginPath(); for (let i = 0; i < 7; i++) { const a = -Math.PI * (.2 + i * .1); c.moveTo(X(Math.cos(a) * w * .3) + 2, Y(-h + w * .35 + Math.sin(a) * w * .12)); c.arc(X(Math.cos(a) * w * .3), Y(-h + w * .35 + Math.sin(a) * w * .12), Math.max(1, .04 * k), 0, TAU); } c.globalAlpha = alpha * .9; c.fillStyle = '#d9b43a'; c.fill(); }
    else { const w = F.w * Math.min(1, .4 + H / 12), arms = [];
      const nArm = Math.round(F.arms * Math.min(1, H / 8)); for (let i = 0; i < nArm; i++) { const side = i % 2 ? 1 : -1, rank = i >> 1, aw = w * (.72 + R() * .12), outer = Math.ceil(nArm / 2) - 1 - rank, y0 = -H * (.08 + rank * .1 + R() * .05), out = w * .5 + aw * .65 + outer * aw * 1.08, top = -H * (.5 + R() * .3 - outer * .06); /* the outer arms rise lowest, the inner ones tuck in beside the trunk */ arms.push([side, y0, out, top, aw]); }
      for (const [side, y0, out, top, aw] of arms) { const ex = side * out, bend = Math.min(-y0 * .6, aw * 1.1), tube = new Path2D(); tube.moveTo(X(side * w * .2), Y(y0)); tube.quadraticCurveTo(X(ex), Y(y0), X(ex), Y(y0 - bend)); c.lineCap = 'butt'; c.globalAlpha = alpha; c.strokeStyle = INK; c.lineWidth = aw * k + lw * 2; c.stroke(tube); c.strokeStyle = '#7f9268'; c.lineWidth = aw * k; c.stroke(tube); col(ex, y0 - bend * .35, aw, (y0 - bend * .35) - top, 0); }   /* the elbow outlined, the arm's column standing in it */
      col(0, 0, w, H, 0); }
  } else if (F.t === 'cholla') {   // joints on joints, each in a halo of pale spines
    const segs = []; const joint = (x, y, a, d) => { const L = Math.max(.12, H * .14) * (.8 + R() * .4), ex = x + Math.cos(a) * L, ey = y + Math.sin(a) * L; segs.push([x, y, ex, ey, d]); if (d < 6 && -ey < H * .95) { const nk = d < 2 ? 2 : 1 + (R() < .5 ? 1 : 0); for (let i = 0; i < nk; i++) joint(ex, ey, a + (nk === 1 ? (R() - .5) * .6 : (i - .5) * 1.1) + (UP - a) * .25, d + 1); } }; joint(0, 0, UP, 0);
    for (const [x0, y0, x1, y1] of segs) { c.beginPath(); c.moveTo(X(x0), Y(y0)); c.lineTo(X(x1), Y(y1)); c.globalAlpha = alpha * .85; c.strokeStyle = '#6f7a52'; c.lineWidth = Math.max(1, .1 * k); c.stroke(); }
    c.beginPath(); for (const [x0, y0, x1, y1] of segs) for (let i = 0; i < 16; i++) { const t = R(), x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t, a = R() * TAU, l = .07 + R() * .05; c.moveTo(X(x), Y(y)); c.lineTo(X(x + Math.cos(a) * l), Y(y + Math.sin(a) * l)); } c.globalAlpha = alpha * .55; c.strokeStyle = '#c8b27a'; c.lineWidth = lw * .5; c.stroke();
  } else if (F.t === 'whips') {   // ocotillo: long unbranched canes from the base, tiny leaves along them, red flowers at the tips
    c.beginPath(); const tips = []; for (let i = 0; i < F.n; i++) { const u = i / (F.n - 1) - .5, a = UP + u * 1.1 + (R() - .5) * .1, L = H * (.7 + R() * .3), ex = Math.cos(a) * L, ey = Math.sin(a) * L; c.moveTo(X(u * .1), Y(0)); c.quadraticCurveTo(X(ex * .4), Y(ey * .55), X(ex), Y(ey)); tips.push([ex, ey]); }
    c.globalAlpha = alpha * .85; c.strokeStyle = '#4e4636'; c.lineWidth = Math.max(.6, .035 * k); c.stroke();
    c.beginPath(); for (const [ex, ey] of tips) for (let j = 0; j < 5; j++) { const qx = ex * (1 - j * .02), qy = ey + j * .08; c.moveTo(X(qx) + 1.3, Y(qy)); c.arc(X(qx), Y(qy), Math.max(.9, .035 * k), 0, TAU); } c.globalAlpha = alpha * .9; c.fillStyle = '#c4462c'; c.fill();
  } else if (F.stems && !g._sub) {   // a branching aloe: several stems, each ending in its own rosette
    for (let i = 0; i < F.stems; i++) { const u = i / (F.stems - 1) - .5, sh = H * (.35 + R() * .3), sx = u * Wc * .7; c.beginPath(); c.moveTo(X(u * Wc * .1), Y(0)); c.quadraticCurveTo(X(sx * .4), Y(-sh * .6), X(sx), Y(-sh)); c.globalAlpha = alpha * .9; c.strokeStyle = '#6b5a42'; c.lineWidth = Math.max(.8, .06 * k); c.stroke();
      drawForm(c, { ...g, _sub: true, H: H * .32, Wc: Wc * .32 }, X(sx), Y(-sh), k, alpha, flip, (seed || 0) + i * 7); }
  } else {   // rosettes: agaves, yuccas, aloes, dudleyas; tapered fleshy blades from the crown, a flower stalk where the species makes one
    const n = F.n, rad = Wc / 2, leaves = [];
    if (F.trunk) { c.beginPath(); c.rect(X(-.12), Y(-H * .7), .24 * k * flip, H * .7 * k); fillStroke(c, '#8a7a62', alpha * .7, lw); }
    const base = F.trunk ? -H * .7 : 0, Hr = F.trunk ? H * .3 : H;
    for (let i = 0; i < n; i++) { const u = (i + R() * .5) / n, a = -Math.PI * (.02 + .96 * u), tilt = Math.abs(Math.cos(a)), L = Math.hypot(rad * tilt, Hr * (1 - tilt * .5)) * (.75 + R() * .3), w = (F.broad ? .22 : F.narrow ? .05 : .14) * L; leaves.push([a, L, w, Math.abs(Math.sin(a))]); }
    leaves.sort((p, q) => p[3] - q[3]);
    for (const [a, L, w] of leaves) { const dx = Math.cos(a), dy = Math.sin(a) * (F.round ? 1 : .9), rec = F.recurve ? .25 : .08, tx = dx * L, ty = base + dy * L + rec * L * (1 - Math.abs(dy)), nx = -dy, ny = dx;
      c.beginPath(); c.moveTo(X(-nx * w / 2), Y(base - ny * w / 2)); c.quadraticCurveTo(X(dx * L * .5 - nx * w * .45), Y(base + dy * L * .5 - ny * w * .45), X(tx), Y(ty)); c.quadraticCurveTo(X(dx * L * .5 + nx * w * .45), Y(base + dy * L * .5 + ny * w * .45), X(nx * w / 2), Y(base + ny * w / 2)); c.closePath();
      fillStroke(c, F.chalk ? '#c9cfc0' : F.narrow ? '#9aa87e' : '#90a283', alpha * (F.narrow ? .55 : .8), lw * (F.narrow ? .45 : .8));
      if (F.teeth || F.broad) { c.beginPath(); for (let t = .2; t < .95; t += .1) { const qx = dx * L * t + nx * w * .45 * (1 - t), qy = base + dy * L * t + ny * w * .45 * (1 - t); c.moveTo(X(qx), Y(qy)); c.lineTo(X(qx + nx * .02), Y(qy + ny * .02)); } c.globalAlpha = alpha * .6; c.strokeStyle = '#5a3b22'; c.lineWidth = lw * .7; c.stroke(); } }
    if (F.stalk) { const sh = H * (F.stalk === 'white' ? 2.6 : 1.4); c.beginPath(); c.moveTo(X(0), Y(base)); c.lineTo(X(.04 * H), Y(base - sh)); c.globalAlpha = alpha * .9; c.strokeStyle = '#5b5a3c'; c.lineWidth = Math.max(.7, .05 * k); c.stroke();
      c.beginPath(); for (let i = 0; i < 40; i++) { const t = .55 + R() * .45, qx = .04 * H * t + (R() - .5) * H * .25 * (1 - t) * 2, qy = base - sh * t; c.moveTo(X(qx) + 1.6, Y(qy)); c.arc(X(qx), Y(qy), Math.max(1, .035 * k), 0, TAU); } c.globalAlpha = alpha * .85; c.fillStyle = F.stalk === 'white' ? '#f2efe2' : '#d9692c'; c.fill(); c.globalAlpha = alpha * .5; c.strokeStyle = INK; c.lineWidth = lw * .5; c.stroke(); }
  }
  c.restore();
}

/* the plant at an age: data scaled by growth; cached by species, age step and variant */
const CACHE = new Map();
function dims(key, yr) {   // a plant's size at an age, without growing it: the chart holds its scale at full size, so the years show as growth
  const D = ROOT_DATA[key], gR = Math.max(.12, 1 - Math.exp(-3 * Math.max(0, yr) / Math.max(.5, D.yrs))), gH = Math.max(.08, 1 - Math.exp(-3 * Math.max(0, yr) / Math.max(.5, D.yrs * (D.form === 'tree' ? 1.4 : 1)))), H = D.h * gH, Wc = AGRO_LIB[key] ? agroRadiusM(key, yr) * 2 : D.spread * gH, T = D.typ * gR;
  return { H, Wc, T, M: Math.max(T, D.max * gR), Lr: Math.max(D.lat * gR, Wc * .3) };
}
function plantGeo(key, yr, variant) {
  const D = ROOT_DATA[key]; if (!D) return null;
  const q = v => habitFor(key, D) ? Math.round(v * 16) / 16 || 1 / 16 : v;   // grown species change in sixteenths of their growth, so the year slider doesn't regrow them every step
  const gR = q(Math.max(.12, 1 - Math.exp(-3 * Math.max(0, yr) / Math.max(.5, D.yrs)))), gH = q(Math.max(.08, 1 - Math.exp(-3 * Math.max(0, yr) / Math.max(.5, D.yrs * (D.form === 'tree' ? 1.4 : 1))))), k = `${key}|${Math.round(gR * 40)}|${Math.round(gH * 40)}|${variant}|${window.__rootsOld ? 1 : 0}`;
  if (CACHE.has(k)) return CACHE.get(k); if (CACHE.size > 400) CACHE.clear();
  const R = rng(hashStr(key) ^ (variant * 2654435761)), H = D.h * gH, Wc = (AGRO_LIB[key] ? agroRadiusM(key, yr) * 2 : D.spread * gH), T = D.typ * gR, M = Math.max(T, D.max * gR), Lr = Math.max(D.lat * gR, Wc * .3);
  const W0 = D.form === 'palm' ? .011 : D.form === 'cactus' ? .03 : D.form === 'tree' ? Math.max(.03, (.04 + .025 * H)) : D.form === 'shrub' ? Math.max(.015, .012 * H + .01) : D.form === 'succulent' ? .02 : .0035;
  const arch = (D.form === 'tree' || D.form === 'shrub') && D.arch === 'fibrous' ? 'plate' : D.arch;   // a tree's fibrous mat is a shallow plate of fine roots, not a bunchgrass
  if (habitFor(key, D) && !window.__rootsOld) { const g = { key, D, H, Wc, T, M, Lr, sc: scTree(key, R, D, H, Wc, T, M, Lr, W0) }; CACHE.set(k, g); return g; }   // the grown engine, species by species as their habits are set
  const g = { key, D, H, Wc, T, M, Lr, variant, roots: rootSys(arch, R, T, M, Lr, Math.max(Wc * (D.form === 'grass' ? .6 : .25), .05), W0, D.form), top: topSys(key, D.form, R, H, Wc, W0) };
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
let LINE = false; const LINED = new WeakSet();   // the line style: pen and ink, no colour or tone; LINED: the contexts already turned to ink
const lineCtx = c => new Proxy(c, { get: (t, k) => { const v = t[k]; return typeof v === 'function' ? v.bind(t) : v; },
  set: (t, k, v) => { if (k === 'strokeStyle') t[k] = /^rgba\(255/.test(String(v)) || v === '#7f9268' ? PAPER : INK;   /* #7f9268: a cactus arm's body, drawn as a fat stroke inside its ink outline */ else if (k === 'fillStyle') t[k] = v === INK || v === INK2 || v === INK3 ? v : PAPER; else t[k] = v; return true; } });   // every colour drawn becomes ink, every fill paper: masses still hide what is behind them
function drawPlant(c, g, ox, oy, k, alpha, flip, groundClip) {   // groundClip(c): a path below the ground, so roots never poke out of a slope
  if (LINE && !LINED.has(c)) { c = lineCtx(c); LINED.add(c); }
  if (FORM[g.key] && !g.sc) { c.save(); if (groundClip) { groundClip(c); c.clip(); } inkLines(c, g.roots, ox, oy, k, SEPIA, alpha * .92, flip); c.restore(); drawForm(c, g, ox, oy, k, alpha, flip, g.variant); return; }
  if (g.sc) { const hb = g.sc.hb; c.save(); if (groundClip) { groundClip(c); c.clip(); } scWood(c, g.sc.roots, ox, oy, k, flip, SEPIA, '#2a1a10', alpha); if (g.sc.fine) inkLines(c, g.sc.fine, ox, oy, k, SEPIA, alpha * .85, flip); c.restore(); scWood(c, g.sc.crown, ox, oy, k, flip, hb.bark, '#1c1b18', alpha); if (g.sc.twigs) inkLines(c, g.sc.twigs, ox, oy, k, hb.bark, alpha * .8, flip); scLeaves(c, g.sc, ox, oy, k, flip, alpha); return; }
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
window.__rootsGeo = (key, yr) => { bind(); return plantGeo(key, yr, 0); };   // for tests
window.__rootsNear = sec => { bind(); return plantsNear(sec); };

/* in the profile, at true scale: the furthest drawn faintest, as a section shows what lies beyond the cut */
window.__rootsProfile = (c, sec, X, Y, n, gnd, pxm, mini) => { bind(); LINE = S.rootsInk === 'line';
  const P = plantsNear(sec); if (!P.length) return 0; const yr = AGRO ? AGRO.year : 10, gy = t => { const q = t * n, i = Math.min(n - 1, Math.floor(q)), f = q - i; return gnd[i] * (1 - f) + gnd[i + 1] * f; };
  const clip = cc => { cc.beginPath(); cc.moveTo(X(0), Y(gnd[0])); for (let q = 1; q <= n; q++) cc.lineTo(X(q), Y(gnd[q])); cc.lineTo(X(n), 1e5); cc.lineTo(X(0), 1e5); cc.closePath(); };
  let drawn = 0;
  for (const p of P) { const g = plantGeo(p.sp, yr, habitFor(p.sp, ROOT_DATA[p.sp]) ? 0 : p.seed % 4);   // grown species: one plant, mirrored for variety; growing four would cost a second
    if (!g) continue; const hp = Math.max(g.H, g.T) * pxm; if (hp < 3) continue;
    drawPlant(c, g, X(p.t * n), Y(gy(p.t)), pxm, 1 - .55 * Math.min(1, p.d / p.reach), p.seed & 1 ? 1 : -1, clip); drawn++; }
  return drawn;
};

/* the root chart: each species the section crosses once, side by side at one scale, against a depth ruler, named, with how deep it goes */
let lastKey = null;
/* the chart on the slope: the planted stretch of the section at true scale, no vertical exaggeration, every plant where it stands on the real ground, roots down through the hillside */
function slopeChart(c, w, h, sec, mode, yr) {
  const P = plantsNear(sec), uf = isFt() ? 3.28084 : 1, un = isFt() ? 'ft' : 'm', narrow = w < 640;
  if (!P.length) return null;
  const n = 600, prof = sectionProfile(n, sec), L = prof.L, gz = t => { const q = Math.max(0, Math.min(1, t)) * n, i = Math.min(n - 1, Math.floor(q)), f = q - i; return prof.gnd[i] * (1 - f) + prof.gnd[i + 1] * f; };
  const yrM = Math.max(yr, ...P.map(p => ROOT_DATA[p.sp].yrs * 1.5)), items = P.map(p => { const g = plantGeo(p.sp, yr, habitFor(p.sp, ROOT_DATA[p.sp]) ? 0 : p.seed % 4); return g && { p, g: { ...g, m: dims(p.sp, yrM) } }; }).filter(Boolean);
  const cap = Math.max(...items.map(({ g }) => Math.min(g.m.M, Math.max(g.m.T * 2.2, g.m.H * .5))));   // how deep the soil is shown: the deep roots go on, said in words
  const pad = Math.max(...items.map(({ g }) => Math.max(g.m.Wc / 2, Math.min(g.m.Lr, g.m.Wc)))) / L, t0 = Math.max(0, Math.min(...items.map(it => it.p.t)) - pad), t1 = Math.min(1, Math.max(...items.map(it => it.p.t)) + pad), span = (t1 - t0) * L;
  let zTop = -Infinity, zBot = Infinity; for (let q = Math.floor(t0 * n); q <= Math.ceil(t1 * n); q++) { zTop = Math.max(zTop, prof.gnd[q]); zBot = Math.min(zBot, prof.gnd[q]); }
  for (const { p, g } of items) { const z0 = gz(p.t); zTop = Math.max(zTop, z0 + topHm(g)); zBot = Math.min(zBot, z0 - Math.min(g.m.M, cap)); }
  const top = narrow ? 34 : 40, bot = narrow ? 110 : 124, mL = narrow ? 40 : 70, mR = narrow ? 10 : 30, k = Math.min((w - mL - mR) / span, (h - top - bot) / (zTop - zBot)), ox = mL + (w - mL - mR - span * k) / 2;
  const X = t => ox + (t - t0) * L * k, Y = z => top + (zTop - z) * k, gy = t => Y(gz(t)), x0 = X(t0), x1 = X(t1), yBot = Y(zBot);
  const ground = () => { const p = new Path2D(); p.moveTo(x0, gy(t0)); for (let q = Math.ceil(t0 * n); q <= Math.floor(t1 * n); q++) p.lineTo(X(q / n), Y(prof.gnd[q])); p.lineTo(x1, gy(t1)); return p; };
  const soil = () => { const p = ground(); p.lineTo(x1, yBot + 6); p.lineTo(x0, yBot + 6); p.closePath(); return p; };
  c.save(); if (mode !== 'labels') { c.fillStyle = PAPER; c.fillRect(0, 0, w, h); }
  if (mode !== 'labels') {   // the hillside in section: a soft soil tone, a light hatch, the ground line
    c.fillStyle = LINE ? PAPER : '#e7e0d0'; c.fill(soil()); if (mode !== 'plants') { c.save(); c.clip(soil()); c.strokeStyle = INK; c.globalAlpha = .1; c.lineWidth = .6; c.beginPath(); for (let x = x0 - 800; x < x1; x += 9) { c.moveTo(x, top); c.lineTo(x + 800, yBot + 800); } c.stroke(); c.restore(); }
    for (const { p, g } of items.slice().sort((a, b) => b.p.d - a.p.d)) drawPlant(c, g, X(p.t), gy(p.t), k, 1 - .45 * Math.min(1, p.d / p.reach), p.seed & 1 ? 1 : -1, cc => { cc.beginPath(); cc.moveTo(x0 - 400, gy(t0)); for (let q = Math.ceil(t0 * n); q <= Math.floor(t1 * n); q++) cc.lineTo(X(q / n), Y(prof.gnd[q])); cc.lineTo(x1 + 400, gy(t1)); cc.lineTo(x1 + 400, 1e5); cc.lineTo(x0 - 400, 1e5); cc.closePath(); });
    c.strokeStyle = INK; c.lineWidth = 1.6; c.globalAlpha = 1; c.stroke(ground()); }
  if (mode === 'plants') { c.restore(); return { panels: [], species: [...new Set(items.slice().sort((a, b) => a.p.t - b.p.t).map(it => it.p.sp))], slope: true };   /* left to right, as the painter is told */ }
  // the words: title, an elevation ruler at true scale, each run of one species named once below the hillside, with a faint leader up to it
  const drop = (gz(t0) - gz(t1)), pct = Math.round(Math.abs(drop) / span * 100);
  c.fillStyle = INK; c.font = font(12, 600); c.textAlign = 'left'; c.textBaseline = 'top';
  c.fillText(narrow ? `roots on the slope · ${yr === 0 ? 'planting day' : yr + ' yr'}` : `roots on the slope · ${yr === 0 ? 'planting day' : yr + ' year' + (yr === 1 ? '' : 's') + ' after planting'} · true scale, no vertical exaggeration · ${fL(span, 0)} across, ${pct}% slope`, narrow ? 10 : 64, 10);
  let stepU = niceStep(((zTop - zBot) * uf) / 5); while (stepU / uf * k < 18) stepU = niceStep(stepU * 2.2);
  c.font = font(10); c.textAlign = 'right'; c.textBaseline = 'middle'; c.strokeStyle = INK2; c.lineWidth = 1; c.beginPath(); c.moveTo(mL - 6, top - 4); c.lineTo(mL - 6, yBot); c.stroke();
  for (let u = Math.ceil(zBot * uf / stepU) * stepU; u <= zTop * uf + 1e-6; u += stepU) { const y = Y(u / uf); c.beginPath(); c.moveTo(mL - 10, y); c.lineTo(mL - 6, y); c.stroke(); c.fillStyle = INK2; c.fillText(`${+u.toFixed(1)}`, mL - 13, y); }
  c.save(); c.translate(12, (top + yBot) / 2); c.rotate(-Math.PI / 2); c.textAlign = 'center'; c.fillStyle = INK3; c.fillText(`elevation · ${un}`, 0, 0); c.restore();
  // each species numbered in order down the line, the number under every plant of it with a faint leader up to its roots, and a key below: as the root atlases label their plates
  const order = [], num = sp => { let k = order.indexOf(sp); if (k < 0) { order.push(sp); k = order.length - 1; } return k + 1; }, sorted = items.slice().sort((a, b) => a.p.t - b.p.t);
  const marks = []; for (const it of sorted) { const x = X(it.p.t), nn = num(it.p.sp), last = marks[marks.length - 1]; if (last && last.n === nn && x - last.x < 26) { last.x = (last.x * last.c + x) / (last.c + 1); last.c++; continue; } marks.push({ x, n: nn, c: 1, it }); }
  const lastX = [-1e9, -1e9]; c.textAlign = 'center'; c.textBaseline = 'middle';
  for (const mk of marks) { const row = mk.x - lastX[0] > 18 ? 0 : 1; lastX[row] = mk.x; const ly = yBot + 14 + row * 17, g = mk.it.g, tipY = Y(gz(mk.it.p.t) - Math.min(g.M, cap));
    c.strokeStyle = INK3; c.globalAlpha = .5; c.setLineDash([2, 3]); c.lineWidth = .8; c.beginPath(); c.moveTo(mk.x, ly - 8); c.lineTo(X(mk.it.p.t), tipY + 3); c.stroke(); c.setLineDash([]); c.globalAlpha = 1;
    c.beginPath(); c.arc(mk.x, ly, 7.5, 0, Math.PI * 2); c.fillStyle = PAPER; c.fill(); c.strokeStyle = INK; c.lineWidth = .9; c.stroke(); c.fillStyle = INK; c.font = font(9.5, 600); c.fillText(String(mk.n), mk.x, ly + .5); }
  // the key: number, name, how many, how deep; wrapped across the width
  const key = order.map((sp, k) => { const D = ROOT_DATA[sp], its = items.filter(it => it.p.sp === sp), g = its[0].g; return { n: k + 1, t: `${D.common}${its.length > 1 ? ' ×' + its.length : ''}`, d: narrow ? '' : ` · roots ${fL(g.T, 1)}, deepest ${fL(g.M, 1)}` }; });
  let kx = narrow ? 10 : 64, ky = yBot + 54; c.textAlign = 'left'; c.textBaseline = 'middle';
  for (const kk of key) { c.font = font(10.5, 600); const w1 = c.measureText(kk.n + ' ' + kk.t).width; c.font = font(10); const w2 = c.measureText(kk.d).width; if (kx + w1 + w2 + 18 > w - 10) { kx = narrow ? 10 : 64; ky += 15; }
    c.fillStyle = INK; c.font = font(10.5, 600); c.fillText(kk.n + ' ' + kk.t, kx, ky); c.fillStyle = INK3; c.font = font(10); c.fillText(kk.d, kx + w1, ky); kx += w1 + w2 + 18; }
  c.restore(); return { panels: [], species: [...new Set(items.slice().sort((a, b) => a.p.t - b.p.t).map(it => it.p.sp))], slope: true };   /* left to right, as the painter is told */
}
const topH = g => g.H * (FORM[g.key] && FORM[g.key].stalk ? (FORM[g.key].stalk === 'white' ? 2.7 : 1.5) : 1.1), topHm = g => topH({ ...g, H: g.m.H });   // room above for flower stalks; topHm at full size, for the chart's scale
{ const T = window.__topo && window.__topo(); if (T) for (const [k, D] of Object.entries(ROOT_DATA)) if (!T.AGRO_LIB[k] && D.agro) {   // the restoration grasses, cover crops and desert shrubs join agroforestry's library: [name, kind, canopy m, years, L a week, flowers, harvest, bees, note]
  const kind = D.form === 'palm' ? 'tree' : D.form === 'cactus' ? 'succulent' : D.form, y = Math.max(.5, D.yrs);
  T.AGRO_LIB[k] = [D.common, kind, [+(D.spread * .7).toFixed(2), +(D.spread * 1.2).toFixed(2)], [Math.max(1, Math.round(y * .7)), Math.max(1, Math.round(y * 1.3))], D.agro.water, D.agro.flowers, D.agro.harvest, D.agro.bee, D.regen.replace(/\.$/, '').toLowerCase()]; } }

function chartPanel(c, G, px0, pw, h, uf, un, narrow, mode, gyFix) {   // narrow (a phone): names only, slimmer columns, and room at the bottom for the plan / 3d / section switch
  const top = narrow ? 34 : 40, bot = narrow ? 76 : 64, avail = h - top - bot, rw = narrow ? 36 : 46, mL = px0 + rw;
  const above = Math.max(...G.map(topHm)), deepT = Math.max(...G.map(g => g.m.T)); let below = Math.max(...G.map(g => Math.min(g.m.M, Math.max(g.m.T * 2.2, deepT * 1.25, g.D.form === 'tree' ? g.m.H * .5 : 0))));
  const minCol = narrow ? 64 : 118, k0 = avail / (above + below), colW = (g, k) => Math.max(minCol, g.m.Wc * k * .85 + 12);
  let k = k0; const fitW = pw - rw; if (G.length * minCol < fitW && G.reduce((s, g) => s + colW(g, k), 0) > fitW) { let lo = 0, hi = k0; for (let it = 0; it < 30; it++) { const m = (lo + hi) / 2; if (G.reduce((s, g) => s + colW(g, m), 0) > fitW) hi = m; else lo = m; } k = Math.max(lo, k0 * .7); }   // never flatter than about half height: neighbours overlap instead
  if (gyFix) k = Math.min(k, (gyFix - top) / above, (h - bot - gyFix) / below);   // one ground line for the whole chart: each panel's scale fits above and below it
  if (k < k0 || gyFix) below = Math.min(Math.max(...G.map(g => g.m.M)), (gyFix ? h - bot - gyFix : avail - above * k) / k);   // spare height shows deeper soil, not blank paper
  const tot = Math.min(fitW, G.reduce((s, g) => s + colW(g, k), 0)), gy0 = gyFix || top + above * k, bottomY = gy0 + below * k;
  // the ruler: depth below ground, rules across the panel like the six-foot lines of the prairie chart
  LAYOUT.push({ x0: mL, x1: px0 + pw, gy0, bottomY, top });
  const type = mode !== 'plants', ink = mode !== 'labels';
  let stepU = niceStep((below * uf) / 4); while (stepU / uf * k < 16) stepU = niceStep(stepU * 2.2); const stepM = stepU / uf; c.font = font(10); c.textAlign = 'right'; c.textBaseline = 'middle';
  if (type) {
  for (let d = 0; d <= below + 1e-6; d += stepM) { const y = gy0 + d * k; c.strokeStyle = d ? 'rgba(40,40,36,.16)' : INK; c.lineWidth = d ? .8 : 1.4; c.setLineDash(d ? [2, 4] : []); c.beginPath(); c.moveTo(mL - 4, y); c.lineTo(px0 + pw, y); c.stroke(); c.setLineDash([]); c.fillStyle = INK2; c.fillText(d ? `${+(d * uf).toFixed(2)} ${un}` : '0', mL - 8, y); }
  let stepA = niceStep((above * uf) / 3); while (stepA / uf * k < 16) stepA = niceStep(stepA * 2.2); for (let u = stepA; u <= above * uf + 1e-6; u += stepA) { const y = gy0 - u / uf * k; c.fillStyle = INK3; c.fillText(`${+u.toFixed(2)}`, mL - 8, y); c.strokeStyle = INK3; c.lineWidth = .8; c.beginPath(); c.moveTo(mL - 4, y); c.lineTo(mL, y); c.stroke(); }
  c.strokeStyle = INK2; c.lineWidth = 1; c.beginPath(); c.moveTo(mL, top - 4); c.lineTo(mL, bottomY); c.stroke(); }
  else { c.strokeStyle = INK; c.lineWidth = 1.4; c.beginPath(); c.moveTo(mL - 4, gy0); c.lineTo(px0 + pw, gy0); c.stroke(); }   // the painter keeps the ground line
  // the plants, each in its own column; roots may run under a neighbour, as they do in the ground
  let x = mL + 4 + Math.max(0, (fitW - tot) / 2); c.save(); c.beginPath(); c.rect(mL + 1, top - 30, px0 + pw - mL - 1, bottomY - top + 30); c.clip();
  const cols = [], squeeze = Math.min(1, fitW / G.reduce((s, g) => s + colW(g, k), 0)); for (const g of G) { const cw = colW(g, k) * squeeze, cx = x + cw / 2; cols.push([g, cx, cw]); x += cw; }
  LAYOUT[LAYOUT.length - 1].cols = cols.map(([g, cx, cw]) => ({ name: g.D.common, cx, cw }));
  if (ink) for (const [g, cx, cw] of cols) { c.save(); c.beginPath(); c.rect(cx - cw * .8, top - 30, cw * 1.6, bottomY - top + 30); c.clip(); drawPlant(c, g, cx, gy0, k, 1, 1, null); c.restore(); }   // each plant in its column and a little either side, as the plates show them; the section above keeps the true spread
  c.restore();
  if (!type) return; c.textBaseline = 'top'; c.textAlign = 'center';
  for (const [g, cx, cw] of cols) { const D = g.D;
    if (g.M > below + 1e-6) { c.strokeStyle = SEPIA; c.lineWidth = 1; c.beginPath(); c.moveTo(cx, bottomY - 14); c.lineTo(cx, bottomY - 2); c.moveTo(cx - 3, bottomY - 6); c.lineTo(cx, bottomY - 2); c.lineTo(cx + 3, bottomY - 6); c.stroke(); }
    c.fillStyle = INK; c.font = font(11, 600); c.fillText(D.common, cx, bottomY + 6, cw - 6);
    if (narrow) continue;
    c.fillStyle = INK2; c.font = `italic ${font(10)}`; c.fillText(D.latin.replace(/\s*\(.*?\)/g, ''), cx, bottomY + 19, cw - 6);
    c.font = font(10); c.fillStyle = INK3; c.fillText(`most roots to ${fL(g.T, 1)}`, cx, bottomY + 32, cw - 6); c.fillText(`deepest ${fL(g.M, 1)}`, cx, bottomY + 44, cw - 6); }
}
const niceStep = v => { const p = Math.pow(10, Math.floor(Math.log10(v))), f = v / p; return (f < 1.5 ? 1 : f < 3.5 ? 2 : f < 7.5 ? 5 : 10) * p; };
let LAYOUT = [], PLATE = null;   // PLATE: the last painted chart and what it was painted from (line, species, year)
const plateKey = (sec, keys, yr) => JSON.stringify([sec, keys, yr, S.rootsInk || 'color', S.rootsLayout || 'side']);   // a painted plate belongs to its line, plants, year and style
window.__rootsSetPlate = (img, sec, keys) => { bind(); PLATE = { img, key: plateKey(sec, keys, AGRO.year) }; };
window.__rootsPlateState = sec => { bind(); if (!PLATE) return 'none'; const seen = new Set(); for (const p of plantsNear(sec).sort((p, q) => p.t - q.t)) seen.add(p.sp); return PLATE.key === plateKey(sec, [...seen], AGRO.year) ? 'current' : 'stale'; };
window.__rootsChart = (c, w, h, sec, mode) => { bind(); LAYOUT = []; LINE = S.rootsInk === 'line';
  const yr = AGRO ? AGRO.year : 10, uf = isFt() ? 3.28084 : 1, un = isFt() ? 'ft' : 'm', seen = new Map();
  for (const p of plantsNear(sec).sort((p, q) => p.t - q.t)) if (!seen.has(p.sp)) seen.set(p.sp, p);
  { const key = plateKey(sec, [...seen.keys()], yr); if (key !== lastKey) { lastKey = key; if (rootInfo) setTimeout(rootInfo); } }   // the layer's words follow what the line crosses
  c.save(); if (mode !== 'labels') { c.fillStyle = PAPER; c.fillRect(0, 0, w, h); } if (!mode) { c.strokeStyle = 'rgba(40,40,36,.25)'; c.lineWidth = 1; c.beginPath(); c.moveTo(0, .5); c.lineTo(w, .5); c.stroke(); }
  c.fillStyle = INK; c.font = font(12, 600); c.textAlign = 'left'; c.textBaseline = 'top';
  if (mode !== 'plants' && S.rootsLayout !== 'slope') c.fillText(`${w < 640 ? 'roots' : 'roots along the section'} · ${yr === 0 ? 'planting day' : yr + ' year' + (yr === 1 ? '' : 's') + ' after planting'}`, w < 640 ? 10 : 64, 10);
  if (!mode && S.rootsShow === 'painted' && PLATE && PLATE.key === plateKey(sec, [...seen.keys()], yr)) {   // the painted plate, fitted whole into the band on its paper
    const im = PLATE.img, f = Math.min(w / im.width, (h - 4) / im.height), dw = im.width * f, dh = im.height * f; c.fillStyle = '#efe6d2'; c.fillRect(0, 0, w, h); c.drawImage(im, (w - dw) / 2, (h - dh) / 2 + 2, dw, dh); c.restore(); return { panels: [], species: [...seen.keys()], painted: true }; }
  if (!seen.size) { c.fillStyle = INK2; c.font = font(11); c.fillText('no species planted near this section line. plant with shape · agroforestry, then draw the section through them.', 64, 32); c.restore(); return; }
  if (S.rootsLayout === 'slope') { c.restore(); return slopeChart(c, w, h, sec, mode, yr); }   // the planted stretch on the real hillside
  const yrM = Math.max(yr, ...[...seen.keys()].map(k => ROOT_DATA[k].yrs * 1.5)), G = [...seen.values()].map(p => plantGeo(p.sp, yr, 0)).filter(Boolean).map(g => ({ ...g, m: dims(g.key, yrM) }));   // drawn at this age, scaled at full size
  // woody and herbaceous each get their own panel and scale, as the atlases do: a grass beside a 15 m oak would be a speck
  const cat = g => /^(tree|palm)$/.test(g.D.form) || (g.D.form === 'shrub' && g.m.H >= 1.2) ? 0 :   /* small shrubs stand with the low plants, where their scale fits */ /^(cactus|succulent)$/.test(g.D.form) ? 1 : 2, groups = [0, 1, 2].map(i => G.filter(g => cat(g) === i)).filter(a => a.length);   // trees, shrubs and palms · cacti and succulents · grasses and flowers, each at its own scale
  const narrow = w < 640, mL = narrow ? 8 : 64, mR = narrow ? 8 : 24, gap = groups.length > 1 ? (narrow ? 12 : 34) : 0, span = w - mL - mR - gap * (groups.length - 1); let x0 = mL;
  const natural = grp => { const above = Math.max(...grp.map(topHm)), deepT = Math.max(...grp.map(g => g.m.T)), below = Math.max(...grp.map(g => Math.min(g.m.M, Math.max(g.m.T * 2.2, deepT * 1.25)))), k = (h - 104) / (above + below); return (narrow ? 36 : 46) + grp.reduce((s, g) => s + Math.max(narrow ? 64 : 118, g.m.Wc * k * .85 + 12), 0); };
  const nat = groups.map(natural), natSum = nat.reduce((a, b) => a + b, 0), need = groups.map(grp => (narrow ? 36 : 46) + grp.length * (narrow ? 64 : 118)), needSum = need.reduce((a, b) => a + b, 0), extra = span - needSum;   // each panel gets room for its labels first, the rest by how wide its plants want to be
  const frac = grp => { const above = Math.max(...grp.map(topHm)), deepT = Math.max(...grp.map(g => g.m.T)), below = Math.max(...grp.map(g => Math.min(g.m.M, Math.max(g.m.T * 2.2, deepT * 1.25, g.D.form === 'tree' ? g.m.H * .5 : 0)))); return above / (above + below); };
  const top = narrow ? 34 : 40, bot = narrow ? 76 : 64, gyFix = groups.length > 1 ? top + (h - top - bot) * groups.reduce((a, g) => a + frac(g) * g.length, 0) / G.length : 0;
  groups.forEach((grp, gi) => { const share = groups.length > 1 ? (extra > 0 ? (need[gi] + extra * nat[gi] / natSum) / span : need[gi] / needSum) : 1, gw = gi === groups.length - 1 ? w - mR - x0 : span * share;
    chartPanel(c, grp, x0, gw, h, uf, un, narrow, mode, gyFix); x0 += gw + gap; });
  c.restore(); return { panels: LAYOUT.slice(), species: G.map(g => g.key) };
};
/* painting the chart: what the painter is told, and a check that it kept the roots where the data put them */
window.__rootsPaintPrompt = keys => { bind(); const lines = keys.map(k => { const D = ROOT_DATA[k]; return `${D.common} (${D.latin.replace(/\s*\(.*?\)/g, '')})${LOOK[k] || D.habit ? ': ' + (LOOK[k] || D.habit) : ''}`; });
  return (S.rootsInk === 'line' ? 'Turn this diagram into a finished pen-and-ink botanical plate in the manner of the root atlases of Lore Kutschera and Victorian scientific illustration: black ink only, fine linework, stippling and cross-hatching for shade lit from the upper left, fine hair roots drawn line by line, no colour and no grey wash, plain white paper. '
    : 'Turn this diagram into a finished botanical plate in the manner of a hand-coloured 19th-century copperplate engraving and the root atlases of Lore Kutschera: fine ink linework, cross-hatched shading lit from the upper left, sepia roots with fine hair roots, quiet natural colour, plain warm paper. ')
    + (S.rootsLayout === 'slope' ? 'This is a section through a planted hillside: keep the sloping ground line exactly where it is drawn; trunks and stems stand vertical, roots grow down through the soil below the slope; the toned area below the line is the hillside soil in section. ' : '')
    + (S.rootsLayout === 'slope' ? 'The species, in the order they first appear from left to right (several repeat further along the slope, keep each drawn plant as the species drawn there): ' : 'The plants, left to right: ') + lines.join('; ') + '. '
    + (S.rootsLayout === 'slope' ? '' : 'All plants stand on one straight horizontal ground line across the whole plate. ') + 'This is a scientific chart: each plant must stay exactly where it is drawn, in the same left-to-right order, at exactly its drawn height and width; never swap, resize, merge or drop a plant. Keep the composition exactly: every plant where it stands, at the size it is drawn, every limb, root and root tip where it is drawn, with the same height, spread, reach and depth; add nothing beyond what is drawn and leave the empty paper empty. Keep each straight horizontal ground line exactly where it is. Coloured blobs are placeholders for foliage: replace them with the true foliage of that species in the same places. No text, no numbers, no labels, no frame.'; };
window.__rootsDrift = (drawn, painted, panels) => { if (!panels.length) return null;   // the deepest and widest root ink below each ground line, drawn against painted: more than 15% off and the picture says so
  const W = drawn.width, H = drawn.height, a = drawn.getContext('2d').getImageData(0, 0, W, H).data, b = painted.getContext('2d').getImageData(0, 0, W, H).data, out = [];
  const ext = (d, P) => { let deep = 0, lo = W, hi = 0; const bg = [d[((P.gy0 + 4 | 0) * W + (P.x1 - 3 | 0)) * 4], d[((P.gy0 + 4 | 0) * W + (P.x1 - 3 | 0)) * 4 + 1], d[((P.gy0 + 4 | 0) * W + (P.x1 - 3 | 0)) * 4 + 2]];
    for (let y = Math.ceil(P.gy0 + 4); y < Math.min(H, P.bottomY); y += 2) for (let x = Math.ceil(P.x0 + 2); x < Math.min(W, P.x1); x += 2) { const i = (y * W + x) * 4; if (Math.abs(d[i] - bg[0]) + Math.abs(d[i + 1] - bg[1]) + Math.abs(d[i + 2] - bg[2]) > 110) { deep = y; if (x < lo) lo = x; if (x > hi) hi = x; } } return [deep - P.gy0, hi - lo]; };
  const tall = (d, P, col) => { const bx = Math.min(W - 2, P.x1 - 3) | 0, by = Math.max(2, P.top - 20) | 0, i0 = (by * W + bx) * 4, bg = [d[i0], d[i0 + 1], d[i0 + 2]], x0 = Math.max(0, col.cx - col.cw * .3) | 0, x1 = Math.min(W - 1, col.cx + col.cw * .3) | 0;
    for (let y = Math.max(0, P.top - 30) | 0; y < P.gy0 - 3; y++) for (let x = x0; x <= x1; x += 2) { const i = (y * W + x) * 4; if (Math.abs(d[i] - bg[0]) + Math.abs(d[i + 1] - bg[1]) + Math.abs(d[i + 2] - bg[2]) > 120) return P.gy0 - y; } return 0; };
  for (const P of panels) for (const col of P.cols || []) { const h0 = tall(a, P, col), h1 = tall(b, P, col); if (h0 < 12) continue; if (h1 < h0 * .25) out.push(`${col.name} missing or moved`); else if (Math.abs(h1 - h0) / h0 > .2) out.push(`${col.name} painted ${h1 > h0 ? 'taller' : 'shorter'} by ${Math.round(Math.abs(h1 - h0) / h0 * 100)}%`); }
  for (const P of panels) { const [d0, w0] = ext(a, P), [d1, w1] = ext(b, P); if (d0 > 20 && Math.abs(d1 - d0) / d0 > .15) out.push(`roots painted ${d1 > d0 ? 'deeper' : 'shallower'} than drawn by ${Math.round(Math.abs(d1 - d0) / d0 * 100)}%`); if (w0 > 40 && Math.abs(w1 - w0) / w0 > .15) out.push(`roots painted ${w1 > w0 ? 'wider' : 'narrower'} than drawn by ${Math.round(Math.abs(w1 - w0) / w0 * 100)}%`); }
  return out; };

/* the layer's words: what each species near the line does for the land, and where the numbers come from */
window.__rootsInfo = (sec) => { bind(); const seen = new Map(); for (const p of (sec ? plantsNear(sec) : [])) seen.set(p.sp, ROOT_DATA[p.sp]); return [...seen.entries()]; };
})();
