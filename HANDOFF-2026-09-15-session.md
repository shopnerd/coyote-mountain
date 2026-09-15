# Coyote Mountain Studio · handoff, 14–15 September 2026 (class tools, dams, line drawings, on now, readout)

Written at Will's request on 15 September. This covers one long session. It started from `HANDOFF-2026-09-14-field-tools.md` and ran alongside the plugins session (`HANDOFF-2026-09-15-plugins.md`) and a phone-layout session. Read those two for their own work. Memory: `project_topo_reorg.md`, `reference_gh_landscape_class.md`, `reference_permaculture_library.md`.

**In one paragraph:**
- Will's 2017 MLA Grasshopper class files were scanned. Three of their ideas became tools: what grows where, steps, and line drawings on the sheet.
- His PDC permaculture library was distilled into an artifact. Its top suggestion became the dam and spillway calculator.
- Check dams were added as a hands-on work-day tool, with field card 18.
- The render now defaults to no cut.
- An "on now" strip shows every look or moving picture that is on, and lets you turn it off.
- Line drawings grew into a nine-style plotter tool with layered SVG.
- The pointer readout came back in the status bar.
- The plugins session's uncommitted last round (solar array, field maps, spot grading) was merged and published.
- Everything is live and the working copy is clean.

## Where things live

| what | where |
| --- | --- |
| site repo | `C:\Users\zolar\WebDev\coyote-studio` = GitHub `shopnerd/coyote-mountain`, live at coyotemountainfarm.com (Pages, 40–55 s after a push) |
| voice copy | `C:\Users\zolar\WebDev\coyote-voice`, helper on localhost:8790 (restarted after each `system.md` change) |
| this session's tests | scratchpad `C:\Users\zolar\AppData\Local\Temp\claude\C--Users-zolar-WebDev\fb8fbb82-764c-4664-991c-53f7aee1e790\scratchpad`: e2e230–e2e233, e2e242, nocut.js, stepsvis.js, laybtn.js, ghscan.py, ghgraph.py, patch scripts |
| older tests | e2e203–229 and tipaudit.js in `…\ff66cb8b-…\scratchpad`; e2e234–241 (plugins) in `…\7d4521fc-…\scratchpad` |
| playwright-core | `C:\Users\zolar\AppData\Roaming\npm\node_modules\@playwright\cli\node_modules\playwright-core` |
| permaculture artifact | https://claude.ai/code/artifact/1a94f38b-db56-4669-8703-e2557f700578 |

Scratchpads are temporary. Copy the tests somewhere safe if they need to outlive temp cleanup.

## Commits, in order

| commit | what |
| --- | --- |
| `d71995d` | Study · what grows where; Shape · steps; the drawing sheet's model picture as lines (straight, one point, crisscross); white sage in AGRO_LIB; layers & look button larger and light orange |
| `b55c03e` | Shape · dam and spillway; Shape · check dams; field card 18; syllabus week 10 |
| `53ac31b` | render starts with no section cut |
| `cee66e4` | the on now strip (its own commit, so it can be reverted alone) |
| `09e034c` | Make · line drawings: nine styles, layered plotter SVG, plates |
| `cc7b4c6` | pointer readout in the status bar |
| `c3d1aa0` | plugins round 6 (solar array, field maps, spot grading), merged and published |

Voice commits: `0c037a9`, `6782986`, `050375f` and `616362d`.

## What was built

### The Grasshopper class scan (no code)

The 48 `.gh` files in `Google Drive\USC ARCH\Grasshopper for Landscape Arch` were decoded with the canoe-studio GH_IO parser. A cluster-aware version is `ghgraph.py` in the scratchpad.

The 2017 final, `Keyline_Automation.gh`, was already an Encino Solo keyline study. Most class ideas already exist in topo. Details are in the memory file `reference_gh_landscape_class.md`.

### Study · what grows where (`suit`, `S.rec.suit`)

- `SUIT_NEEDS` gives each AGRO_LIB species: water need, the most slope it tolerates, sun side, frost tenderness, and whether it needs drainage.
- Each cell is read for slope, sun-facing (south-west in the north), wetness and cold low spots.
  - Wetness is a **percentile rank** of the topographic wetness index.
  - Cold low spots are ground more than 1.5 m below its surroundings within about 60 m.
- The score is the product of how well each need is met, and the weakest need gives the "why".
- Zones: steep, wettest, hot, cool, frost pocket, open.
  - Each zone's plant list favours plants that do better there than across the whole site (zone mean + 0.6 × the difference).
  - Otherwise tough generalists top every list.
- A tap reads out a spot, with a button to plant the best plant there.
- Test e2e230: a cool slope ranks oak above rosemary, a hot slope ranks sage above oak, and watering widens where lemon fits.

### Shape · steps (`steps`, `S.rec.steps`)

- A flight is drawn as a centreline, stored in lat/lon.
- It has n risers at (k + ½)·T, with half a tread of level ground at each end.
- Stride check: 2R + T between 620 and 700 mm.
- Warnings for short treads, long strides and more than 12 risers.
- Cut and fill are **integrated every T/8, not on the grid**, because a grid cell can be wider than a tread.
- The section shows the whole flight plus a close-up of the first steps.
- Flights draw on the plan whichever tool is open.

### The sheet's line picture and Make · line drawings (`lines`, `S.rec.lineart`)

`lineArt(o)` draws polylines in page millimetres, in layers: terrain, after, water and design.

**Oblique view, hidden-line removal (vector).** For each surface, a "front" array holds the highest nearer ground on the page, per row and half-cell column. A point is hidden if any nearer row rises above it. Crossings are bisected, so lines stop cleanly rather than being painted over.

The nine styles:

- **straight, point, cross**
- **water:** drops traced downhill in half-cell steps on the real z. Paths shorter than 8 cells are dropped, so flat ground stays blank.
- **terraces:** contours on a stepped surface.
- **sun:** tone comes from how many rows survive. Shading is scaled to the site's own 3–97% range of lit ground, and cast shadow is fully dark.
- **keyline:** offsets are smoothed more the further they are from the keyline, and parts that run backwards are dropped.
- **change:** base against z, or two surveys through CHG.
- **fan:** stacked profiles with their own occlusion.

The water layer is the D8 network, Chaikin-smoothed, in 3 width classes.

Exports: PNG, one black plate per layer, and an SVG with Inkscape layers at the paper size and a 0.3 mm pen. `sheetLines()` gives the drawing sheet all nine styles. The first three still go through the older `lineComposition()`.

Test e2e233: a synthetic 50 m ridge leaves rows far behind it complete, and rows in its shadow at exactly 0%.

### Shape · dam and spillway (`damwall`, `S.rec.dam`)

- It uses the water analysis dam: `damAt()`, `S.damH` as full water depth, and `damPool`.
- The wall runs across the valley, perpendicular to the line from the pond's centroid to the dam, until the ground reaches the design crest.
- Crest = water + flood depth over the spillway + freeboard, built 10% higher for settling.
- Crest width follows the USDA 590 table. Batters are 3:1 upstream and 2:1 downstream, with a 2.4 × 0.6 m cut-off trench.
- Spillway width is √(catchment in ha) m.
- Design flood: Q = C·i·A/360, with C from `S.runoff`. Flow depth comes from Q = 1.7·b·h^1.5.
- Also reported: storage ratio with its rating, a year's yield, evaporation and seepage, and a wall-line CSV.
- Storm intensity, rain, yearly runoff and evaporation all say **"(example)"** until entered.
- Test e2e231: on a V valley, the wall's fill is within 0.2% of the integral.

### Shape · check dams (`checks`, `S.rec.checks` {gullies, points})

Rules come from the Zeedyk and Sponholtz field guides, read from the PDC library.

- **One-rock dams**, not tall check dams.
  - Height is a third of the full channel depth.
  - The top of one dam is level with the foot of the next. Crossings are interpolated, so gaps don't creep.
  - Rock weight is 20–40 lb for a 1 ft channel, scaled by depth^2.1.
  - Four rows sit on a two-row footer.
- A gully is traced along `an.down` from the top tap to the point nearest the bottom tap.
- Each dam can be marked built and logged after rain. It shows "full" at 90% of its height.
- Headcuts get Zuni bowl dimensions (apron at 2–3H, a one-rock dam 4–6H below) or a 3:1 rundown. Media lunas are also available.
- GPX export, and walk the line gains a "check dam gullies" source.
- Test e2e231: dams on a 5% channel are spaced exactly 3.00 m apart.
- Field card 18, `book/field/18-build-one-rock-dams.md`, is written as a work day with a status line ("not yet tried on the land").

### Render no-cut default

`S.rendCut` now defaults to `'none'`, and the menu says so.

The home site (`home.json` stores `black`) and a reopened session both force `'none'`, then call `rendUI()`. Project files opened on purpose keep their cut. `sectionCamera()` still uses a black cut for the sheet's section picture and restores it afterwards.

### The on now strip (`cee66e4`)

- Chips show under layers & look for looks changed **since the site opened**.
  - The baseline is captured on the first draw and after every `loadProject`. The function is wrapped for this.
  - Covered: history, rain, walk, recording, render, painted, cut, photo, overlay and colours.
- A chip's name jumps to where the look is set. × returns it to the baseline, and an undo chip lasts 10 s.
- Leaving site history stops the history animation, and leaving water or water budget stops the rain. Neither happens during a tour.
- layers & look · on now has two toggles: show or hide the strip, and stop or keep the moving pictures. They're saved in localStorage as `coyote-onnow`.
- Test: e2e232.

### Pointer readout (`cc7b4c6`)

`readout(g)` already fed the hidden classic header. It now also writes `#u2read` in the status bar: lat/lon, elevation, the existing height where graded, and slope.

In 3D without a sculpt brush, a throttled `pick()` feeds it about 16 times a second. It clears when the pointer leaves the map and is hidden on touch screens (`pointer:coarse`). Test: e2e242.

This was built in a temporary worktree, because the main folder held the plugins session's uncommitted work.

### Plugins round 6 merge (`c3d1aa0`)

The plugins session left the solar array, field maps and spot grading, plus its handoff, uncommitted. At Will's ask they were committed locally, rebased onto af687f6 and cc7b4c6 with no conflicts, then tested and pushed. e2e234–241 print **"ALL PASS"**, not a FAILS count.

### Smaller

- **Permaculture library:** four readers covered the 896 files, and the artifact ranks the ideas. Unread scans: Mollison's *Designers' Manual*, Yeomans' *Water for Every Farm*, Nelson's *Small Earth Dams*.
- **Lot-scale resolution (assessed, not built):**
  - Baja heights come from INEGI continental relief via Terrarium tiles. At Encino Solo, z15 averaged into 8 m blocks loses only 4 cm rms, so there's no real detail below about 10–15 m.
  - The grid is about 150 cells at any site width, so a lot shows a smooth guess. US sites use 3DEP.
  - The fix is a drone DTM or a points file, which the tool already imports. The recommended next step is an honest data-resolution note in the status bar.

## Verified and estimated

**Verified by tests:**
- Steps cut and fill balance on an even slope.
- Dam wall fill against the integral.
- Check dam spacing.
- Rational method and weir arithmetic.
- Hidden-line removal on the ridge.
- The readout's lat/lon against `nodeLatLon`.
- The plugins session's own checks.

**Estimates, and the panels say so:**
- The plant needs in SUIT_NEEDS (Claude's rough ranges for a dry site).
- All dam rules of thumb (Australian and US farm-dam guides, not checked for Baja).
- The example storm intensity, rain, runoff and evaporation.
- Check-dam rock weights outside 1–1.5 ft channels (extrapolated).
- Solar prices, and the field maps' sample data.

## Gotchas learned this session

- **Apostrophes in heredocs.** An apostrophe inside a Python heredoc that writes JS (`sheet\'s`) came out as a bare `'` and broke the page. Write patch scripts with the Write tool, or avoid apostrophes in JS strings.
- **Panels that never redraw.** Panels whose render skipped when a panel input had focus stopped redrawing after typing. Only timer-driven refreshes should defer (`dwRender(soft)`). A press or change redraws at once.
- **Settings objects replaced.** `Object.assign({defaults}, S.rec.x)` on every call replaces the object, so panel closures edit a copy and lose the edit. Fill defaults in place.
- **Canvas positioning.** A canvas inside a panel needs `position:static;inset:auto`, because of the page-wide canvas rule. The steps section escaped the panel once.
- **home.json overrides defaults.** It carries saved settings (rendCut black), so a changed default isn't enough on its own.
- **Non-breaking spaces.** Readout and panel text use `&nbsp;`. Normalise `[\s\u00a0]+` in test regexes.
- **Detached backgrounding.** Running tests with a trailing `&` inside a backgrounded command sends the completion notice at once. Wait on the log file instead.
- **Worktree folder locks.** A local http.server started in the worktree holds a Windows lock. Stop it before `git worktree remove`, then prune.
- **Test output formats.** The plugins tests print "ALL PASS"; the older ones print "FAILS n" or "errors:".
- **Default grid size.** The sample site at 3 km has cells of about 20 m. Dam and gully tests run on a 400 m site (`setSiteW(400)`).
- **Pre-existing tour gaps.** Two learn steps report "no target" (12 of 25; grade a pad 3 of 5). They were there before these changes.

## Open, waiting on Will

1. Try field card 18 on a real gully, and mark up what doesn't match.
2. Local figures for the dam tool: design storm intensity, yearly rain, runoff and evaporation for Encino Solo.
3. Decide the lot-scale step: a data-resolution note in the status bar, and planning a drone DTM of the house area.
4. Send one A3 line-drawing SVG to the shop plotter or laser before trusting the files.
5. Astra's review (pasted 14 September), not acted on:
   - card 01's "dead level";
   - the reference manual's "survey noise, not change";
   - grazing's "half their starting height";
   - a status line on each field card;
   - the licence versus commercial land-care use;
   - trimming the syllabus to a core plus strands.

## Open, no dependency on Will

- The status bar's data-resolution note (proposed above).
- Next ideas from the permaculture artifact:
  - zones and sectors;
  - windbreak designer (needs a wind direction);
  - grazing recovery chart;
  - road drainage planner;
  - headcut finder;
  - pond drawdown (needs evaporation data);
  - plant library natives from RegenPLANTS.
- Line drawings: water lines leave flat ground blank, and keyline offsets still cross a little where the two sides meet.
- The Astra wording fixes that need no decision: "survey noise", "dead level" and "half height".
- The earlier open list in `HANDOFF-2026-09-14-field-tools.md` still stands: phone-width pass on field tools, ground change surveys not saved, budget not on the sheet, stale artifacts.
