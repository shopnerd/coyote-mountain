# Coyote Mountain Studio — session handoff, 8–12 September 2026

Written 12 September at a stopping point Will asked for. Read this first in a fresh session, then `HANDOFF-2026-09-08-render-paint-sandbox.md` items 30–50 for the code-level detail of everything below. Memory: `project_coyote_studio.md`.

## Where things live

- **Repo** `C:\Users\zolar\WebDev\coyote-studio` = public GitHub `shopnerd/coyote-mountain`, GitHub Pages at https://coyotemountainfarm.com. Pages: `topo.html` (the tool), `flight.html`, `index.html`, `teachers.html`, `walk/` (walkthrough), `projects/centro-equino.json`, `LICENSE.md` (PolyForm Noncommercial), `home.json` (Encino Solo, Will's save).
- **Artifact copy of topo.html**: https://claude.ai/code/artifact/062c2198-f39e-45bc-aa65-6025b1e7b42c — republish with `url` after every push.
- **Plan** (business / USC): https://claude.ai/code/artifact/40b48406-3be9-4d5f-9b1f-24fb3d019609 and `Google Drive\INBOX (1)\coyote-studio-plan-2026-09-08.md` (both carry the LandScope market note and the Earth Pro note).
- **Rail review** (the cut list that was executed): https://claude.ai/code/artifact/62eb87de-f9e6-41fb-8b6a-df320c77d462.
- **Tour doc for Will's edits**: `Google Drive\INBOX (1)\coyote-tour-stops.docx`, built by `scratchpad/tour-doc.py` from the live TOUR (28 stops deep, 18 simple; CARD + VOICE lines; DROP / "ADD AFTER n:" conventions). Waiting on Will.
- **Walker's Centro Equino share folder**: `Google Drive\MEXICO (1)\Chichihaus\Centro Equino paints` = https://drive.google.com/drive/folders/1VrjHj9A1rVydHj_FEKzaoYSUd4Mvl6VA (anyone with the link can view, inherited from Chichihaus; Walker is onestronghive@gmail.com and oramomi@gmail.com, both already editors). Holds 13 of Will's paints, 3 drawing sheets, 4 design boards, the project json, the walk-through video, README.
- **Scratchpad of this session** (tests, patches, scripts): `C:\Users\zolar\AppData\Local\Temp\claude\C--Users-zolar-WebDev\cfe5e248-717d-45c4-aa23-692bc3a89141\scratchpad`. Key scripts: `e2e152.js` (builds the Centro Equino layout from the Google Earth image), `walk-video.js` (records a walk-through), `walk-frames.js` (tour frames for the teachers page), `tour-doc.py`, `openai-paint-test.js`, `recv.py` (localhost:8766 receiver for pulling painted pictures out of Will's Chrome), patches 100–109.

## Standing rules (unchanged, all still in force)

- Single-file vanilla JS + Canvas, no libraries, Will's light house style (mono, paper/ink/ember), plain English, no native tooltips, never name other programs in the page.
- Test locally with Playwright (`python -m http.server 8765` in the repo; it dies between turns, restart it), then push, poll the live page with curl, republish the artifact, show visual proof, update memory + handoff.
- **Keys never in the repo and never handled by Claude.** Google key lives in the browser as `gemini-key`; OpenAI key as `openai-key` (Will pastes it with the key button). Will's `OPENAI_API_KEY` is in the Surface Book user scope; read it into a process with `[Environment]::GetEnvironmentVariable('OPENAI_API_KEY','User')` for Node tests, never print it.
- Never append `//` comments to one-line statement chains in topo.html (it has swallowed code twice; once more this session).
- Two painter tics stay: buildings hanging over the model edge, clouds drifting past the model.
- Will dictates; read for intent.

## What was built this session, in order

1. **Home file remade**, tour reordered top-to-bottom, simple/deep switch, paint prompt hardened (terrain + cut forced), deeper zoom, structured control (contour lines + rain pools + map mash-up), drawing sheet (painted model + true painted section + plan + analysis + notes, 150 dpi), multiple sections, CAD object import, reference photo, studio backdrops, tilt-shift tested via the words box (not in code).
2. **Rail cuts** (tag `rail-cuts`, before = `rail-before-cuts`): one sun clock, no flood layer, no ½/2× width, no random ground/relief, no reset, no rain pause in model, one eye height, plowing effect under keyline, a sheet block. Revert: `git revert --no-edit rail-cuts`.
3. **Rail sections** (tag `rail-sections`, before = `rail-before-sections`): headings view · world · draw · sheet / model · render · paint / sections · geology / water · sun / site · grading · fabricate · project · exports. Titles now ember, 11.5 px. Revert: `git revert --no-edit rail-sections`.
4. **Tour** follows the blocks (28 deep / 18 simple); **paint this section** replaced "see this section in 3d" (paints the active cut with the drawing sheet's camera rule; drawn without a key).
5. **Reference photos, plural**: up to three, roles the place / the look / the building.
6. **Centro Equino** (Walker's equestrian centre, Hacienda Chichihuas, Valle de Guadalupe): laid out on the real ground from the annotated Google Earth image; Will's point 32.000240, -116.763689 is beside the round pen; barn as a placed gable object 72×40 ft. Project link: https://coyotemountainfarm.com/topo.html?proj=projects/centro-equino.json (the `?proj=` opener is new; the file is public). Real-place paint recipe: aerial on, water off (raw ground), vertical exaggeration 1, hour 3 pm, no cut, words "gentle valley floor, flat open dry pasture, hardly any rocks, vineyard rows beyond".
7. **Walk mode** (walk button beside orbit/sculpt): first person at eye height, W A S D / arrows, Q E turn, shift runs, drag to look; no cut on foot; ~10 fps while moving in headless Chromium.
8. **Painted ground** (painted button beside aerial photo after a paint): the last painting baked onto the terrain through its camera with a depth test; placed objects take the painting's colour; walk inside the painting. Photo-ground white grid fixed (shade seam overlap, no rim under patches, triangle-mapped big patches).
9. **Walk-through video** from the tool itself (`walk-video.js` → `centro-equino-walkthrough.mp4`, in the share folder). Higgsfield's free plan refuses all video models; Will chose the OpenAI key over Higgsfield.
10. **OpenAI painter**: painter menu (google / gpt-image-1-mini ~1c / gpt-image-2 ~5c / gpt-image-2.5 sunburst ~25c), key `openai-key` in the browser, `images/edits` with the control letterboxed 1536×1024 and cropped back, fidelity retry, plain refusal message (OpenAI's 401 carries no CORS header). Verified from Node with the environment key: gpt-image-2 holds the model; mini invents its own scene. Not yet run in Will's own browser.
11. **Backlog sweep**: wetness index + landforms (geomorphons) layers; kml + geotiff exports at true coordinates (validated by parsing); walkthrough regenerated; painter pen-lines-hidden switch; no-invented-buildings rule in every style; painted objects on foot.
12. **Plan**: LandScope market note (per-map $349 floor, credit packs, free demos, per-site pricing idea) and the Google Earth Pro note (desktop installer gone 25 June 2027; download the installers now; "what people did in Earth Pro, in a browser, with grading and a sheet at the end").

**Everything after 11 September 22:00 is in `HANDOFF-2026-09-12-night.md`** (the seams, the score, the export menu, points, animate history). Read that one first.

## Open, waiting on Will

- Tour doc edits in the docx → apply to TOUR + `vo-script.txt` → respell (ky-oh-tee, kee-points, key-line, pee en gee, see en see) → record with `WebDev/twin` F5-TTS **in float32** (`vo-batch32.py`; fp16 is silent on the GTX 1660 Ti) → `vo-assemble.py` → `vo_check.py` (faster-whisper) → send. Narrated cut goes live only after his voice verdict; the silent cut is live now.
- Six example picks for the teachers page gallery (38-paint contact sheet in the scratchpad, or "you pick").
- Paste the OpenAI key once in his browser and try gpt-image-2 / 2.5 on Centro Equino with the barn photo as "the building"; then the live proof of paint → painted → walk.
- Download the Google Earth Pro installers and keep them with the backups.

## Open, no dependency on Will

- ~~Animating 2D drawings~~ BUILT (item 13). Possible follow-ups if Will wants them: a tour stop for `animate` (goes in with his tour doc edits), the walker crossing trees, the pies as a cut·fill history, an mp4 instead of webm (needs a converter; the browser only records webm).
- USGS unified geology (GeMS / NGMDB): swap in behind the geology switch once there is a lat/lon query endpoint; Macrostrat stays until then (and for Mexico).
- Parametric drawing sheet (drag boxes) — backlog. Deeper geology sources — backlog.
- Sandbox real-hardware test at USC (Will), teachers page tuning.

## How to verify things quickly

- Local: `cd coyote-studio && python -m http.server 8765`, then any `e2eNNN.js` in the scratchpad with `node` (Playwright-core at `C:\Users\zolar\AppData\Roaming\npm\node_modules\@playwright\cli\node_modules\playwright-core`). The page exposes `window.__dbg(fn)` with S, AI, camera, aiControl, aiCall, aiPrompt, snapshotProject, bakePainted, renderPicture, kmlOut, geoTiff, W, H and more for tests.
- Live: `curl -s https://coyotemountainfarm.com/topo.html | grep -q '<marker>'` in a loop; Pages takes 10–70 s.
- Will's Chrome (his keys): claude-in-chrome tools; hidden file inputs via `find` + `file_upload`; pull a painted picture out with `recv.py` on 8766 and a `fetch` POST of the panel image's data URL.
