# Handoff · 19 September 2026 · bilingual topo + flight, click corners, dark mode

Everything below is **committed, pushed and live** on coyotemountainfarm.com (last commit `6257ead`). Nothing is left uncommitted.

## What shipped today

| change | where | commit |
|---|---|---|
| **español / english button** in topo's top bar: every label, tooltip, message, tour and learn card (2,433 phrases, Mexican Spanish) | `lang.js` (new) + 3 lines in `topo.html` | `bb6e1af` |
| the floating **hover hints** in Spanish too (TIPS, data-tip, label hints; 2,023 hover targets checked) | `lang.js`, `labelTip` in topo | `543f4a8` |
| Spanish **task tabs** sized like the English (fit as a share of the tab, so the rail's zoom cancels; refit on every task change) | `lang.js` `fitTabs` | `3e85bb7` |
| plan **scale bar** sized to the ground on screen, never crosses the caption when zoomed in | `topo.html` plan chrome | `9e3d1c1` |
| **flight planner** in Spanish: same button, same dictionary; "plan" stays *plan* there; logos keep their names; the phone caption no longer runs over the scale bar | `flight.html`, `lang.js` | `3996b56` |
| **click corners** in the area map: click the corners, the site turns to fit them (rotation slider now 1° steps) | `topo.html` `ptFit`, `fetchArea(lat, lon, w, rot)` | `7c1d01e` |
| **dark mode**: chosen tool / task / map mode in bright orange `#e0763f` with dark text (5.8:1) | topo + flight CSS | `6257ead` |

## How the language switch works (read before touching UI text)

- `lang.js` is loaded at the end of `topo.html` and `flight.html`. The pages stay written in English. When Spanish is on, a MutationObserver swaps text nodes and `title` / `placeholder` / `aria-label` values for their entry in `ES`, and swaps them back for English.
- Keys are the English with every number as `#`. `"# ft wide"` covers "40 ft wide". Values keep the same `#`s in the same order.
- **Adding UI text? Add its Spanish to `ES` in lang.js.** With Spanish on, `window.__langMissing` lists whatever isn't covered.
- **Code that reads a button's words** must read the English: `(el.dataset.en || el.textContent)` or `coyoteLang.en(el[, attr])`. There are two such places in topo, plus `labelTip`.
- **Per-page meanings** go in the override near the top of lang.js (flight: `Plan` → `Plan`).
- `translate="no"` on an element keeps it English (used for the button itself and the logos).
- **Stays English:** text drawn on the canvas (map captions, the 3d inset, the flight profile strip), exported files, drone model names.
- The choice is remembered in localStorage `coyote-lang`. `?lang=es` / `?lang=en` in a link overrides it. A browser set to Spanish opens in Spanish.
- The translation was machine-made with a glossary. **Have a Spanish speaker read the tour before leaning on it with the crew.**

## Tests (playwright, in this session's scratchpad)

Scratchpad: `C:\Users\zolar\AppData\Local\Temp\claude\C--Users-zolar-WebDev\2017eabf-809a-41db-a7dc-c4831204b5e8\scratchpad`

Run with `node <test>.js "<playwright-core>" http://localhost:8771 <outdir>`. The playwright-core path is in the 9/15 handoff. Serve the folder with `python -m http.server 8771`. Each test prints `FAILS 0`.

- `e2e_lang.js`: topo switch, coverage, tour, back to English word for word, phones
- `e2e_tips.js`: every hover hint in Spanish
- `e2e_flight.js`: the same for the flight planner, plus caption/scale bar and logo
- `e2e_corners.js`: click corners (30° rectangle → site turned 30°), backspace, box still north-up, Spanish bar
- `e2e_scalebar.js`, `dark2.js` (contrast)

Dictionary build: translations live in `tr/out*.json` + `extra.json`, the engine in `lang.head.js`. `node build.js` writes `coyote-studio/lang.js`. For a small change, **just edit lang.js directly**. The scratchpad is temporary.

## NEXT: Will's idea — Google-Earth-style shapes (not started)

Draw lines and areas with **endpoints (vertices) you can grab and move later**, like Google Earth's path and polygon tools:

- **Draw:** click to drop points; double-click or click the first point to close an area. An open line is a path.
- **Edit later:** select a shape, drag any vertex, click an edge to insert a vertex, remove one with a right-click or Delete. Move the whole shape.
- **Measure live:** length for lines, and area plus perimeter for closed shapes, in the site's units (ft/ac or m/ha).
- **Label and attributes:** a name plus free fields (e.g. use, owner, crop, note). Shown as a label on the plan.
- **Saved list:** a panel listing every shape with its measurement. Show or hide, rename, delete, zoom to. Stored with the project, and exported as KML / GeoJSON so they open in Google Earth. There's already a KML lot-boundary import to reuse.
- **Where it fits:** probably a new tool in **Shape** (or **Site**), e.g. "shapes & measures".
- **What to read first:**
  - `selectPanel` (topo.html ~8100): the select tool already picks and drags drawings.
  - `S.strokes`: the drawing store.
  - `remapDrawing`: keeps drawings pinned to the ground when width or rotation changes.
  - The KML lot boundary (`#kmlBtn`, `S.boundary`).

  Store the vertices in lat/lon or in ground metres, so they survive refetch and rotation.
- **Spanish:** add its strings to `ES` in lang.js as you go.

## Other open threads

- **Flight planner has no site rotation.** Click corners is topo-only.
- **Canvas text is English** (captions, 3d inset labels, flight profile). Translating it would mean passing the strings through `ES` inside the draw code.
- **Toggles like "follow terrain" / "detail 1×"** keep their dark-orange look in dark mode. Will may want them bright orange too; that's a small CSS change.
- **The home page (`index.html`)** isn't translated.
