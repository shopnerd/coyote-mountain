# Handoff: Food4Rhino plugins rebuilt in topo (14–15 September 2026)

**Read this first.** Over two days Will asked to scout Food4Rhino for Grasshopper plugins related to topo, then rebuild the useful ones as tools in `topo.html`. This session added twelve tools across eight rounds. They are live at coyotemountainfarm.com (repo `shopnerd/coyote-mountain`). For how tools are built (the panel-tool pattern, `S.rec` records, hover tips, hooks), read `HANDOFF-2026-09-14-field-tools.md` first. Sections G–K there cover the first five rounds in detail. Section L below is the last round.

No plugin code was copied. Methods were rebuilt from each plugin's docs, examples and published equations, since several plugins are GPL.

## The scouting

- Sweep one: [Topo Plugin Scout](https://claude.ai/code/artifact/e38c3647-2697-438b-9bb4-366d61b073ac)
- Sweep two: https://claude.ai/artifact/V6iZLHkb9Ny1QT45moDpZH
- Food4Rhino blocks WebFetch with a 403. Scrape it with curl or urllib using a browser user agent, with pages at `?page=0%2CN`.

## Everything built, in order

| round | commit | plugin | tool (task · name, `id`) | details | test |
| --- | --- | --- | --- | --- | --- |
| 1 | `996e23c` | Groundhog | Study · stream crossing, `xing` | G | e2e234 |
| 1 | `996e23c` | Docofossor | Study · what you can see `view`; Shape · best route `route`; Shape · ditch and berm `ditch` | G | e2e234 |
| 2 | `bd8dd68` | Manta-Ray | Study · wind, `wind` | H | e2e235 |
| 2 | `bd8dd68` | FlahaETo | Study · irrigation, `irrig` (FAO-56) | H | e2e235 (+ fao56.js) |
| 3 | `443f68a` | Cockroach | Site · point cloud, `cloud` | I | e2e236, e2e237 |
| 4 | `099cfeb` | SpaceVisual | inside `view`: isovists, horizon, VGA, sky view, route out of sight | J | e2e238 |
| 5 | `b085a06` | Ladybug + Gismo | Study · sunlight, `solar` | K | e2e239 |
| 5 | `b085a06` | AeroField | wind around trees and buildings (inside `wind`) | K | e2e240 |
| 6 | this commit | PV layout tools, e.g. the PVWatts method | Shape · solar array, `pvarray` | L | e2e241 |
| 6 | this commit | kriging/IDW tools | Study · field maps, `fmap` | L | e2e241 |
| 6 | this commit | LandArchGrade-style grading | Shape · spot grading, `spots` | L | e2e241 |

All test scripts are in session scratchpad `C:/Users/zolar/AppData/Local/Temp/claude/C--Users-zolar-WebDev/7d4521fc-d03a-4274-b332-fc532b15a7b4/scratchpad`. Scratchpads are temporary: copy them somewhere safe if they need to outlive the machine's temp cleanup.

## L. Solar array, field maps, spot grading (15 September)

### Shape · solar array (`pvarray`, `rec.arrays`)
- **Drawing and settings.**
  - Draw an area by taps, then lay out the rows.
  - Module choices: 400 W (1.722 × 1.134 m), 550 W or 300 W.
  - Portrait or landscape, panels deep per table, and tilt (defaults to latitude, clamped 5–40°).
  - Facing, setback, and losses of 14% (PVWatts), heat 5% and inverter 96%.
  - Price per watt and grid cost per kWh are flagged as examples until Will enters real numbers.
- **Row spacing (`pvPitch`).**
  - Uses the lowest sun between 9 and 3 solar time on the winter solstice (21 December; 21 June in the southern hemisphere).
  - Accounts for how steeply the ground rises toward the back rows: `d = (H − s·D) / (tan alt / cos Δaz + s)`, and the pitch is D + d.
- **Layout (`pvLayout`).** Rows step back through the polygon. Each row's usable length is where both its front and back edges lie inside the area, less the setback. Modules sit 2 cm apart.
- **Energy (`pvYield`).**
  - Plane-of-array monthly kWh/m² from `slPanel` (the sunlight tool's sky and horizon), × kWp × (1 − losses)(1 − heat) × inverter.
  - Shows a monthly chart against daily use, then cost and payback.
- **Verified:**
  - At the computed pitch the winter ray just clears the next row (0.00 cm), and at 97% of the pitch it is blocked by 9.8 cm.
  - A test rectangle gives 6 rows, 600 panels and 240 kWp, matching a hand count.
  - Rising ground shortens the pitch (5.483 m vs 6.583 m on the flat).
  - The yield equals the PVWatts arithmetic exactly.
- **Hooks:** `__pvLayout(k)`, `__pvYield(k)`, `__pvNew(pts)`.
- **Limits:**
  - It does not model shade from trees or buildings, only the ground.
  - Payback uses example prices until Will enters his own.
  - Tables are simple fixed-tilt rows (no trackers or string design).

### Study · field maps (`fmap`, `rec.fmap` {src, method, power, thin, sets})
- **Data sources.** Any field-note kind with ≥ 3 numeric values, or an imported csv of latitude, longitude and value (`fmImport`).
- **Methods.**
  - Inverse distance with a chosen power.
  - Ordinary kriging with a spherical variogram (12 bins, weighted least squares over 40 trial ranges).
  - "Best by test", which picks whichever misses less when each point is left out. Kriging's leave-one-out uses Dubrule's shortcut.
- **Kriging uncertainty.** The standard error is computed on a coarse grid and interpolated. Ground is hatched where the error > 0.8 × √sill. A tap reads the value ± the error.
- **Verified:**
  - Kriging passes through every sample (1.8e-6).
  - Weights sum to 1.
  - The Dubrule shortcut equals a brute-force refit (1.646243 both ways).
  - Error is 0.775 at a sample vs 3.489 far away.
  - The csv import works.
- **Hooks:** `__fmCompute`, `__fmImport`, `__fmWeights`.
- **Limits:**
  - About 150 points is the comfortable ceiling, because it uses a dense matrix inverse.
  - Coordinates are treated as flat (fine at site scale).
  - It fits one spherical variogram only, with no trend or anisotropy.

### Shape · spot grading (`spots`, `rec.grading` {spots, lines, bound})
- **Inputs.** A boundary (taps), spot heights (tap, type, nudge or drag) and breaklines with per-point heights.
- **Surface (`sgCompute`).**
  - Breaklines are densified every 0.75 cell, and the boundary every cell at ground height.
  - A Bowyer-Watson Delaunay TIN (`sgDelaunay`) is rasterised inside the boundary. Outside, the ground is untouched.
- **Outputs.**
  - Cut and fill, the graded area and the steepest slope.
  - Slope classes: under 1%, 1–5%, 5% to 1 in 3, and steeper than 1 in 3.
  - A slope wash and flow arrows.
- **Apply to the ground.** Uses `snapshot()`, so it can be undone. Contours, water, cut and fill, and field build then see it.
- **Verified:**
  - The Delaunay TIN has 109 triangles (= 2n − 2 − h) and no empty-circle violations.
  - A tilted plane is reproduced within 0.01 mm.
  - A raised spot is exactly +1.0000 m at the spot (202.6 m³ fill), with the edge within 3 cm.
  - Breakline ridge heights are exact, and halfway along within 0.9 cm.
  - Apply and undo work.
  - Drag works.
- **Hooks:** `__sgDelaunay`, `__sgCompute`.
- **Limits:**
  - The TIN is linear, so the surface has creases at triangle edges.
  - It does not check for surfaces that fold, or for walls needed where the design meets the ground steeply.
  - Nothing enforces a minimum drainage slope; read the blue class.

### This round's checks
- e2e241: 25 checks, all pass (screenshots `out241/241-pv.png`, `241-fmap.png`, `241-grade.png` looked right).
- Regression: see the commit message.
- tipaudit and the reference manual (`book/reference.md`) were rerun.
- Voice `system.md` updated (coyote-voice `5c83784`).
- Name clash caught: `const PV` is already the plan-view zoom, so the array state is `PVA`.

## Numbers that are estimates, not verified
- Solar: array price, grid tariff, heat and losses are typical values. ERA5 sunlight is a ~10 km average.
- Irrigation: WUCOLS factors and efficiencies.
- Stream crossing: Manning's n, bed speeds and storm intensity until entered.
- Wind: bare-ground and plan-flow pictures, not CFD; speed-ups beside buildings read high.
- Point cloud: trees from the 2019 photogrammetry cloud merge along the arroyo.
- Field maps: every map value between points is an estimate; only the points are measured.

## How to run the tests
1. Start `python -m http.server 8765` in `coyote-studio`.
2. Run `node e2eNNN.js <playwright-core> http://localhost:8765 <outdir>`, where playwright-core is `C:/Users/zolar/AppData/Roaming/npm/node_modules/@playwright/cli/node_modules/playwright-core`.
3. Older suites:
   - e2e203–e2e229 and `tipaudit.js` are in scratchpad `ff66cb8b…`. e2e220 must use its own scratchpad as the out dir.
   - e2e230–e2e233 are in `fb8fbb82…`.
   - e2e174, e2e187 and e2e192 are obsolete (classic layout).
4. Parse check: extract the `<script>` blocks to one file and run `node --check`.
5. Reference manual: `node book/tools/make-reference.js <playwright-core>`.

## How a new tool gets added (the checklist this session followed)
1. Write the block (state + compute + draw + panel + `window.__` hooks) and insert it before `/* shape · steps`.
2. Grep for name clashes (`const PV`, `WF`, …) before inserting.
3. Add the tool's key to the `drawPlan` cache key and its draw call in `drawPlanBase`.
4. Add a TASKS entry and a U2TIP hover line, with `data-tip` on every control.
5. Write a Playwright test that checks against closed forms or brute force, not only "it renders". Look at the screenshots.
6. Run the regression suites, tipaudit, the reference manual and the voice copy.
7. Commit, push, grep the live page for the new hook.

## Open
- **Waiting on Will:**
  - A real installer quote and tariff for the solar array.
  - Real soil or moisture readings for field maps.
  - A first spot-grading design on the Encino pad to try apply-to-ground on real ground.
- **No dependency:**
  - Shade from trees and buildings (the sunlight tool is bare ground, so the array is too).
  - Exporting graded surfaces to LandXML via field build.
  - Supabase sharing of records (carried over).
  - Remaining candidates from sweep two.
