# Coyote Mountain Studio · handoff, 13–14 September 2026 (the field tools and the field book)

Written at Will's request on 14 September. **Read this first.** It continues from `HANDOFF-2026-09-13-tasks.md` (items 1–35, plus the notes appended at its end). Memory: `project_coyote_studio.md`, `project_topo_reorg.md`, `project_coyote_voice.md`.

In one paragraph: the task layout became the only layout (classic removed), Astra's five review items were built, and then all sixteen tools on the build-next list, from Ground Change to Field Build, plus a phone-as-level mode. Three real bugs turned up along the way and were fixed. Every control now has a hover description. A field book was written: a manifesto, 17 field cards, a generated reference manual and a 15-week syllabus. The licence stays PolyForm Noncommercial, described as "free for learning and the commons".

## Where things live

| what | where |
| --- | --- |
| site repo | `C:\Users\zolar\WebDev\coyote-studio` = GitHub `shopnerd/coyote-mountain`, live at https://coyotemountainfarm.com (Pages, 40–55 s after a push) |
| topo tool | `topo.html`, about 5,900 lines, single file, no libraries |
| flight planner | `flight.html`, about 1,130 lines |
| field book | `book/`: `manifesto.md`, `syllabus.md`, `reference.md` (generated), `field/01…17-*.md` + `field/README.md`, `tools/make-reference.js` |
| voice copy | `C:\Users\zolar\WebDev\coyote-voice` (local git only), helper on `localhost:8790`, started by `start-voice.ps1`, key in the `ANTHROPIC_API_KEY` user env var |
| session scratchpad | `C:\Users\zolar\AppData\Local\Temp\claude\C--Users-zolar-WebDev\ff66cb8b-dc17-4dd7-8321-ea283d60ec4e\scratchpad` (tests `e2e210`–`e2e229`, updated copies of `e2e203`, `e2e205`, `flightui/test2.js`, audits `tipaudit.js`, `flighttips.js`, `srctips.js`, the patch scripts `*.py`) |
| older tests | `…\10bf6f57-35b1-40b3-91be-0b431b7aab49\scratchpad` (`e2e204`, `e2e207`, originals) |
| playwright-core | `C:\Users\zolar\AppData\Roaming\npm\node_modules\@playwright\cli\node_modules\playwright-core` |

Artifacts:
- [Coyote Build-Next List](https://claude.ai/code/artifact/48aad303-22e6-403b-94ee-26c3d3adb835): all sixteen ideas, each marked built with where it lives.
- [Coyote Mountain Field Book](https://claude.ai/code/artifact/c02842ef-e89d-40d3-9460-f52652c9d45b): manifesto, syllabus, cards and reference in one page (a preview; the source of truth is `book/`).
- Stale, not updated this session: the Topo Control Map (`1bdc1965…`), the private gallery (`acbd3cd4…`), the old topo artifact copy (`062c2198…`).

## What was built, in order

### A. The layout (13 Sept)

1. **Will's design-mode notes applied as rules** (`4442991`): tasks spaced down the left; tool buttons one per row at one width. Design mode's per-button paddings used `nth-child`, which would have hit the wrong buttons on other tasks, so they became CSS rules.
2. **Task layout made the default** (`ee68506`), then **classic removed** (`9f6b41d`): no `?classic`, no classic link, no classic tour in learn. `#tour` (the teachers page link) opens learn. The old rail HTML stays in the page, hidden, because the task layout borrows its rows. Old `?new` links still work.
3. **Task names** (`aec09d4` → `c575a7d` → `5bc8cc9`): stacked upright capitals, 20 px, in a 32 px column; the tabs are CSS grid rows sized by JS to the tallest tab (`minmax(<tallest>px,1fr)`), so AIRCRAFT never clips. localStorage `u2tasksW2`.
4. **Narrow column** (`6670310`, flight in `9f6b41d`): the rail lays out at **220** wide (was 300), with every tool and settings button full width. localStorage `rail3`; an old `rail2` converts so text keeps its size. Paired buttons wrap instead of squeezing (`.u2panel .seg{flex-wrap:wrap}`). In lot and survey, **clear** sits alone at the bottom.
5. **Hover descriptions for the layout's own buttons** (`5bc8cc9`): `U2TIP` (tasks and tools) and `U2BARTIP` (top bar, views).

### B. Astra's review, five items (`6e0cadd`)

1. **Plan tools keep their settings in 3D and section.** 3D sculpts, so `setMode` switches the brush and `setBrush` hides pad/grade/path rows; `remount()` shows them again for a `view:'plan'` tool away from plan, skips `#brushParams`, and shows a **draw it in plan** button (`t.planLabel` overrides the text).
2. **One model size:** `#mm` mounted in 3d print, laser-cut model and cnc and maps (the same element moves; laser and cnc already read `S.mm`).
3. **Exact numbers:** click any slider's value to type. `bind()` stores `el._fmt`; `exactSet()` searches slider positions for the shown number nearest the typed one (whichever number in the label moves, so a scale or a width both work).
4. **Group labels:** a `'=name'` entry in a tool's `rows` draws a small label (pad: footprint, level and grade, edges, earthwork); `group:` on a tool labels the tool list (make: pictures and sheets, physical models, in the field, files). `unit('=…')` returns null.
5. **Your-turn steps in learn:** a step with `start`/`wait` disables next until `wait(start)` is true (polled), with `window.__tourNow` as the test hook.

Also: **play all** in learn on topo and flight (`a2ef2f3`), and flight's site tool gets **pick an area on a map** (copied from topo, 100 m–6 km).

### C. The sixteen tools (13–14 Sept)

Every one is a **panel tool**: a `panel: box => …` entry in `TASKS`, its state in `S.rec` (saved in the project file as `records`), a `window.__<x>Draw(ctx)` layer called from `drawPlan` with its key in the plan cache key, a capture-phase `pointerdown` listener on `cv` only while it is placing something, and its own test.

| tool | task | commit | test | stored |
| --- | --- | --- | --- | --- |
| ground change | study | `f2d0765` | e2e212 | not saved (surveys reloaded each visit) |
| earthwork budget | shape | `eff7e4c` | e2e213 | localStorage `coyote-budget` |
| nature records | site | `9043756` | e2e214 | `rec.nature` (imports only) |
| water budget | study | `bcb953e` | e2e215 | `rec.water` (A/B), localStorage `coyote-water` |
| fire ready | study | `6e710f7` | e2e216 | `rec.fireBld`, localStorage `coyote-fire` |
| agroforestry | shape | `cc9b56c` | e2e217 | trees carry `sp`; `rec.agroYear` |
| walk the line | make | `0190505` | e2e218 | `rec.flags` |
| phone as a level | make · walk the line | `52975de` | e2e229 | — |
| landscape story | make | `4695548` | e2e219 | `rec.story` |
| field notes | site | `635c397` | e2e220 | `rec.obs`, `rec.series` |
| grazing | shape | `328daa2` | e2e221 | `rec.graze` |
| species surveys | site | `f42a137` | e2e223 | `rec.bio` |
| recovery | study | `11a8419` | e2e224 | `rec.recovery` |
| carbon | study | `c96cc6d` | e2e225 | `rec.carbon` |
| landscape fit | study | `eb2f1ae` | e2e226 | `rec.fit` |
| visitor walks | shape | `f171839` | e2e227 | `rec.visit` |
| field build | make | `9c8bb4f` | e2e228 | — |

What each does, briefly:
- **Ground change:** before and after GeoTIFFs sampled per cell; heights lined up by the median difference; a noise floor (`chgLod`); ember lost, blue built up, volumes. With only an after survey it compares with `base` (marked rough); from field build it compares with the design `z` (`CHG.design`). Test: a pit and mound come out within 2% and 4%.
- **Earthwork budget:** quantities from `S.earth` and `S.strokes` × rates kept in metric; low/base/high by how firm the prices are; trucks, diesel and CO₂; example rates flagged until edited; csv.
- **Nature records:** iNaturalist `v1/observations` by bounding box (CORS open, no key, up to 5 pages with a 1.1 s pause), groups, species list, hover tip, blurred locations as rings; eBird or BirdNET csv import (confidence ≥ 0.5, no-location rows placed at the centre).
- **Water budget:** one storm split by `floodSim` pools, the dam pond (`damPool`), swales (contour length × cross-section) and roof tanks; a year; dry-season demand; A/B compare.
- **Fire ready:** a risk per cell from slope (×2 per 10°), sun-facing sides, wind blowing upslope and cover, lowered by gravel, paving and graded ground (rasterised design) and raised by planting; 30 ft and 100 ft rings stretched downhill around mapped buildings, objects and tapped buildings. Labelled a planning aid.
- **Agroforestry:** `AGRO_LIB` (20 species: canopy and years ranges, water, bloom and harvest months, bee forage, a note); plant one or a row; the year slider recomputes `st.r` for library trees, so 3D, fire, budget and carbon all follow; crowding crosses; calendar with bee gaps.
- **Walk the line:** lines from the keyline and swales (`keylineFor`, `contourPolys` + `clipToLabel`), paths, drawn lines and the lot; `watchPosition` plus a wake lock; distance, side, to the end, and for level lines the ground above or below the level (from the model, not the phone's height); flags; GPX. **Phone level:** `deviceorientation` beta; two-way zero; target grade; LEVEL and a beep.
- **Landscape story:** chapters on the canvas with a caption band, recorded through a composite canvas and `MediaRecorder`; the page's state is put back afterwards; `window.__storySpeed` for tests.
- **Field notes:** kinds, method and accuracy, a photo shrunk to 640 px JPEG, placed where I stand or by tap; sensor csv attached to a note and charted with rain bars; csv out. A soil organic carbon kind was added for carbon.
- **Grazing:** paddocks by tapping corners (stored lat/lon), herd intake, forage, grazing days, move in or out, rest status, left ungrazed, water points, next moves.
- **Species surveys:** spots and routes, visits with minutes and counts, a list seeded from nature records, per-hour and season tables, a private species list kept out of the csv.
- **Recovery:** treated and untreated areas, goals from a baseline to a target, measurements (by hand or from field notes inside), treatments, next check and overdue, comparison, repeat photos.
- **Carbon:** rough mature kg C per species (`CARBON_KG`) grown with each canopy as a 30-year band; soil carbon % → t/ha by depth and density; csv marks estimate or measured.
- **Landscape fit:** five things to place (footprint, hard max slope, preferred slope, weights); hard limits (steep, stream channel, protected: drawn, geojson or kml import, recovery areas, ungrazed paddocks); weighted score (sun, low or high ground, water, road, fire); the three best spots of the footprint's size, apart; fit wash with ruled-out ground hatched.
- **Visitor walks:** walks and stops; length, climb, steepest grade, share ≤ 5%, Tobler walking time; conflicts with protected ground, recovery, surveys, streams, slopes over 1 in 5; closed months with an alternative; group and weekly limits; visit log; fees beside the cost of care.
- **Field build:** grade stakes on a grid over disturbed ground (C or F), edge marks, path and wall points; csv (with UTM) and gpx; LandXML TIN design and existing surfaces (WGS 84 / UTM, EPSG 326xx/327xx); keep-out kml; the as-built check. `utm()` matches pyproj to a centimetre (test).

### D. Fixes found along the way

1. **Tools that only read the plan could dig** (`328daa2`): a tool with no `pick` left the last brush active, so a click on the plan raised or lowered the ground and added an undo step. `chooseTool` now sets `setBrush('look')` for tools without `pick` or `sculpt3d`; in plan, a `look` drag pans. Test e2e222 covers nine tools.
2. **GeoTIFF reader half a pixel off** (`9c8bb4f` topo, `54c42ec` flight): pixel-is-area values belong to the middle of each pixel; `sample()` treated them as corners. Now `c -= .5; r -= .5` when `GTRasterTypeGeoKey` is area. Found when an as-built survey identical to the design showed millions of yd³ of change.
3. **Path surfaces** (`2497e5e`): the old gravel and paving fill used a lattice over a self-crossing corridor polygon, with density capped by the bounding box: holes on bends, stones spilling out, near-empty long diagonals. `pathSurface()` now lays rows and courses along the resampled centreline; under 7 px wide it draws a dotted or tinted strip. Area paving jitter halved. Plant row 3 + 2.
4. **Phone level wait** (`52975de`): headless Chromium has `DeviceOrientationEvent.requestPermission`, which never answers; it now races a 3 s timeout.
5. **Undo and project whitelists** carry `sp` for trees (both lists in `snapshot` and `snapshotProject`).
6. **Hover descriptions everywhere** (`859a3fb`, box descriptions in `e2e5093`): `LABEL_TIPS` (a regex on a control's label or aria-label) is the fallback in `tipFor`; hover now includes selects and the logo. Flight's `tipsIn()` sets `data-tip` on its moved rows and menus. The audits find none missing.

### E. Voice copy

`system.md` was rewritten for the task layout (`dcdbad6`), stripped of classic (`74a85f1`), and given ground change, the budget and the fourteen new tools (`c3cbf7a`, `4628e4d`, `479b338`). `tools.json` press block hint updated. The helper was restarted after each change; `system.md` is only read at start.

### F. The field book (`293e16f`, `f52bd92`, `e2e5093`)

- **Licence:** kept PolyForm Noncommercial 1.0.0. The README and LICENSE now say "Free for learning and the commons", worded to match the licence: teaching, study, research and personal projects, and schools, charities, environmental groups, research organisations and public bodies; business use needs a licence. (An earlier draft said "personal land and community projects"; that overstated it, because a farm using it for its business counts as commercial.)
- **Manifesto** (`book/manifesto.md`): observe first; the smallest intervention that does the most lasting good; build it right; measure what happened; say what is estimated; the people on the land hold the data (says exactly when the tool reaches out); teach.
- **17 field cards** (`book/field/`): 01 stake a swale · 02 flag a line · 03 field notes and photo points · 04 soil infiltration test (USDA single ring) · 05 soil carbon sample · 06 rain gauge and readings · 07 after-rain walk · 08 species survey visit · 09 plant a row · 10 move the herd · 11 recovery check (line-point intercept) · 12 fly a drone survey (use the DTM, not the DSM) · 13 compare two surveys · 14 stake the grading for a machine · 15 check what was built · 16 defensible space walk (California zones, ask the local fire service) · 17 visitor walk check. No time estimates: none are real yet.
- **Reference manual** (`book/reference.md`, about 740 lines): generated by `node book/tools/make-reference.js <playwright-core>` against the local server. It visits every tool in plan and 3D and writes each control with its hover description, plus top bar, views, camera, layers, status, learn, keys and the flight planner. **Rerun it after changing the tool.**
- **Syllabus** (`book/syllabus.md`): "Reading and shaping land", 15 weeks (theme, learn chapter or tool, field card, deliverable), a final project, assessment weights and criteria, safety and ethics, a 5-day intensive, further reading (McHarg, Yeomans, Mollison, Lancaster, SER 2019, the NRCS test kit guide).
- Nothing in `book/` is linked from the site yet.

## Numbers that are estimates, not verified

Carbon per species; agroforestry canopy, years and water ranges; herd forage intake; fire factors; example budget rates; the diesel figure (0.45 L/km, 2.68 kg CO₂/L). Each panel labels them. Verified: Ground Change volumes (2–4% on a synthetic pit and mound), UTM (to a centimetre against pyproj), the infiltration arithmetic in card 04.

## How to run the tests

1. `cd coyote-studio && python -m http.server 8765`
2. `node <test>.js <playwright-core> http://localhost:8765 <out dir>` from the scratchpad.
3. Full set, all passing on 14 Sept: e2e203, e2e205, e2e210–e2e229 (e2e210 needs a run on its own; in a long batch it can time out). Flight: `flightui/test2.js` (34 checks; the one known fail counts the map picker's buttons as unmapped rail controls).
4. Audits: `tipaudit.js` (topo, every task, tool and view) and `flighttips.js`; `srctips.js` checks source labels against `LABEL_TIPS`.

Page hooks for tests: `window.__ui2` (`state, chooseTask, chooseTool, TASKS, catalogue, applyView`), `__ui2probe(gx, gy)` (grid → canvas px), `__dbg(fn)` (S, W, H, cs, z, geoTiff, snapshotProject, updateStats, nodeLatLon…), `__tourNow`, `__tipFor`, `__utm`, `__fitCand`, `__levelEvent`, `__levelState`, `__storySpeed`. Engine functions like `agroTrees` or `parseGeoTiff` are **not** reachable from `page.evaluate`; go through `__dbg` or add a hook.

## Gotchas learned this session

- **`//` inside a one-line chain comments out the rest of the line.** It removed `tourGo`'s closing brace this time. Use `/* */` for any comment that is not at a line's end.
- **Bash heredocs with quotes, apostrophes or backticks break the Bash tool.** Write patch scripts and tests to files with the Write tool, then run them.
- **Patch scripts assert each anchor appears exactly once.** Duplicates to watch: `MONTHS` already exists; the stroke field list appears twice (`snapshot` and `snapshotProject`); `#u2learn button.u2all{` matches its dark rule too.
- **A new plan layer needs its key in the `drawPlan` cache key**, or it will not redraw.
- **A panel's text inputs need `keydown` `stopPropagation`**, or typing triggers the page's shortcuts. Keep drafts in state if the panel re-renders (field notes lost typed values once).
- **A re-render while a select or input has focus loses it**: refresh loops check `document.activeElement` is not an input before rebuilding.
- **New buttons need a description**: a `data-tip`, or a line in `LABEL_TIPS`. Run `tipaudit.js`.
- **`.u2wb .set` selects are capped at 118 px**; wider content overflows the 220 column.
- **iNaturalist asks for about one request a second.**
- **A GeoTIFF from the page's own `geoTiff()` exports `zv` (water lifted), not `z`.**
- **Units in tests:** a saved session can restore feet or metres over localStorage; select `#unit` in the test.
- **Pages deploy takes 40–55 s**; poll the live page for a marker.

## Open, waiting on Will

- **Try the field tools on a real phone at Encino Solo.** Walk the line, the phone level and field notes were tested only with simulated position and tilt. Start with field card 01 or 04 and mark up what doesn't match.
- **Shared records:** a Supabase project so Walker and helpers add to the same notes, surveys and paddocks (today they live in one project file). Only Will can create the account.
- **Read the manifesto, cards and syllabus in his voice** and say what sounds wrong; then decide whether and how `book/` is linked from the site.
- **LandXML with the equipment dealer** before a machine digs to it.
- Older, still open: tour voice-over, Walker's iPad report, opening the obj/glb exports in his CAD, animation references, the painter key on `localhost:8790`.

## Open, no dependency on Will

- A phone-width layout pass on the field tools (Walk the line, field notes) before the field test.
- Ground change surveys are not saved in the project.
- Budget and sheet: the budget is not on the drawing sheet.
- A paper needs field results; plan the before and after surveys and infiltration tests now so there is something to report.
- Refresh the stale artifacts (control map, private gallery, topo copy).
- The `e2e204` and flight drag checks read `rail2`; the value is now `rail3` (they print a blank but pass).

## Added later on 14 September (from Will's 2017 Grasshopper class)

Three tools from the MLA class scripts:

- **Study · what grows where** (id `suit`). SUIT_NEEDS gives each AGRO_LIB species its water need, most slope, sun side, frost tenderness and drainage. Wetness is a percentile rank of the topographic wetness index. Zones: steep, wettest, hot, cool, frost pocket, open. Each zone's plant list favours plants that do better there than across the site. A tap reads a spot and can plant the best plant there. Saved in S.rec.suit. White sage was added to AGRO_LIB and CARBON_KG.
- **Shape · steps** (id `steps`). The flights live in S.rec.steps, in lat/lon. The flight has n risers at (k+½)T, a half tread of level ground at each end, and a stride check of 2R+T within 620–700 mm. Cut and fill are integrated every T/8, not on the grid, because a grid cell can be wider than a tread. The section shows the whole flight plus a close-up. Steps are drawn on the plan whichever tool is open, so they print on the sheet.
- **Drawing sheet · model picture** set to lines (straight, one point, crisscross). `lineComposition()` is a row-by-row hidden-line painter. The controls are #sheetStyle, #lineN, #lineVe and #linePng. With a painter key, the model painting call is skipped when a line style is chosen.
- The #u2layBtn toggle is now larger and light orange (Will).

Test: e2e230 (23 checks) in session fb8fbb82's scratchpad. Regression 203, 205 and 211–229 passed, and the tip audit found none missing. Voice system.md was updated (coyote-voice 0c037a9) and the helper restarted. Permaculture library distilled: https://claude.ai/code/artifact/1a94f38b-db56-4669-8703-e2557f700578.

## Added later still on 14 September: dam and spillway, check dams

- **Shape · dam and spillway** (id `damwall`, S.rec.dam). It uses the water analysis dam: damAt(), S.damH as the full water depth, and damPool. The wall runs across the valley, perpendicular to the line from the pond's centroid to the dam, until the ground reaches the design crest.
  - Crest = full water + flood depth over the spillway + freeboard, built 10% higher. The crest width follows the USDA table, with 3:1 and 2:1 batters and a 2.4 × 0.6 m cut-off trench.
  - The spillway rule is √(catchment ha) m. The flood is Q = C·i·A/360, with C from S.runoff, and the flow depth comes from Q = 1.7·b·h^1.5.
  - Also reported: the storage ratio with its rating, a year's yield, evaporation, seepage, and a wall-line CSV.
  - The storm intensity, rain, runoff and evaporation inputs show "(example)" until entered.
  - dwSet fills S.rec.dam in place. An earlier version replaced the object and lost edits.
- **Shape · check dams** (id `checks`, S.rec.checks {gullies, points}).
  - A gully is traced along an.down from the top tap to the point nearest the bottom tap.
  - One-rock dams are a third of the full channel depth high, placed so the top of one is level with the foot of the next. Crossings are interpolated so the spacing doesn't creep.
  - Rock weight follows Zeedyk (20–40 lb at 1 ft, scaled by depth^2.1), with 4 rows plus a 2-row footer per dam.
  - Each dam can be marked built and logged after rain, and shows "full" at 90% of its height.
  - Headcuts get a Zuni bowl or a 3:1 rundown; media lunas are also available. Everything exports as GPX, and walk the line gains a "check dam gullies" source.
- Field card 18, "build one-rock dams", has a status line. Syllabus week 10 now uses it.
- Render functions for these panels only defer for a focused input when the refresh comes from a timer. Otherwise the panel never redraws after typing.
- Test e2e231 has 20 checks: a V valley whose fill matches the integral within 0.2%, and dam spacing on a 5% channel of exactly 3.00 m. Regressions passed and the tip audit found none missing.
- **Resolution at lot scale (Will's concern, not yet acted on):** Baja heights come from Terrarium tiles, which use INEGI continental relief behind them. Averaging the Encino Solo z15 tile into 8 m blocks loses only 4 cm rms, so there is no real detail below about 10–15 m. The grid is about 150 cells at any site width, so a lot shows smooth interpolation. US sites use 3DEP. The real fix at lot scale is a drone DTM or a points file, both of which the tool already imports.

## Also 14 September: render no-cut default, the on now strip, line drawings

- The render starts with no cut. This covers the default, the home site and a reopened session; project files keep the cut they were saved with.
- **On now strip** (commit cee66e4, which reverts on its own). It shows chips for looks changed since the site opened; the baseline is captured when the page first loads and again whenever a project is loaded. Chips cover history, rain, walk, recording, render, painted, cut, photo, overlay and colours. Pressing × returns a look to its baseline, and undo restores it for 10 seconds. Leaving site history stops the history animation, and leaving water stops the rain, except during tours. The layers & look · on now panel has show/hide and stop/keep toggles, saved in localStorage as coyote-onnow. Test: e2e232.
- **Make · line drawings** (id `lines`, S.rec.lineart). The engine is `lineArt(o)`, which returns layers of polylines in page mm.
  - Oblique hidden-line removal is vector-based. For each surface, a per-row "front" array holds the highest nearer ground on the page per half-cell column. Crossings are bisected, so lines are left out rather than painted over.
  - Nine styles: straight, point, cross, water, terraces, sun, keyline, change and fan.
  - Water paths trace straight downhill on the real z in half-cell steps and drop anything shorter than 8 cells. The stream network is D8, Chaikin-smoothed, in 3 width classes.
  - Sun tone is scaled to the site's own 3–97% range of lit shading, with cast shadow drawn as fully dark.
  - Keyline offsets are smoothed more as the offset grows, and parts that run backwards are dropped.
  - Layers are terrain, after, water and design. Outputs are a PNG, one plate per layer, and an Inkscape-layer SVG at the paper size.
  - The drawing sheet's model picture offers all nine styles through `sheetLines`.
  - Test: e2e233, including a synthetic ridge that hides exactly the rows in its shadow.

## G. Four tools from two Grasshopper plugins (14 September, later)

Will asked to build Groundhog and Docofossor into topo, after a Food4Rhino sweep ([Topo Plugin Scout](https://claude.ai/code/artifact/e38c3647-2697-438b-9bb4-366d61b073ac)). Most of both plugins already existed here (flow, catchments, ponds, flood pooling, wetness, pad, grade, path corridors, ground change), so only the missing parts were built. Methods were rebuilt from the plugins' docs, examples and published equations; no plugin code was copied (Groundhog is GPL-3).

| tool | task | from | stored | what it does |
| --- | --- | --- | --- | --- |
| stream crossing | study | Groundhog channel region + channel info | `rec.xing` | tap a stream; section square across it; rational-method storm flow; water level by halving until Manning's equation carries it; spill vs bank-full capacity; Kirpich arrival time; scour vs Fortier and Scobey bed speeds; ARR 2019 hazard H1–H6; Froude |
| what you can see | study | Docofossor dfViewshed | `rec.view` | viewpoints, a line, or mapped roads (≤150 sampled sources); eye height and target height; or where a building/tower shows from; edge-ray horizon sweep plus a direct sightline for cells the rays skip; earth curve less refraction |
| best route | shape | Docofossor dfShortestPath | `rec.routes` | A* with 16 moves, hard grade limit (foot 15, track 12, trucks 10, step-free 5%), cost above the preferred grade, stream crossings cost extra, protected ground (fit, recovery, ungrazed paddocks) and open water closed; Tobler time; build it as a path via `applyPath` |
| ditch and berm | shape | Docofossor dfCutOnPath + dfFillOnPath | `rec.ditches` | contour walk from a tap or a drawn line; trapezoid ditch (level, follows the ground, or falls 0.5–2%); berm height solved so it holds the dug soil; section; dig it into `z` with `snapshot()` (undoable) |

Test `e2e234.js` in session scratchpad `7d4521fc-d03a-4274-b332-fc532b15a7b4` (31 checks): Manning depth in a V valley vs the closed form (<2%), bank-full capacity, a wall's hidden zone vs geometry, no hidden specks on open ground, a 12% route up a 25% slope, no step-free route, protected ground avoided, contour held within 1 cm, ditch cut vs the node sum (0.4%) and vs the smooth integral (6%, the 1 m grid), balanced berm downhill, dig and undo, saved records, hover tips. Regression: e2e203, e2e205, e2e210–e2e233 all pass (e2e220 must run with its own scratchpad as the out dir, for field.jpg and rain.csv). tipaudit: 0 missing. `book/reference.md` regenerated. Voice `system.md` updated (coyote-voice `6a56f2d`).

Hooks: `__xgCalc(k)`, `__vwCompute()`, `__vwSeen(gx, gy)`, `__rtSolve(A, B, kind, cross)`, `__rtStats(k)`, `__dbCalc(k)`, `__dbContour(gx, gy, len)`, `__dbNew(pts)`.

Estimates, not verified: Manning's n and bed speeds are textbook values; storm intensity is an example until entered; views ignore trees and buildings; routes are first lines to walk, not alignments. On the Baja relief tiles (about 10–15 m real detail) small channels read wider and shallower than they are.
