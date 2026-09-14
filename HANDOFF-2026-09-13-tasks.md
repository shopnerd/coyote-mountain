# Coyote Mountain Studio: handoff, 12–13 September 2026 (the task layout)

Written at Will's request on 13 September. Read this first. The earlier record is `HANDOFF-2026-09-12-night.md`, whose items 1–22 cover everything up to the history drape. This file continues from its item 22. Memory: `project_coyote_studio.md`, `project_topo_reorg.md`, `project_coyote_voice.md`.

## Where things live

- **Public site:** repo `C:\Users\zolar\WebDev\coyote-studio` = GitHub `shopnerd/coyote-mountain`, served at https://coyotemountainfarm.com.
  - `topo.html` and `flight.html` each carry both layouts. **The new task layout is at `?new`**; the classic layout stays the default.
  - `gallery/` is the public gallery. `index.html` is the home page with the gallery card.
- **Private talking copy:** `C:\Users\zolar\WebDev\coyote-voice`, local git only, never pushed.
  - The helper runs on `localhost:8790`, started by `start-voice.ps1`.
  - The key lives in the `ANTHROPIC_API_KEY` user environment variable. Will set it himself.
- **Session scratchpad:** `C:\Users\zolar\AppData\Local\Temp\claude\C--Users-zolar-WebDev\10bf6f57-35b1-40b3-91be-0b431b7aab49\scratchpad`.
  - Tests are `e2e175`–`e2e207`.
  - `remap/` holds `controls.json` (all 219 classic controls), `build_map.py`, `ui2.js`, and the round patches.
  - `gal/`, `gal2/`: gallery building. `flightui/`: the flight helper's tests and screenshots.
- **Artifacts:**
  - Control map: https://claude.ai/code/artifact/1bdc1965-2032-4b72-bbd6-407fea1bb5fe
  - Private gallery (35 pieces, older than the site's gallery): https://claude.ai/code/artifact/acbd3cd4-a0da-4599-a03a-94399ddc145f
  - The topo artifact copy (062c2198…) is **stale**; republishing needs the full live copy read first.

## Standing rules (unchanged, plus this session's)

- Single-file vanilla JS and Canvas, no libraries, the house style, plain English, no native tooltips, never name other programs in the page.
- Test locally with Playwright against `python -m http.server 8765`, push, poll the live page with curl, show proof, update memory and the handoff.
- **`//` inside a one-line statement chain** comments out the rest of the line. It broke `const [lo, hi]` once more this session; use `/* */`.
- **The page has a generic `canvas{position:absolute;inset:0}` rule.** Any new canvas in a panel needs `position:static`; the `.u2prev` preview canvas covered its own button until it had that.
- **Rows moved into the task layout must never leave the document.** Unused rows wait in `#u2park`. Clearing the panel once detached them, and `setMode` crashed on a null.
- **Will's taste calls:**
  - no "+ more" folds (show everything);
  - keep the classic look;
  - rail and task column both draggable;
  - painting and rendering in Make only;
  - site history and the sandbox in Site;
  - `/` opens find a tool.
- **Commits:** topo.html, flight.html and gallery commits end with the Co-Authored-By line.

## What was built, in order (continuing the night handoff)

23. **History pace and glow** (`0ce2eb6`): 2.6 s a picture. Black replaces gold. A glow strength slider `#histGlowOp` (localStorage `coyote-hist-glowA`).
24. **Buildings in the model at city scale** (`17ef546`). `bldGround()` caches centre, reach, corner ground and roof per terrain. Buildings under 1 px (3 px while orbiting) are skipped. Under 4 px (12 px) they draw a roof only. Big ones draw only the walls that face the eye, as one path. LA with 50,048 buildings: a model frame went from 17 s to under 1 s, an orbit frame from 20 s to 0.15 s. Test `e2e198`.
25. **Gallery** (`4a5069b` onward):
    - **The pieces:** 129 Downloads exports clustered by dHash into 104 groups; picked by eye.
    - **On the site:** `gallery/` in the site style, with a full-size viewer (dialog, arrow keys).
    - **Edit mode:** `?edit` drops pieces (localStorage `coyote-gallery-dropped`). Applying drops means deleting the entry and the file, then pushing.
    - **Current contents:** 39 pieces, all rows full: 3 clips, 24 painted, 6 sheets, 6 studies.
    - **Links:** a full-width card on the home page (`gallery/thumbs/`) and a gallery button on the topo top bar.
26. **The reorganization, decided.** An interface review Will largely agreed with; route B: a new task layout over the same engine. See `project_topo_reorg.md`.
    - **The control map artifact** placed every classic control.
    - **Simple-mode bugs fixed first** (`191561d`): an empty geology heading, and an analyze hint that pointed at a hidden button.
27. **Task layout, first cut** (`f1eb787`). One block near the end of topo.html's main IIFE, comment "the task layout (?new)".
    - **`TASKS` and `LAYERS` specs** list original row selectors. `unit()` resolves a selector to its row, and rows mount into the panels.
    - **Tool buttons press the original buttons.** `setMode` and `setBrush` are wrapped so rows remount after the engine moves them. `modeFor(view, tool)` maps Plan plus the Study water and sun tools to `S.mode` `'analysis'`.
    - **The four tasks:**
      - **Site:** place, lot and survey, site history, sandbox.
      - **Shape:** select, sculpt, pad, grade a→b, path, plant, sketch, object.
      - **Study:** section, water, sun.
      - **Make:** render, paint, video, drawing sheet, 3D print, laser-cut model, CNC and maps.
    - **Around the tasks:** a top bar (`#u2head`) with project, undo, redo, find a tool, learn, gallery, flight, dark, classic layout. Plan / 3D / Section on the canvas (`#u2views`). A layers & look panel (`#u2layers`). A status bar (`#u2status`) with cut, fill and units.
28. **Round 2** (`1d20ea5`):
    - **No folds:** second groups follow a dashed rule.
    - **Rail drag:** `setRail` zooms `#u2rail` (base 300, localStorage `rail2`).
    - **Redo in the engine:** `redoStack`, `applySnap`, Ctrl+Shift+Z / Ctrl+Y.
    - **Layers that aren't available** show "none here" notes.
29. **Learn** (`798e4da`). `tourStart(steps)` accepts any list of steps. Seven chapters reuse TOUR demos and set `tour.onDone` (localStorage `coyote-learn`). In the task layout, the plain tour offer opens the learn menu. Test `e2e205`.
30. **The voice version reads the task layout** (coyote-voice `5accac6`). The catalogue covers `#u2*` containers, with blocks named tasks, tools, "<tool> settings", view, layers & look, status bar, and the learn card. `system.md` explains both layouts. Earlier in the session:
    - **Tools:** `choose` for dropdowns (`4a7bbe5`), `type_text`, and the painted and animated panels.
    - **Behaviour:** stop after two identical failures.
    - **Cost:** top-level `cache_control` (`a10d161`). The first real session measured about 8¢ a request before conversation caching; the dropdown failure alone cost 31¢ over 22 steps.
31. **Round 3** (`3426024`):
    - **`areaMap()`:** a satellite picker (Esri imagery plus boundary and place labels). The current site is outlined; draw a box with the site's aspect, whose width becomes the site width; search; fetch. `fetchArea()` sets the site width quietly, then calls `fetchWorld`.
    - **`sheetBox()`:** zoom to a box drawn on the plan.
    - **Select tool:** capture-phase pointer listeners on `#c`. `strokeDist` hit-tests lines, closed shapes and objects. Move, duplicate, delete, line colour and dash, all undoable. Pads and paths are carved into the ground and can't be picked.
    - **Previews:**
      - drawing sheet: `drawingSheet(sheetPictures(renderPicture…))`, drawn, not painted;
      - 3D print: `drawModel` plus the size;
      - laser: `laserSVG` rasterised with thickened strokes.

    Test `e2e207`.
32. **Flight planner task layout** at `flight.html?new`, built by a helper agent in the same pattern. Tasks: Area (site, survey area, drone survey), Aircraft, Flight (height and overlap, lines and speed), Plan (plan, export). Three learn chapters; flight numbers in the status bar. The helper's checks passed 39 of 39. The classic tour still runs. There is no general undo on that page.
33. **The task column drags** (`d28a136`): `#u2taskGrip`, 44–240 px, localStorage `u2tasksW`, on both pages.
34. **Design mode works with the task layout** (`?new&design`). Caution: drags inside the rebuilt left panel may snap back when switching tools; wording and sizes stick.
35. **Old maps in site history for wide sites** (`af622c1`).
    - **Cause:** the query asked for sheets that *contain* the site. A site wider than a quadrangle straddles edges and found none (Salton Sea at 8.3 km: 0 of 44 touching sheets).
    - **Fix:** take every sheet that *intersects* the site. Group a year's sheets by scale, and measure coverage on a 12×12 sample. Keep the most detailed group covering at least 90% (or the best one over 60%), and stitch its sheets with `lockRasterIds`.
    - **Result:** Salton Sea now gets 1956 (1:24,000), 1959 and 1965; Encino Solo still gets 1950 and 1954.

## Open, waiting on Will

- ~~Making the task layout the default~~ DONE 13 Sept evening (`ee68506`): default on topo and flight, `?classic` for the old layout (it has a "new layout" link back), old `?new` links still work. Will's design-mode spacing applied as rules first (`4442991`). Classic tests now load `?classic`.
- **Further tweaks** as he uses it: he said "there might be a few things that I'll continue to tweak".
- **The painter key on `localhost:8790`:** Will pastes it himself with the key button.
- **Older open items**, still open: tour voice-over, Walker's iPad report, opening the obj/glb exports in his CAD, animation references.

## Open, no dependency on Will

- Republish the topo artifact copy (read the live copy in full first).
- Task layout gaps:
  - previews for CNC and GIS;
  - a "none here" style note when a tool's rows are all hidden (Study · section in plan shows only its buttons);
  - phone-width testing of both new layouts.
- The voice version's `system.md` "what the tool can do" list is written against classic block names, with a note to use tasks and tools in the new layout; ~~rewrite it~~ DONE 13 Sept (coyote-voice `dcdbad6`): blocks as look lists them, every feature as task · tool with real labels, press-with-block for duplicate labels (paint), helper restarted. Also 13 Sept: task names run vertically in capitals (`aec09d4`).
- The private gallery artifact is out of date against the site gallery (39 pieces).

## How to verify quickly

- **Local:** `cd coyote-studio && python -m http.server 8765`, then `node e2eNNN.js <playwright-core> http://localhost:8765`. Playwright-core is at `C:\Users\zolar\AppData\Roaming\npm\node_modules\@playwright\cli\node_modules\playwright-core`.
  - **Task layout:** `e2e203` (every tool, views, find, layers), `e2e204` (folds, rail drag, redo, notes), `e2e205` (learn chapters), `e2e207` (map picker, sheet box, select, previews).
  - **Classic regressions:** `e2e164`, `e2e173` (previous session's scratchpad).
- **Page hooks:** `window.__ui2` = `{ state, chooseTask, chooseTool, TASKS, catalogue, applyView }`, and `window.__ui2probe(gx, gy)` gives a grid point's sheet position. `window.__dbg` also hands out `z` and `drawModel`.
- **Live:** curl `https://coyotemountainfarm.com/topo.html` for a marker; Pages takes 40–55 s.

Late 13 September (continued)

* The classic layout is removed (`9f6b41d`): no `?classic`, no link, no classic tour; `#tour` (teachers page) opens learn. The old rail stays hidden in the page because the task layout borrows its rows.
* Rail: task names stacked upright, 20 px capitals, 32 px column, equal-height tabs, hover descriptions on every new button; the settings column lays out at 220 px on both pages (localStorage `rail3`); lot and survey's clear sits alone at the bottom.
* Voice prompt rewritten for the task layout and stripped of classic (coyote-voice `dcdbad6`, `74a85f1`), helper restarted.
* Tests: classic tests are obsolete; e2e204 and the flight drag check read `rail2` and need `rail3`.
* Astra's review, verified: Shape · pad in 3D shows only topsoil and swell; laser-cut model has no scale control (it's under 3d print). Candidates next: pad settings that stay in 3D, a shared model size & scale for print/laser/CNC, typed numbers beside sliders, small group labels inside pad and make.

Astra items 1–5 and after (13 September, late)

* `6e0cadd`: plan tools keep their settings in 3D and section (a "draw it in plan" button; the sculpt radius/strength hidden there); one model scale in 3d print, laser-cut model and cnc and maps; click any slider value to type an exact number (`bind()` stores `el._fmt`, `exactSet` finds the nearest shown number); group labels via `'=name'` entries in a tool's rows (pad) and `group:` on tools (make); try steps in learn (`start`/`wait` on a step, next waits, `window.__tourNow` test hook). Test `e2e210` (29/29).
* `a2ef2f3`: learn "play all" on topo (7 chapters, 25 steps) and flight (3, 12); flight's site tool gets "pick an area on a map" (100 m to 6 km, rounded to 50 m). Test `e2e211`.
* Test copies updated in this session's scratchpad (ff66cb8b…): `e2e203.js` skips `=` labels, `e2e205.js` satisfies try steps and runs all chapters, `flightui/test2.js` without the classic section.
* Build-next list (Astra's ten ecology/engineering ideas plus Claude's five, ranked): https://claude.ai/code/artifact/48aad303-22e6-403b-94ee-26c3d3adb835. Recommended first: Ground Change (two drone surveys → erosion/deposit map) and the Earthwork & Resource Budget. The data-layer decision (likely Supabase) gates Field Observatory and most later tools.
* Ground Change built (`f2d0765`): Study · ground change. `CHG` state near `planShot`, `chgCompute()` / `chgUI()` beside the survey code, rows `#chgFiles #chgInfo #chgAlignRow #chgLodRow #chgShowRow` (+ `#chgFile`) in the hidden rail, wash drawn in `drawPlan` (key includes `CHG.ver`). Heights lined up by the median difference; noise floor `chgLod` (default 0.15 m); only-after mode compares with `base`, marked rough. Surveys are not saved in the project yet. Test `e2e212` (10/10: pit and mound volumes within 2% and 4%, 0.8 m drift removed). Voice prompt updated, helper restarted.
* iNaturalist checked: `api.inaturalist.org/v1/observations` with a bounding box answers with CORS open and no key (4,418 observations around Encino Solo). Merlin has no public API; bird IDs via BirdNET CSV or eBird. Added to the build-next list as rank 3, "Nature Records". Next build: Earthwork & Resource Budget.
* Path surfaces rebuilt (`2497e5e`): `pathSurface()` lays gravel rows / paving courses along the resampled centreline (the old lattice over the corridor polygon left holes on bends, spilled stones, and thinned out on long diagonals because the density cap used the bounding box); under 7 px wide it draws a dotted or tinted strip. Area paving jitter .7→.35. Plant row 3 + 2 in the task layout. Repro script `hatch.js` in this session's scratchpad.
* Earthwork budget built (`eff7e4c`): Shape · earthwork budget, a `panel:` tool (`budgetPanel` / `budBuild` / `budUpdate` / `budCsv` in the task-layout block). Quantities from `S.earth` (cut, fill, loose haul after swell, topsoil strip) and `S.strokes` (wall face from top/bot, gravel and paving paths and areas, trees, shrub beds, hedges). Rates kept metric in localStorage `coyote-budget`, shown per yd³/ft²/ft or m³/m²/m; 'example rates, not quotes' until edited; firmness ranges quoted −10/+15%, local −20/+35%, early idea −30/+60%; trips = loose haul / truck load, diesel 0.45 L/km round trip, 2.68 kg CO₂/L. Test `e2e213` (18/18). Voice prompt updated, helper restarted. Next on the list: Nature Records (iNaturalist layer).
