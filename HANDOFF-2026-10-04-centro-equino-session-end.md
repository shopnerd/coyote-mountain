# Centro Equino · handoff for the next session · 4 Oct 2026 (end of a very long session)

Read this first, then `HANDOFF-2026-09-24-centro-equino-session.md` §18 (newest notes at its top) for the build details.
Walker's side: `HANDOFF-2026-10-04-for-walker.md` and `COMO-EDITAR-EL-PAQUETE.md`. Everything is pushed (coyote-studio =
github shopnerd/coyote-mountain, will-os = shopnerd/will-os); both repos were at origin/main at the end.

## 0. UPDATE 4 Oct (later session): §1 is DONE as sheet E-1 → pack v43 (20 pages, E-1 = p19)
- `projects/electrical.py` (exec drain.py, like irrigation.py). Power from Andrés' main ranch buildings in the main-road water
  trench; MD main disconnect + sub-meter at the NE gate; 10 × 8 ft electrical room (stable frame x -56..-46, y -41..-33, south
  of C1); SP-2 at the stalls' SW end post, SP-3 at the bleachers; fixture schedule L1-L9 (dark sky, Ensenada 2006 regulation);
  solar from PVGIS (stable S 1743, N 1390, stalls ~1600 kWh/kWp): full 216 panels 94 kWp 149 MWh/yr, phase 1 = 16 panels 7.0 kWp.
  **The ranch already has a grid-tied system**: E-1 offers (a) tie into it or (b) own hybrid inverter + 15 kWh battery: ranch's call.
  Two render slots `E1-0` (blue-hour hill) and `E1-1` (EMPTY: the dusk lights-on render goes here; swap via the pack editor).
- D-3: troughs as natural pools (Walker's vetiver chamber = the lower spill basin, gravel over sand, bubbler, goldfish) and a
  first-flush standpipe at every downspout (8 in, ~8 ft, ~80 L). Backup `irrigation-2026-10-04-pre-vetiver.py`.
- Model: phase-1 panels on the stable's south roof (material `solar`, viewer switch "Solar, fase 1", OFF by default and OFF in
  model shots unless a view passes `solar: true`); `electrical room` object in site_extras.py (MATOBJ in export.py). Both
  index.html copies. Check shots: `renders/checkshot.mjs`. Open question for Will: solar ON by default in the model/renders?
- p10 text + stale comments now say 12 in tube posts.

## 1. (DONE, see §0) what Will asked for last
**Basic electrical and lighting plan** (Will, 4 Oct, after seeing the blue-hour hill view `4-hill-s-fan-blue-google`, which he likes
"quite a bit"):
- Lighting and outlets in **both stables** (the main stable and the covered stalls).
- Consider lighting for the **round pen, arena, roads, landscaping and the riding track**.
- "A fine line": **no light pollution, lighting should be sensitive**. Design it dark-sky: fully shielded, downward, warm
  (2200-2700 K), low and on switches/timers/motion; amber path and step lights at knee height; no uplighting; arena/round pen
  lights only on when riding, shielded and aimed in; nothing that lights the hills or the sky.
- Deliverable suggestion: a new sheet "E-1 Plan eléctrico y de iluminación · Electrical and lighting plan" (same pattern as
  `irrigation.py` / D-3: exec drain.py, site map + notes column, bilingual, a fixture schedule and a short dark-sky note), a
  stable-plan overlay with outlets/lights per stall/aisle/wash/tack (12 ft grid makes it easy), add it to pack.py after D-3.
- Will's image of it: "the stable will look incredible at night with the sticks and the light pouring out": warm interior light glowing through the gaps between the horizontal sticks and the open clerestory is the hero night shot; keep the outside dark around it.
- **Then render "early evening just after sundown"** with the lights on (the `blue` light variant + the fixtures in the brief):
  but renders are PAUSED (see §3) until the details are settled.

## 2. Where everything is
| | |
|---|---|
| Presentation page (public) | https://will.100xbtr.com/equino/pack/ (pack **v42**; click any rendering/drawing/text to enlarge; phone: pinch, double-tap, tap to go back; text opens as a reflowed reading view) |
| 3D model (public) | https://will.100xbtr.com/equino/model/ (plan view snaps square; contours on, labels off at start; roof structure switch) |
| Renderings gallery (unlinked) | https://will.100xbtr.com/equino/ (finalists, 3/4 Oct sections, "Abanico de cámaras · Camera fan", app renders) |
| Pack layout editor | https://will.100xbtr.com/equino/pack/edit/ (move/resize photos + drawings, swap photos, edit text; publish = `python pull_layout.py && python pack.py`) |
| Shared PDF | Drive pack folder `Centro-Equino-pack-11x17-2026-09-23.pdf` (always the newest; dated copies beside it, last `...-2026-10-04-v42.pdf`) |
| Drive pack folder | `G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack/` (renderings/, sheets/, handoffs) |

Build chain (projects/): stable change -> `python centro-equino-barn.py && python swap_stable.py` -> copy the stable stroke into
`_bak_0928/*.json` (snippet in §18) -> `cp _bak_0928/*.json . && python site_extras.py && python bleachers.py` -> `cd viewer &&
python export.py . && cp data.json ../../../will-os/equino/model/` -> sheets (`sheet1.py`, `irrigation.py`) -> bump `out=` in
pack.py -> `python pack.py` -> copy PDF over the shared name -> push both repos. Serve the viewer for shots:
`cd projects/viewer && python -m http.server 8792`.

## 3. State at the end
- **Renders paused** (Will: "pause renders until we get all the details finished up"). The round of five options per pack
  rendering (`renders/round_all.py`) was stopped. Done: el-west-horse and el-north (all five), plus OpenAI golden for el-south,
  el-east and 1-hero-sw. **Gemini prepaid credits are DEPLETED** (Google AI Studio "prepayment credits are depleted"): Will must
  top up before any Gemini painting. Resume later with `round_all.py` (skip views already in `img/fans.json`).
- **Stable posts are back to Andrés' heavy 12 in tubes (12 3/4 in OD)**, as first planned (Will, 4 Oct). `POST` in
  centro-equino-barn.py; plan/section/elevation drawings and spec text updated. The W tie ring now sits on a stub welded to the
  SW corner post. Existing paintings still show the thinner posts (fine until the next render round).
- Pack v42 contents: pages 2 elevations, 3 stable plan + east/south line-work elevations, 4 structure (line work, open doorway),
  5 covered stalls (over the stalls and from the hill repainted 4 Oct), 6 stalls drawing, 7 north/inside/bleachers/picnic
  (picnic = trailer as a café, raked arena), 8 site views, 9 plan view, 10-12 text/materials/inspirations, 13 topo, 14 grading,
  15 operator sheet, 16 grading sections, 17 drainage D-1 (road gully, 12 notes), 18 irrigation D-3, 19 discussion.

## 4. Decisions made today (do not re-propose)
- East trough 32 x 3.5 outside the NE run fence; north roof half feeds it, south half feeds C1 -> long trough + pad trough.
- Every trough pours from a stone spout into a small lower stone basin at its end (recirculating; Will's photo).
- Cistern C1 40 m3 at the stable SW corner; **C2 30 m3 just downhill of the round trough** at the stalls' SW end.
- Wash pad: pipe trellis with **green** grapes (Walker); tie-ups = W ring on the corner post, M bent-pipe hoop on the centre
  line (8 x 4.5 ft, 2 ft off the wall so the sliding door passes behind), E rings on run 1's fence. Wooden swing doors on wash
  and tack rooms.
- Walking path from the parking meanders through the pines and lands on axis at the east doors.
- Road gully: two legs + a new SW crossing (agreed in principle with the owner).
- Typography: one typeface (Plus Jakarta Sans) and size tiers by page; drawings are line work (real sticks, site stone).
- The trailer appears as a small café only in the picnic-side view so far; making it the default everywhere is Will's call.

## 5. Rendering methods (now a skill)
`WebDev/.claude/skills/camera-fan/SKILL.md`: camera fans and light/weather fans from true model shots, the hybrid brief, pose
figures, app renders through Will's ChatGPT (Plus) / Gemini (Pro) in Chrome (`apprender.py`), the A/B brief test (`briefab.py`).

## 6. Traps that bit this session
- A `// line comment` inserted into a one-line JS statement swallows the rest of the line (viewer broke twice): use `/* */`.
- Bash heredocs turn `\n` inside Python strings into real newlines: write patch scripts to files.
- Python patch strings with straight apostrophes inside single-quoted Python literals: use typographic ’.
- `fan.py` writes a per-run views file; several fans can run side by side.
- Will's own Drive mount is `G:`; the pack's OUTDIR is overridable with `EQUINO_PACK_DIR` (Walker's machine).
