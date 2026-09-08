# Handoff: render, paint it, sandbox, tour, simple/deep, geology
Date: 2026-09-08. Written by Claude (Fable 5.1) for Will, and for whoever picks the studio up next (a later Claude session, or another model).

If you are reading this with no other context: everything you need is here. The topo tool is one file, `topo.html`, about 3,300 lines of vanilla JavaScript and Canvas, no libraries, in the public GitHub Pages repo `shopnerd/coyote-mountain`, live at https://coyotemountainfarm.com/topo.html. The earlier handoff `HANDOFF-2026-09-07-flight-survey.md` covers the flight planner and the drone-survey import and is still current.

## 1. What changed since the 9/7 handoff, in the order it landed

1. **Grading tools.** Pad (rectangle, oval, drawn shape; balanced cut and fill or held level; edges as slopes, walls where needed, or walls), path (centreline, corridor draped on the ground, raised or sunk, bare/gravel/paved), grade a→b now cuts and fills instead of pushing earth, retaining walls drawn and counted, building relief for milling (blocks, pedestal, recess, outline), cnc lines DXF in the project's units.
2. **Render mode** (model view → render). A section-perspective: free camera (eye level, low aerial, high), real sun by month and hour with cast shadows, sky (clear, cumulus, marine layer, overcast), the section cut along A–B as a black or white poché band that spans the whole frame with blank paper below it, or no cut, in which case the base slab and its sides are drawn so it reads as a model on a table. `renderSet()` makes a multi-view sheet.
3. **Paint it.** The render becomes the control image for an image model (Google Gemini image, model id in localStorage `gemini-model`, default `gemini-3.1-flash-image`; the key lives only in the browser's localStorage `gemini-key`, never in the repo). Four styles: photograph, watercolour, ink wash, map mash-up. The control frame is *structured*: contour lines drawn on the ground, standing rain pools in blue, the surface colour map you chose (elevation, slope, aspect, sun...) kept at full strength, no captions or credits, no blue tint in shadows. The prompt is written as a strict image-to-image edit and names everything the control carries. See section 3 for what the painter still gets wrong.
4. **Sandbox** (`sandbox/bridge.py`, `sandbox/README.md`). A depth camera over real sand drives the tool; projector window with keystone. Built against the Orbbec Femto Bolt through Orbbec's K4A wrapper DLLs, tested only with `--mode fake`. Real-hardware test is pending at USC.
5. **Guided tour**, 27 stops in deep, 17 in simple, ordered top to bottom: header, command row, then the rail in plan, model, section (with the geology stop), analysis, then world, site, grading, fabricate, exports. Steps marked `deep: true` are skipped in simple. The tour hands the user's own project back at the end.
6. **Simple vs deep** switch in the header. Simple keeps every tool whose result shows on the sheet in one gesture; deep adds tuning, calibration, fabrication and the extra exports. First visit is simple, remembered in localStorage `coyote-depth`. Implementation: class `deep` on about 58 elements plus one CSS rule `html[data-depth="simple"] .deep{display:none!important}`; hidden settings keep their values.
7. **Geology under the section.** A `geology` switch in the section view (deep). Samples nine points along A–B, asks Macrostrat (`/api/v2/geologic_units/map?lat&lng&scale=large|medium|small|tiny`, first non-empty scale wins, CORS open) for the mapped unit, draws bands under the existing ground hatched by rock type, with name, lithology and age. Depth is nominal (45% of the section relief) and the sheet says so. At Encino Solo: Neogene intermediate volcanics on the west, Late Cretaceous sandstone on the east.
8. **Model zoom** to 24× (was 6×); tiles subdivide when larger than 30 px on screen with bilinear heights, slopes and light, so deep zoom shades smoothly.
9. **Home project** is Will's clean Encino Solo sheet saved 2026-09-08 00:14 UTC (`home.json`).
10. Dark mode across the studio, landing page at the root, sketch studio hidden at `sketch.html` (unlinked, noindex, still in the public repo).

## 2. How the paint pipeline works (so you can change it safely)

- `aiPaint()` sets `S.rendOn = true; S.mode = 'model'; S.aiCtl = true`, draws the model at 1536×864 into an offscreen canvas, draws rain pools on top with `drawRainOverlay(..., poolsOnly = true)` (pools on the camera side of the cut are skipped via `rendCutSide` / `camSideOf`), then resets the flags. `drawModel0` returns right after `rendCutSide = cutSide` when `S.aiCtl` is set, so nothing textual reaches the control.
- `aiPrompt()` builds the text from `AI.style`, `AI.ctl` (`pools`, `map`, `slab`), `aiScene()` (month, hour, sky, place, strokes, buildings, walls, the aerial ground-cover reading, and the user's words box) and the cut description.
- Requests: `POST /v1beta/interactions` first (`input: [text, image, image?]`, `response_format: image`), fallback `models/{model}:generateContent` with `inlineData` and `responseModalities: ['IMAGE']`. `findImg()` digs the base64 out of either shape. The aerial photo goes along as a second image when it is on, with wording "colour and texture only, never layout".
- The painted image element is created on demand inside `#aiImgWrap`; `#aiPanel` shows it with save png / again / close.

## 3. What the painter still gets wrong, and what to try next

- **Landmarks from the place name.** Told "Seattle" it added the Space Needle. Leave the place name out of the words box to stop it.
- **Water it wants to see.** A large blue area in the control is respected; a subtle one sometimes grows. The prompt already forbids water when the site has none.
- **Framing drift.** When the model is small in the frame the painter sometimes grows the terrain to the edges. Zoom so the model fills the frame before painting.
- **Next lever if control is still too loose:** a depth-conditioned image model (a second provider) with our depth map as a hard constraint. The renderer can output a depth map for free.

## 4. Testing and deploy method (keep doing this)

- Patch files are Python scripts with assert-before-replace (`rep()`), applied to `topo.html`; then `node -e` runs `new Function` over every `<script>` block as a syntax check.
- Playwright-core (`C:\Users\zolar\AppData\Roaming\npm\node_modules\@playwright\cli\node_modules\playwright-core`) end-to-end scripts run first against `python -m http.server 8765` in the repo folder, then against the live site after `git push` (GitHub Pages takes about 60 s; poll `curl | grep` for a new identifier).
- Live checks that exist in the scratchpad from this session: `e2e122` (deep tour, every stop's target visible), `e2e123` (render cut, zoom), `e2e124` (simple/deep, simple tour), `e2e125` (oblique cut, paper never above the band), `e2e126` (paint control and prompt with a mocked Gemini route), `e2e127` (no-cut slab), `e2e128` (geology against the real Macrostrat API).
- The artifact copy of `topo.html` at https://claude.ai/code/artifact/062c2198-f39e-45bc-aa65-6025b1e7b42c is republished after each change (outer document tags stripped).

## 5. Traps that bit this session

- **Never append a `//` comment to the end of a one-line JavaScript statement chain in `topo.html`.** It swallows the rest of the line. It broke the paint panel once and the whole render mode once (live for about ten minutes) before the live check caught it.
- The depth switch handler and the theme handler live *outside* the main IIFE: `toast()`, `resize()` and `S` are not in scope there.
- `S` and `TOUR` are not reachable from Playwright's `page.evaluate`; tests read the DOM instead.
- Tour targets must be elements that are always visible: `#bldRow`, `#bldModeRow`, `#seaRow`, `#roadRow`, `#ovRow`, `#trimRow` are conditional.
- The paper polygon under the cut must be extended along the band's own line, not horizontally, or a wedge of paper appears above the band on oblique cuts.

## 6. Open items

- Sandbox with the Femto Bolt at USC: `bin/k4aviewer.exe` first, then `python sandbox/bridge.py --mode k4a --dll "<wrapper>\bin"`, open http://localhost:8787/topo.html (the https site cannot fetch localhost).
- Geology: deeper sources (SGM Mexico 1:50,000 sheets, well logs, SoilGrids for soils) if real depths are wanted.
- Depth-conditioned painting (section 3) if Gemini's edits stay too free.
- The sketch studio at `sketch.html` needs work before it is linked again.
