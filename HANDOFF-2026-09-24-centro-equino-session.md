# Handoff · 22–24 Sep 2026 · Centro Equino, the whole session

Read this first for anything about Walker's Centro Equino (Chichihuas, Valle de Guadalupe). It covers one
long session: grading the site in the topo tool, the water plan, ~45 renderings, a bilingual 11×17 print
pack, a laser-cut site model, 3D-print parts, and the stable's structure. The detailed day logs are
`HANDOFF-2026-09-23-grading.md` (grading steps and traps) and `HANDOFF-2026-09-22-equine.md` (older traps).

**Standing rules for this project:** every sheet/report is bilingual (Spanish first, English italic).
Keep every rendering, good and bad. Walker's email is **onestronghive@gmail.com only**. The name is
**Andrés** (not Andreas).

---

## 1. THE CURRENT STABLE DESIGN (agreed 24 Sep, not yet built into anything)

Walker's concept sheet (`projects/walker-stable-concept-sheet.webp`, also in the Drive pack folder)
predates the sticks and the steel. Will's merged direction, word for word in spirit:

- **Frame:** Andrés' heavy 12 in steel tubes as **pipe portal frames**, exposed.
- **Walls:** **stacked rock, big to small, 4.5 ft tall all the way round the building**, including the
  short ends beside the entries.
- **Above the rock:** **tomato stakes** (hard, slightly wavy wood) run horizontally, on light verticals,
  letting air and light through. All four sides.
- **Entries:** a **large entry at both short (gable) ends**, the portal frame exposed there.
- **Roof:** metal, with **occasional translucent panels as skylights**. **No ridge vent.**
  **2 ft overhang on the long sides.**
- **Still to confirm with Will/Walker** (from her sheet, not re-stated): 72 × 40 ft footprint;
  6 stalls on the north side with 12 × 40 ft runs; wash, tack, feed and alfalfa/storage on the south;
  14 ft centre aisle; roof colour (her sheet: dark; earlier: sky blue); whether the barn stays where the
  topo drawing has it (her site plan shows another spot).

**CONFIRMED by Will 24 Sep (later session):** Walker's layout (72 × 40 ft, 6 stalls + 12 × 40 ft runs
north, wash/tack/feed/alfalfa south, 14 ft aisle) · roof **sky blue** · barn stays at the topo-drawing
spot (pad 1087.6) · **big pipe for eave beams and purlins for now** (Andrés' timbers later, sizes unknown).

**REBUILT 24 Sep (later session). Everything except the renderings now uses the new design:**
- Frame check `laser/portal_frame.py`: 40 ft span, 2 ft overhangs → worst **68 %** (Sch 40), ridge ≈ ⅔ in,
  base ≈ 44 kip-ft / 8.3 kip shear / 8.4 kip uplift. Pipe purlins + eave beams: **8 in Sch 40 at ~5 ft**
  (38–49 %, ½ in sag); 6 in is too bouncy. Old results kept in `portal_frame_results-42ft-old.json`.
- Barn object `centro-equino-barn.py` → `.obj` (old one kept as `centro-equino-barn-76x42.obj`), name
  **`walker barn 72x40`**. `swap_barn.py` writes **`~/Downloads/centro-equino-final-2026-09-24.json`**
  (23b untouched). The barn sits **10 ft south** of the old centre on the same pad so the 40 ft north
  runs stay flat (graded z 1086.9–1088.0); earthwork unchanged. **Will's browser still holds the old
  barn:** open the 09-24 json in topo.html to load it.
- drain.py / pack.py / topo_pages.py / site_layers.py now read the 09-24 json and the new name.
- Pack **`~/Downloads/Centro-Equino-pack-11x17-2026-09-24-v4.pdf`**: p.13 plan (72 × 40 layout + roof
  and skylight plan: 6 panels 3½ × 10 ft over the aisle), p.14 structure (40 ft frame, gable entry,
  72 ft north wall), p.15 anchors (44 kip-ft, 15 of 27 kip per rod), p.16 spec (8 in pipe, 44 × 20 ft,
  skylights, gutters on both sides), p.2 and p.11 texts. **Not yet on Drive.**
- Laser `site_layers.py` rerun (19 sheets, barn on layer 26); old outputs in `laser/out-2026-09-23-76x42/`.
- Print parts `stable_parts.py`: new body (6 stalls, 4 south rooms, open gable entries), 6 runs of
  12 × 40, gable frames open over the entry. Also fixed the frames' missing top chord (a bug in the old version too).
- **Still old:** the renderings (page 1 cover, page 2 plan-view image, pages 8–10 views and their
  captions, which still say "sticks stacked like a bird's nest").

## 2. Structure work already done (older layout, reusable method)

- **Portal frame check** `projects/laser/portal_frame.py` (2D stiffness solver, ASD combos): 12¾ × 0.406
  pipe, 42 ft span, 12 ft eave, 17 ft ridge, frames at 24 ft → worst **75 %** of capacity (D + Lr),
  ridge ≈ ¾ in; base moment ≈ 50 kip-ft, shear ≈ 9 kip, uplift ≈ 8 kip. At 12 ft spacing ≈ 37 %.
  **Redo for 40 ft span / 72 ft length** when the layout is confirmed (change SPAN, add the 2 ft overhang).
- Rafters are 21.6 ft along the slope → one welded splice each (8 ft offcuts). Knees welded with
  haunches; ridge bolted with end plates so each half-frame lifts separately.
- **Anchors (pack p.15):** 4 × 1¼ in F1554 Gr 55 **headed** rods, 30 in embedment, 22 × 22 × 1¼ in
  plate, 4 gussets, oversize holes + plate washers, levelling nuts, 2 in grout. **No J-bolts.**
- Foundations: Ø 36 in × 9 ft piers, a tie beam across the aisle under each frame, a perimeter grade
  beam that the rock sits on. **Staged build:** frames + roof first (stable usable with pipe stall
  fronts), rock later, sticks last → **piers must hold the roof down without the rock's weight.**
- **Seismic:** Baja California is active. Tall stone must be reinforced; the new design (rock only to
  4.5 ft all round) removes the tall-facade problem.
- Will's other ideas on the table: big timbers from Andrés as eave beams/purlins (**sizes still
  needed**); pinning big rocks with rods set in epoxy (fine for the rocks; a ½ in rod is too slender
  to be the stick-wall post, so use 2 in pipe or 3 × ⅜ flat-bar verticals every ~4 ft).
- Every page says: feasibility only, a Mexican structural engineer (DRO / corresponsable) signs off.

## 3. The print pack (11 × 17, 18 pages, bilingual)

- Built by `projects/pack.py` (run from `projects/`; pulls helpers `drain.py`, `sheet1.py`, `sheet2.py`,
  `topo_pages.py`, `posts_page.py`, `structure_pages.py`, `geo.py`/`geo18.py`). **Verified 24 Sep that
  it builds from the repo alone.** It reads the drawing export
  `~/Downloads/centro-equino-final-2026-09-23b.json` and the paintings `~/Downloads/coyote-topo-painted-*`.
- Latest: `~/Downloads/Centro-Equino-pack-11x17-2026-09-24-v3.pdf`; Drive copy keeps the name
  `Centro-Equino-pack-11x17-2026-09-23.pdf` so shared links stay live.
- Walker's page order: 1 cover (the "winner", renders #70) · 2 plan view (#89 **fixed** by masked edit)
  · 3 existing topo (clean) · 4 grading plan · 5 operator grading sheet (50 ft A–Z/1–17 stake grid,
  cut/fill per stake, STAKE FIRST note) · 6 drainage · 7 sections · 8–10 other views (2 per page with
  captions) · 11 text + references · 12 inspirations (slots) · 13 stable plan · 14 structure (portal
  frames) · 15 base plate detail · 16 metal building spec (filled) · 17 logistics (slots) ·
  18 discussion (**Walker fills in the agreements**).
- PDF is ~36 MB: over Gmail's 25 MB and the phone-transfer limit; share by Drive link.

## 4. Site and topo drawing (see the 9/23 handoff for the step-by-step)

- Drawing lives in Will's browser (`localStorage['topo-session']`), plus exports:
  `~/Downloads/2026-09-23 Centro Equino topo drawing.json` (also in the Drive pack folder).
- Graded: roads (12 ft truck roads + 5 ft walking path), pads flat to their edges (barn 1087.6,
  paddocks 1082.5, arena 1073.3, round pen 1080.6, parking 1102.4 following the ground, trough apron
  1082.2), swales, infield basin, **natural water sink** at the track's SE end (no dug pond), 7 culvert
  marks, 12 gate bars, fences rebuilt with openings. The track side of the site is fully fenced as one
  turnout (cross fence closed at both ends 24 Sep, 4.6 acres). Earthwork ≈ 4,960 cut / 4,720 fill yd³,
  ±30–50 % on 30 m terrain.
- **Replay order that keeps pads flat:** reset → roads → pads → ditches → trough apron.
- **Photo trap:** Esri zoom 18 and 19 sit ~13 ft apart here; the app shows z18. Fit to z18.
- Objects: barn (old 76×42 + runs), stone trough 12 × 4 ft, watering station 10 ft round (filled),
  5 parked cars in the east strip, fences, paddocks with shade stalls.

## 5. Renderings

- ~45 paintings, all in `~/Downloads/coyote-topo-painted-*` and `Drive pack folder/renderings`.
  Gallery artifact: https://claude.ai/artifact/2M6bC7MXYVzZYgq9uUX3XR (updated through the model
  mash-ups; the 24 Sep repaints #80–89 are on Drive, not yet in the gallery).
- What works: gpt-image-2 (openai-2) holds the layout far better than Gemini. Give a top-view **barn
  reference diagram** (`projects/barn-topview-ref.png`) tagged "the building" or the barn comes out
  wrong. The grey model edge gets painted as a lake: frame it out. Low camera angles make the sky read
  as real.
- **Masked edit** fixes one spot without repainting: `/v1/images/edits` with a mask, then composite
  only the masked area back (use `destination-in`; `destination-out` inverts it). Used for #89.

## 6. Laser site model + 3D prints (`projects/laser/`)

- `site_layers.py`: 49 layers of 1/8 in board, 1 ft per layer, 1 in = 40 ft (5× vertical), fenced
  site + 20 ft, 28 × 15.3 × 6 in, hollow rings with ¾ in glue lips, 19 sheets at 32 × 18 in. Red cut,
  blue score (next-layer glue line + the design), green score (stake grid), black text (layer · elev).
  Most sheets are edge frames; splitting frames into strips would cut it to ~7–8 sheets (not done).
- `stable_parts.py`: 1:480 glue-up parts for a Prusa: open-top body with the stall layout inside,
  lift-off roof lid (2 flat panels + 4 flat trusses with locating tabs), north and south run fences.
  **Old 10-stall layout: rebuild for the new design.**
- `preview_sheets.py` renders the SVGs for checking. Outputs in `projects/laser/out/` and the Drive
  pack folder.

## 7. Shared with Walker

- Email **sent 23 Sep** (Will's Gmail, 23:55 UTC) "Centro Equino: the pack, the drawing, and how to work
  with Claude": pack PDF + folder links, archive folders, `WALKER-HOW-TO-WORK-WITH-CLAUDE.md` attached.
- Drive: `My Drive / MEXICO / Chichihaus / 2026-09-23 Centro Equino pack` (and the archive folders) are
  **anyone-with-the-link can view**, inherited from Chichihaus. The Drive connector cannot change
  sharing.
- Artifacts: water plan https://claude.ai/artifact/3aVtBDrvF5LAYf6XwhSamw (bilingual, D-1 and D-2), gallery
  above. Both private until Will shares.

## 8. Next steps, in order

1. Confirm the open points in §1 (layout, roof colour, barn location, timber sizes).
2. Rebuild the barn to the new design everywhere: topo object, pack pages, renderings, laser outline,
   print parts; rerun `portal_frame.py` for the real span and the 2 ft overhang.
3. Draw the skylight layout and the stick-wall detail (verticals, fixing, spacing) for the pack.
4. Walker fills in the agreements page; add inspirations, logistics and the metal-building supplier's
   drawings when they exist.

## 9. Watershed correction (24 Sep, late)

The "about 10 acres at the road bend" figure came from the 400 m sheet, which cuts the hill off at its
south edge. Zoomed out to 1,600 m, about **15.6 acres (6.3 ha)** of hill drains into the lot; the 400 m
sheet shows ~7.7. At 30 m resolution the flow at any single crossing is not reliable (the water arrives
along the whole south fence as ~8 small flows), so the crossings are now sized for the full watershed:
- Drainage note 1 (drain.py): road-bend crossing "up to about 16 acres"; rock-lined ford preferred, or
  a **30 in** culvert (was 24 in). Note 5: the west spreader is sized for the full watershed.
- Note 3's English heading shortened to "Natural sink at the track end" (it ran 5 pt off the page).
- Pack rebuilt: `~/Downloads/Centro-Equino-pack-11x17-2026-09-24-v5.pdf`; copied over the Drive file `Centro-Equino-pack-11x17-2026-09-23.pdf` (same name, so shared links stay live). Drive had been holding v3.
- Water plan artifact republished (v3): new lede, watershed fact, the pond replaced by the natural low
  spot, the new D-1 sheet.
- Method: `coyote-studio/lessons/workflow.html` step 2. Zoom out BEFORE grading.

## 10. Covered stalls moved (26 Sep, Lenovo session)

- The 9/24 swap json on the Surface Book's Downloads is gone; the Drive copy `2026-09-23 Centro Equino topo
  drawing.json` already carries `walker barn 72x40`, so it IS the latest. Working copies now live in
  `projects/` (`centro-equino-2026-09-26.json` = that + Will's yellow KML line as an ember sketch).
- Walker's brief: 16 stalls 16 x 20 ft (8 a side), 12 ft corridor, one roof over the corridor overhanging
  8 ft onto each stall front (back 12 ft of each stall open, palms may stay there), minimal grading.
- `projects/covered_stalls.py` → `covered-stalls-16.obj` (128 x 52 ft, roof 28 x 132 ft, eave 9, ridge 13),
  grading (corridor on the ground's own line ~1089.3, level across; stall floors ≤5 % from the corridor;
  3:1 to the ground), a ditch 6 ft above the uphill row falling 1 % SW then turning downhill round the SW
  end (records.ditches ×2), and `paddocks.py --no-shelters` → the four paddocks lose their shelters.
  Output `projects/centro-equino-2026-09-26-stalls16.json` (+ Drive pack folder copy). This change:
  ≈260 yd³ cut / 150 fill on the 8.8 ft grid. Clear of main road 18 ft, round pen road 34, scrub road 29.
- Block sits 14 ft past the yellow line's open SW end (`python covered_stalls.py <T0>` slides it).
- Open this locally: serve coyote-studio and open `topo.html?proj=projects/centro-equino-2026-09-26-stalls16.json`.
- Not yet: pack pages / laser / print parts / renders for the stalls; palm positions only from the old Esri z18
  photo (`stalls_0926.py` has the palm mask + A/B roof sketch).
- **Paddock pad undone (option, 26 Sep):** `projects/undo_paddock_pad.py` → `centro-equino-2026-09-26-stalls16-nopad.json`:
  ground back to existing under the four paddocks, then the 3 roads and 3 ditches crossing it re-run (roads then
  ditches). Site earthwork ≈5,200/4,900 → ≈3,300/3,100 yd³. Paddocks then sit on 8–11 % median slope (Will had
  asked for them "on flat ground" on 9/22 — decision pending). The natural sink is untouched.
- **Field check:** Walker confirmed the low spot below the track exactly where the analysis put the natural water sink.
- **Decided 26 Sep (Will):** paddocks REMOVED (fence object + 4 paddock gates) and their pad undone; Will's yellow sketch
  line removed; waterers at the new stalls = 8 (one per pair, in the divider at the corridor edge) on a 6 ft level strip
  at every stall front (`FLAT` in covered_stalls.py). Chain: `covered_stalls.py` → `undo_paddock_pad.py` →
  `centro-equino-2026-09-26-stalls16-nopad.json` = THE current drawing (Drive: `2026-09-26 Centro Equino topo drawing,
  16 covered stalls.json`). Site earthwork ≈3,350 cut / 3,110 fill yd³. The "paddocks to cross-fence gate" road and the
  paddock swale : Will kept the swale, then REMOVED the road (`remove_road.py`, ground restored, its culvert mark gone); the cross-fence gate stays because people will still walk that way. Chain is now covered_stalls.py → undo_paddock_pad.py → remove_road.py; re-dug ditches sample natural ground, never their own dug bottom. Site ≈3,340 cut / 3,110 fill yd³.
- Also removed 26 Sep: **road between track and paddocks** (`remove_road.py "road between track and paddocks"`, then
  `fix_junction.py "road between track and paddocks" "west road, gate to gate"` to clear its 6 ft ramp at the west
  road and re-run the west road there) + its culvert mark. The 2–3 ft fill left along the track's south edge is the
  track's own. Full chain: covered_stalls.py → undo_paddock_pad.py → remove_road.py (×2 roads) → fix_junction.py.
  Site ≈3,290 cut / 2,800 fill yd³.
- **Butterfly roof on the covered stalls (26 Sep, Will):** both planes fall ~2:12 to a valley gutter over the corridor;
  valley 11.5 ft at the NE end falling 1 % to 10.2 ft at the SW end (10 ft+ clear over the corridor); outer eaves 2.5 ft
  higher (14 ft NE / 12.7 SW); a leader runs 8 ft past the SW end and drops into the ditch outlet. `VALLEY_NE, FALL, RISE`
  in covered_stalls.py; rerun the whole chain after any change there.
- **Round trough at the SW end (26 Sep, Will):** 8 ft across, 2 ft tall, on the corridor's centre line with 10 ft clear
  between it and the building end and all round (`TROUGH_D, TROUGH_H, GAP`). No downspout: the valley gutter carries
  on as an open chute (2 % fall, one slim post past the far rim) and pours into it. Level apron 6 ft past the rim at
  ~1089.1 ft. Overflow = buried pipe (blue dashed stroke `stalls trough overflow pipe`) to the stalls' ditch outlet,
  which now runs 10 ft past the trough and ends IN the `ditch above the barn road`, so roof water, overflow and hill
  water join the water plan. No road within 60 ft of the trough. Site ≈3,320 cut / 2,800 fill yd³.
- **Trough revised (Will: the chute post read as a downspout):** no post. The chute cantilevers 7 ft past the roof end
  (`CHUTE`) and pours 2 ft inside the near rim; the trough moved in to 7 ft from the building end (`END_GAP`, a
  walk-through), open sides stay clear. An assert stops the build if the chute would not end over the trough.
- **Stalls 16 x 30 ft, roof lower + flatter (26 Sep, Will):** building now 128 x 72 ft (S0 = -8, grows 10 ft each side;
  the extra is open sky). Roof ~1:12 (eaves 1.25 ft above the valley), valley 10.7 ft NE -> 10.0 ft SW at 0.5 %, top
  ~12 ft (was 14). Open stall backs may fall up to 8 %, covered fronts 5 %. Clear of round pen road 24 ft, scrub-side
  road 19 ft, main road 18 ft. Site ≈3,420 cut / 2,860 fill yd³. 1:12 needs standing-seam or a low-slope panel.
- Stray pen line removed (26 Sep): unnamed thin ink stroke (94.0, 62.2) -> (97.8, 57.3) across the main road by the barn
  circle, deleted from the 09-26 source and both outputs, so a chain rerun will not bring it back.

## 11. Pack v6, water check, money shots (26 Sep, in progress)

- `drain.py` reads `projects/centro-equino-2026-09-26-stalls16-nopad.json` and RECOMPUTES flow with `projects/flow.py`
  (priority flood + D8; matches the app's own `__flow` on 99.8 % of cells). The export's `__flow` is stale after any
  outside-the-app grading. D-1 now has note 11 (covered stalls: roof ≈2,300 gal/in, trough ≈500 gal, ditch +
  overflow to the barn-road ditch), note 3 (sink: Walker confirmed on site; now ≈0.9 ac, fills at ≈½ in), note 6
  counts culverts (5). D-2 section A = across the covered stalls.
- Water check 26 Sep (site grid, before → after): sink 0.64 → 0.89 ac; barn-road ditch 0.23 → 0.48 ac (capacity
  ≈14 cfs vs ≈0.5 cfs); main waterway leg 1 0.20 → 1.08 ac; crossings were already sized for the 16 ac watershed.
  Earthwork 3,420 cut / 2,860 fill: ≈560 yd³ surplus.
- Water plan artifact republished (v4) with the new D-1/D-2, facts and a "what changed" list; its 4 view paintings
  are still the old ones (captioned as such).
- Pack: `pack.py` now writes `Centro-Equino-pack-11x17-2026-09-26-v6.pdf` straight into the Drive pack folder;
  new page 14 `stalls_page.py` (plan, butterfly section, specs); PADS, texts, operator sheet updated. Renderings
  missing on disk show as grey placeholder frames: v6 on Drive is a DRAFT until the new money shots exist.
  The shared `Centro-Equino-pack-11x17-2026-09-23.pdf` on Drive is untouched.
- Money shots: `projects/renders/shoot.mjs` (headless Playwright from the global @playwright/cli, needs the
  8791 server) saves golden-hour cumulus control views of 6 walk/drone cameras to `renders/ctl/`; `paint.py
  [openai|google] [medium|high]` paints them. BLOCKED 26 Sep: OPENAI_API_KEY / GEMINI_API_KEY are not on the
  Lenovo and not in the SECRETS backups (those predate 9/11); Will to copy them from the Surface Book.
- Then: new gallery artifact, swap renders into pack pages 1, 2, 8–10, rebuild v6, email Walker (draft first).
- **DONE 26 Sep (late):** keys now on the Lenovo (OPENAI_API_KEY user scope; Will's key notes live in
  `G:\My Drive\Claude Private\SECRETS\note_PAD\`). 7 paintings (gpt-image-2 high) in the Drive pack folder
  `renderings/2026-09-26 money shots` (all attempts + control views kept). Gallery artifact
  https://claude.ai/artifact/H6EbuHWHiV7kMkznEuRF6W (private). Pack v6 final (cover = site from NE, p.2 = plan
  painting, pp.8–10 new views, p.14 covered stalls) copied over the shared `-2026-09-23.pdf` (same link).
  Email "Centro Equino: grading plan updated with the covered stalls" SENT to onestronghive@gmail.com
  2026-09-27 05:18 UTC from Will's Gmail, on his "send". Known render liberties: stable roof silver, not sky blue.

## 12. Scaled back to 8 stalls (27 Sep, Will)
- `covered_stalls.py`: PER_SIDE 4 + one NE bay (NB = 5), 80 x 72 ft, the NE (stable) end fixed at t = 114 (18 ft
  off the main road), so the block shrank from the SW. NE bay uphill = closed alfalfa room 16 x 30 (walls 10 ft,
  10 ft door on the corridor, own shed roof); NE bay downhill = open covered tie-up. Roof OVER 12 ft (36 ft wide,
  84 long), RISE .75 = 1/2:12 (standing-seam minimum), valley 10.7 -> 10.3 ft. Object is now `covered stalls`
  (`covered-stalls.obj`); drain/pack/topo_pages match by that name. Roof water ≈1,900 gal/in.
- Rebuilt chain (the same five commands) -> site ≈3,270 cut / 2,760 fill yd³. Pack v7 `...-2026-09-27-v7.pdf` in
  the Drive pack folder; the shared `-2026-09-23.pdf` still holds v6 (16 stalls) until the paintings are redone.
  Drive drawing `2026-09-27 Centro Equino topo drawing, 8 covered stalls.json`. Water plan artifact v5.
- The 26 Sep paintings + gallery still show 16 stalls; `renders/shoot.mjs` + `paint.py` redo them.
- **Repainted 27 Sep** (cameras 1 and 2 re-aimed at the moved block; brief now says 8 stalls + alfalfa room, near-flat
  roof): Drive `renderings/2026-09-27 money shots (8 stalls)` (all attempts + control views). Pack v8
  `...-2026-09-27-v8.pdf` (cover 3-site-ne-3, plan 7-plan-4 cropped, pp.8-10) copied over the shared
  `-2026-09-23.pdf`. Gallery artifact v2 and water plan artifact v6 (new views) republished. Known liberties: in
  5-corridor-out the trough sits inside the corridor and the alfalfa room is stone, not metal.

## 13. Stalls 16 x 20, alfalfa under the same roof, strict render brief (27 Sep, Will)
- Stalls back to Walker's 16 x 20 (STALL_D 20, S0 2) -> 80 x 52 ft; roof unchanged (84 x 36, 1/2:12, 12 ft over each
  stall). The NE end bay is the ALFALFA BAY under the same butterfly roof, full roofed width 16 x 36: pipe panels on
  three sides, 12 ft gate on the road end; it closes the corridor's NE end. No separate structure (the old shed roof
  was the "notch" Will saw). Clearances 18 / 34 / 29 ft. Site ≈3,190 cut / 2,710 fill yd³.
- Paintings drifted from the model (Will): `paint.py` SCENE is now a STRICT one-to-one brief (same count, outline,
  position, size, orientation, roof shape; add nothing, remove nothing; terrain silhouette kept; no palms, they aren't
  modelled). `FIXES` dict appends a per-view correction for a repaint. Camera 5 moved to the new corridor end (89.6,
  64.2). Method: after each round, pair every painting with its control view and repaint the ones that drift.
- Drive `renderings/2026-09-27 money shots v2 (8 stalls 16x20)`; pack v9 copied over the shared `-2026-09-23.pdf`;
  gallery v3, water plan v7. Known liberty: 5-corridor-out-5 has an extra stock tank in the foreground.
- Walker sent a 3D viewer artifact (https://claude.ai/artifact/7dHdStVCWd2rjz3UW1ezXq, hers); Will wants it rebuilt
  with this work + her renderings. Reading it needs Will's yes in-session.

## 14. Stable redesign + 3D viewer (27 Sep, Will + Walker's ChatGPT image)
- Walker's image `projects/renders/ref/stable-walker-2026-09-27.png` (Drive: `renderings/stable reference from Walker
  2026-09-27.png`). Will: keep the 24 Sep FLOOR PLAN (6 stalls + runs north, wash/tack/feed/alfalfa south — her
  "4 south doors" are those rooms); DECIDED from the image: clerestory roof, woven sticks, low rock wall all round.
  Roof colour taken as dark charcoal from the image (24 Sep had sky blue): confirm with Will.
- `centro-equino-barn.py`: clerestory monitor 60 x 10 ft (2.5 ft glazing, mullions, own roof), woven near-vertical
  sticks (0.22 ft at 0.5 ft, alternating, three battens) on long walls and gables. Old model kept as
  `centro-equino-barn-2026-09-24.{py,obj}`. `swap_stable.py` swaps it into all three drawings in place.
- `paint.py`: STABLE_REF (her image as a jpg) goes to the painter as the last reference with STABLE_NOTE (take only
  the building); FIXES for 3-site-ne and 7-plan. Set v3 in Drive `2026-09-27 money shots v3 (new stable)`.
- Pack v10 (cover = 6-west-5): stable texts, roof inset (clerestory), structure elevation strip, spec row
  (Claraboya) updated. NOT yet: the frame cross-section on the structure page still draws no monitor.
- 3D viewer artifact https://claude.ai/artifact/NiKaQ9hYfGgu5UATQGEPzh — source `projects/viewer/` (`export.py` ->
  data.json + aerial.jpg; `index.html`, three r128 + OrbitControls). Wheel zooms to the cursor (raycast, caught on
  the parent in capture), middle/right drag pans, R hides roofs, sun slider 27 Sep solar time.

## 15. Stakes horizontal, stall roof 1:12, fences re-seated (27 Sep, Will)
- Stable walls back to HORIZONTAL tomato stakes, bird's-nest (loose courses 0.12 ft at 0.3 ft, jittered, on light
  verticals every 4 ft); clerestory kept. Walker's image stays the painter's building reference but STABLE_NOTE says
  the sticks run horizontal, not vertical as in her image.
- Stall roof RISE 1.5 = 1:12 (1/2:12 was too flat). Eaves ≈11.8–12.2 ft, valley 10.3–10.7 ft.
- The site and cross fences were buried up to 2 m (draped before the regrading): `redrape_fences.py` re-seats each
  vertex on today's ground by its height above the local post foot. Now visible in the app, the viewer and paintings.
- NEW CHAIN ORDER: covered_stalls.py -> undo_paddock_pad.py -> remove_road.py (x2) -> fix_junction.py ->
  swap_stable.py (places centro-equino-barn.obj at stable_origin.json) -> redrape_fences.py.
- Set v4 in Drive `2026-09-27 money shots v4 (stakes, 1-12 roof, fence)`; pack v11 (cover 3-site-ne-7) behind the
  shared link; viewer v3, gallery v5, water plan v9. Liberty: the painter copies Walker's stone trough near the stalls.

## 16. Stable stalls both sides, model renders + light AI finish, phone viewer, gates (27 Sep, Will)
- Stable SOUTH = 4 stalls + tack/feed + wash (east end); runs 12 x 40 off all 10 stalls; south runs climb 5 %
  (`stable_runs_grade.py`, vertical rock-wall edge, max ~2 ft). Alfalfa lives only at the covered stalls.
- Both obj builders tag faces with `usemtl` (stable: rock/stakes/steel/roof/glass/wood/fence; stalls: panel/steel/roof/
  hay/galv/water); topo.html ignores it, `viewer/export.py` splits parts by it. Stall panels are posts + 4 rails now.
  Stall valley gutter is dark steel (the light one read as a slot of sky = the "notch").
- Arena and round-pen fence openings were at arbitrary stations: `pipe-fence.py` now opens them at the drawing's gate
  marks; `swap_fences.py` (+ `fence_origins.json`, `objtools.py`) places them.
- CHAIN: covered_stalls -> undo_paddock_pad -> remove_road (x2) -> fix_junction -> swap_stable -> swap_fences ->
  stable_runs_grade -> redrape_fences; then viewer/export.py.
- RENDERS NOW COME FROM THE MODEL (Will chose "model render + light AI finish"): `renders/modelshots.mjs` renders the
  viewer (window.__shot, 8 cameras incl. 8-stable) -> `renders/model/`; `renders/finish.py` (gpt-image-2 high, strict
  "keep everything, only materials/light/sky") -> `renders/finished/`. Drive: `2026-09-27 renders from the model`.
  The old AI-painting path (shoot.mjs/paint.py) stays but drifted too much for Will.
- Viewer v4: materials (canvas textures, planar UVs), phone layout (bottom sheet with a drag handle: tab / toolbar /
  full, tap cycles), wheel zoom-to-cursor, middle-drag pan. Pack v12 behind the shared link; gallery v6; water plan v10.

## 17. 28 Sep – 3 Oct: gallery site, stable on a 12 ft grid, bleachers, trough, pack v13, elevations (READ THIS FIRST)

**Where things live now**
- **Presentation page (public):** https://will.100xbtr.com/equino/pack/ — the pack page by page (`will-os/equino/pack/p01..pNN.jpg` + `pages.json`, written by `pack.py` on every build), buttons to the 3D model, the gallery and the Drive PDF (file id 1YcIsLYivRXHzFMVM4jPr0YHusk0_iR1d = the shared `-2026-09-23.pdf`). Push will-os after a pack build to publish. Pack v21 (4 Oct): 18 pages, logistics page dropped.
- **Gallery (public, no sign-in):** https://will.100xbtr.com/equino/ — repo `WebDev/will-os/equino/` (push main = deploy). Picks/notes/★finalists saved in Netlify Blobs via `will-os/netlify/edge-functions/equino-picks.js` (GET/POST `/equino/api/picks`, fields gone/note/star/by). `img/<view>-<tag>.jpg`; tags: openai, google, model, fresh (Gemini 28 Sep), freshoa, picnic, raw (no-AI). "★ Finalists only" mode hides everything else. Read notes: `curl https://will.100xbtr.com/equino/api/picks`.
- **3D viewer (public):** https://will.100xbtr.com/equino/model/ — copy of scratchpad viewer (`projects/viewer/index.html` + `export.py`); after every model change: `cd projects/viewer && python export.py <outdir>` → copy `data.json` to `will-os/equino/model/` and push. Site copy of index.html has an extra "Galería de renders" link line under the lede.
- **Topo app with connect AI:** https://will.100xbtr.com/equino/topo/topo.html (current coyote-studio topo.html copied 3 Oct). coyotemountainfarm.com is NOT down — Will's home router was blocking it (3 Oct); the /equino/topo copy is a stopgap until he restarts the router. Connector code **BVQKW4N4Y3**: set `localStorage['coyote-ai-code']='BVQKW4N4Y3'`, reload, load project via the hidden file input (`find` → ref, `file_upload`), switch on in `#u2aiPop`. Then the claude.ai topo MCP tools (get_state, screenshot, set_view, open_tool…) drive Will's tab. Read Will's tab project: override `URL.createObjectURL` + click `#saveProj` (see 3 Oct transcript). Objects move with SHAPE → object (select only picks strokes).
- **Drawings:** `projects/centro-equino-2026-09-26*.json` (nopad = current). Rebuild chain now: `for f in _bak_0928/*.json; do cp $f .; done; python site_extras.py; python bleachers.py` (backups in `_bak_0928/` carry the current stable/stalls; after `swap_stable.py` or a stalls rebuild, copy the new stroke into `_bak_0928` too — snippet in transcript).
- **Paintings:** `renders/gallery3.py` (one strict BRIEF + BLOCK3 + PICNIC + per-view EXTRA; `python gallery3.py google|openai <views>`), `renders/elevations.py` (eye-level, site photo refs `site-ref-0576/0577.jpg` from Drive `Chichihaus/Site photos`), `renders/cover_paint.py`. Model shots: `node renders/modelshots.mjs http://127.0.0.1:8792/index.html model <ids>` (serve scratchpad/viewer on 8792). Gemini is better at positions; OpenAI better at geometry detail. Gemini sometimes doubles floating blocks.

**Design state (all in the model)**
- **Stable 72 x 42 on a 12 ft grid**, steel trusses every 12 ft on 6 in pipe posts; 5 ft tan rock + black pipe floating to 6 ft; above, 3 ft steel-framed panels of horizontal sticks cut to ONE common length (walls, gable bays, **sliding doors**, **gable triangles above the end trusses** — 3 Oct). Open clerestory (no glass). 10 stalls 12x14 with **rock partitions**, pipe fronts + gates, open 6x9 doorways to 12x40 runs (6 N, 4 S at the east end). **Wash room at the west (road) corner** with its 6x9 outside door, tack next to it, both plastered, concrete floors; 12x24 concrete pad on the south wall. Tan dirt floor. Pad cut level under the whole footprint (+2 ft). Labels "Lavado/Monturas" in the viewer.
- **Covered stalls:** 8 stalls 16x20, butterfly roof, round stone trough under the chute end. **3 Oct (Walker): corridor runs straight through; alfalfa split both sides behind panels, bay 24 ft long** (building now 88 ft); pad levelled under it.
- **Stone trough:** 44 ft, one level, retaining wall (stable side held at the rim), **centred on the stable 57 ft off the west gable, running N–S** (Will placed it in the app 3 Oct). Roof-water pipe from stable SW corner.
- **Barn road:** one smooth Bezier from ~120 ft out into the west entry; ground under it smoothed (no trough hump).
- **Bleachers:** Walker's sketch — 6 ft deck along the 40 ft trailer + 3 curved "blade" platforms (pinwheel), largest highest; may cross the arena walking path; trailer+bleachers moved 3 ft back (2 ft clear of the main road); **trailer sign removed**.
- Small round-pine grove (30 trees) between stable and parking; all fences black.

**Pack:** v13 in Drive pack folder (`pack.py` → `Centro-Equino-pack-11x17-2026-09-28-v13.pdf`), finalists in `renderings/2026-09-28 finalists/`, stable pages from `stable_pages_0928.py` (plan + truss page), earthwork 3,243 cut / 2,720 fill. Cover = original 3-site-ne (Will's choice after much back-and-forth). **Walker made v14** (`Centro-Equino-pack-11x17-2026-10-02-v14.pdf`, 18 pages, "Giant Nature" branding, horse-photo cover) — Drive file id `1k1IjiPGQQoPBAUi1q189TnQNkTjV2Q94` (Drive metadata says owner onestronghive; Will says he owns it). Not on G: mount. It is open in Chrome; page capture via JS timed out — next session: download it (Drive connector is 14 MB, too big inline) or have Will drop it in the Drive pack folder, then preview/compare with v13.

**Open / next**
1. Preview Walker's v14 for Will and fold her changes into `pack.py` (she is the editor now — ask whether she keeps editing her file or we regenerate).
2. Elevations: straight-on cameras done (`el-north/south/west/east` in modelshots.mjs, north eye 9 ft above floor, east framed by two pines); **repainted 3 Oct with the stick doors/new trough — results in `renders/elevations/` not yet reviewed or delivered** (previous set in `elevations/prev/`, Drive `renderings/2026-10-03 stable elevations (eye level)/`).
3. Model changes since the last gallery repaint (stick doors/gables, trough, road, hallway stalls) — gallery paintings are stale.
4. Will may still redraw the road (asked him to sketch it with the pen; read strokes from his tab).
5. coyotemountainfarm.com: fine; Will's router was blocking it (restart pending).

## 18. 3 Oct (afternoon): elevations gallery, Walker's v14 folded into pack.py → v15 (READ THIS FIRST)
### 4 Oct (line work): drawings redrawn as line drawings · pack v32
- Will: 'less or no fills, more diagrammatic, wiggly sticks in frames drawn as in real life, mostly line work'. NEW `linework.py` (exec'd by `stable_elevations.py` and `stable_pages_0928.py`): `lw_sticks` (outline=True at large scale = paper-filled tapering sticks that overlap like a real bundle, occasional knot; single wavy lines at small scale), `lw_stones` (site stone like the tabular slabs stacked on site, photo 7-0: rough rectangles, chipped corners, uneven edges, big at the bottom and smaller up, some gaps), `lw_planks`, `lw_ground` (hatched), `lw_pipe`, `lw_vine`. Openings are paper-backed so they cut cleanly.
- Redrawn: both stable elevations (p3) and the structure page's truss section + two-bay elevation (p4). The two-bay doorway is now OPEN (the stick frames start above the 9 ft lintel; before, sticks were drawn across it). The plan itself still has light tone fills.
- `_preview_lw.py plan|truss <out.png> [dpi]` renders one of those pages without the whole pack (fast iteration).

### 4 Oct (latest): stable elevations, click-to-enlarge renderings · pack v31
- **Stable page (p3):** NEW `stable_elevations.py` (exec'd at the top of `stable_pages_0928.py`, called from `barn_plan()`): east elevation (top, looking west: gable with stick panels, 14 ft aisle with both sliding leaves parked open, clerestory end-on, north runs + the 32 ft trough) and south elevation (below, looking north: rock + pipe, cob-plastered wash/tack rooms, wash opening + parked door, stall doorways, roof plane + clerestory, pad, trellis with grapes, pad trough, run fence in front). Titles are fig.text above each. The plan's 'camino road' label was removed (duplicated the orientation line).
- **Web enlarge per image:** pack.py export now writes `will-os/equino/pack/zoom/pNN-i.jpg` (crops of the PDF at up to 2600 px) and `pages.json` `hot` = per-page hotspots (fractions). Hotspots = every photo placed from `renders/` (+ the cover) and every drawing axes >= 1.2 % of the page on the pages in `ZOOMPG` (stable plan, structure, covered stalls, plan view). Material and inspiration photos do NOT enlarge (Will). Click a hotspot -> that image fills the screen; click elsewhere on a page -> the whole page; click or Esc -> back.

### 4 Oct (late night): trough on the run fence, trellis, tie-ups, walking path, plan snap, lightbox, type pass · pack v30
- **East trough (final):** `site_extras.py` builds `east trough` 32 x 3.5 ft fieldstone just OUTSIDE the north-east run's east fence (stable frame x 37.0..40.5, y 25..57), apron only outside the fence (never regrades the run). The stable roof splits: SOUTH half -> SW downspout -> cistern C1 -> long trough + pad trough; NORTH half -> NE downspout -> east trough. D-1 note 8, D-3 notes 2 and 4, pack summary 'Agua', `walker_pages` water paragraph, `sheet2` note B, viewer schedule and stable mini-plan all say so. Verifier confirmed the geometry clears posts, rails and the drip line.
- **Wash pad trellis (Walker via Will):** `centro-equino-barn.py` after the pad: 4 in posts at the pad's south edge (x -35.5, -24, -12.5), 3 in south beam and wall ledger at TR_H 10.3 ft (clears the sliding-door track at 9.9), 2 in cross pipes every 3 ft, three wires, a grapevine canopy of loose `sage` boxes. Stable plan page draws the outline, posts and 'pérgola de tubo con parra'.
- **Tie-ups (Will approved sketch v2, `tieup_sketch2.py`):** the sliding door parks east of the opening, so nothing ties to that wall. W = one ring at 6 ft on the SW corner post (no tail tie); M = 3 in pipe hoop bent like an upside-down C on x = -24, 8 ft long, 4.5 ft high, 12 in bends, legs 3 ft in concrete, 2 ft off the wall so the door passes behind, rings at 3.5 ft and top centre; E = rings at 5 ft on the first two posts of run 1's west fence (x = -12). `tie_ring()` helper in the barn script. Plan page shows the hoop and the five rings.
- **Walking path:** `site_extras.py` re-routes 'walking path, parking to barn' as a Hermite curve from its old parking end, with a soft double bend (7 ft amplitude, flat at both ends), onto the stable's centre line 30 ft out and straight to the east doors (x 38.5). Pines keep 8 ft off the new line (`WALK = WALK_NEW`), so a tree moved.
- **Viewer plan view:** `PLAN_UP = [0, -1]` (site grid top up, square to the screen); the plan button now SNAPS (a fly-to into a straight-down camera rolled the whole plan ~70 deg on its last frame, verifier-confirmed); the pressed button updates in the snap path. Viewer opens with contours on, labels off.
- **Pack page lightbox** (`will-os/equino/pack/index.html`): click a page -> nearly full screen with the caption under it; click again or Esc -> back to the same scroll spot (only re-scrolls if you stepped pages with the arrows); touch panning blocked while open.
- **Type pass (Will: 'variable text range to match the page layouts'):** one typeface across the pack now, `plt.rcParams['font.family'] = ['Plus Jakarta Sans', 'DejaVu Sans']` after walker_pages loads (DejaVu only fills missing glyphs). Drawing-page titles 24/14 -> 30/17. Tiers from a page-by-page review: generous pages up (text refs 10.5, existing/grading 10.5 body + 9.5 tables, truss specs 10, plan-view notes 9, sections 9.5, operator 9 / 8.5, renders captions 13.5, stable plan specs 8.5, plan labels >= 6.5); dense sheets only lifted a little (stalls 7.4; D-1 and D-3 notes stay 6.3 but wrap 102 because PJS is narrower). Pages 18-19 were not reviewed (credits ran out mid-run).
- **Pack order:** operator sheet -> grading sections -> drainage -> irrigation (Will). Site views: slot 4-2 cropped so the NW block matches the SW one in size.
- **Verifier notes still open:** D-3 trough volumes are now inside measure (walls .7, water 1.25 ft); the stable plan's dashed roof outline still stops at the gables (model has 2 ft gable overhangs); the plan sheet now has a true north arrow (24 deg east of the stable axis).

### 4 Oct (night): east trough (option B), irrigation sheet D-3, swing doors, tie-up sketch · pack v29
- **Third trough — SUPERSEDED the same night, see the next section:** option B (20 x 3.5 at the east gable, 30 ft out) was built, then Will moved it to the outside of the north-east run fence (32 x 3.5).
- **Irrigation and water plan = NEW sheet D-3** `irrigation.py` (exec's drain.py like sheet1; `sheet('irrigation.py',…)` in pack.py after the grading sections). Content: 2 in HDPE main from an ASSUMED vineyard tap at the NE gate along the main road (530 ft), 1.5 in branch along the barn road, drip branch to the track infield; cisterns C1 40 m³ under the long trough's side (stable roof 3,496 ft² = 2,178 gal/in, ≈24,000 gal/yr at 11 in) and C2 30 m³ at the stalls' SW end (2,063 gal/in); all four troughs recirculating (weir → grated sump → small pump → far end; float make-up from the cistern; detail inset); zones Z1 entry natives, Z2 pine grove, Z3 old-nursery trees inside the track (the site was a rented vivero for years, Will), Z4 stall palms, Z5 picnic shade, Z6 parking shade; water budget (22 horses × 10 gal/day ≈ 1,540 gal/wk is the real load; cisterns ≈ 5 weeks of everything); Vision paragraph (vivero + café + wine tasting + children + animals). Numbers are design assumptions, flagged on the sheet; the vineyard tap point/pressure is to confirm with the ranch.
- **Wooden swing doors (Will):** `centro-equino-barn.py` `swing_door()` puts a 7-board plank leaf with 3 ledges and 2 strap hinges in each SOLID room's aisle door hole (TACK_DOOR 4 x 8), hinged on the gable-side jamb. Shown CLOSED in the wall plane so the plank face reads from the aisle (an open leaf hid inside the room in 10-stable-aisle). They are swing doors, not sliders: angle is `a_` in the loop if Will wants them ajar.
- **Tie-up / cross-tie / farrier bay:** `tieup_sketch.py` → sketch sent to Will 4 Oct (nothing placed). Option A recommended: rings at 6 ft on the three 6 in wall posts (-36, -24, -12) giving two cross-tie bays (wet bay by the door, farrier bay in front of the tack room with +4 ft of slab and mats edge to edge), plus a heavy hitching rail (3 in pipe at 42 in on 4 in posts 3 ft in concrete, rings at 5.5 ft) at the pad's south edge. Option B = free-standing steel frame on the pad facing the trough. Best practice gathered: anchors 10–12 ft apart, rings at withers + 6 in, quick-release at the wall end + breakaway; farrier wants level, dry, non-slip, 12 x 16–18, side light, room behind for a stretched hind leg. **Waiting on Will's choice.**
- Viewer side panel (both copies): rows for the east trough and the cisterns; earthwork now **3,598 cut / 2,846 fill yd³** (east-trough apron). Pack v29 = v28 + D-3 after the grading sections (19 pages).

### 4 Oct (evening): road gully, 2 ft gable overhangs · pack v28
- **Gully above the scrub-side road (Will, talked over with the owner):** NEW `road_gully.py` carves two interceptor ditches into the three `_bak_0928` chain inputs, 15 ft off the road centre on the hill side (6 ft past the 16 ft road edge), bottom = 3 m-smoothed ground - 1 ft forced monotone-falling, 2 ft bottom, 2:1 sides. East leg 640 ft from the road's east end into crossing 1 (the main-waterway culvert inlet); west leg 450 ft from 12 ft past the bend to a NEW crossing at the SW corner (grid x 27.5, stroke `culvert · road gully, west leg under existing scrub-side road`), inside the fence the ground runs down the west fence to spreader 5. Records `road gully, east leg…` / `…west leg…`. Deepest cut 2.5 ft (terrain bump at ~620 ft). Idempotent; rerun after any chain reset. **Earthwork 3,344 → 3,608 cut / 2,844 fill yd³** (viewer side panels updated, both copies).
- `drain.py`: note 12 + callout (104,74.5); NCULV auto-counts 6 crossings now. `sheet1.py`: notes column tightened (fs 6.3, wrap 92, step .0101) so 12 notes clear the earthwork block; sheet dated 4 oct 2026. Encoding trap: edit drain.py with Python (utf-8), sed mangles the backslash escapes.
- **Stable roof overhang 2 ft all round (Will):** `GOH = 2.0` in `centro-equino-barn.py`; roof sheets to ±(HL+GOH), purlins extended to carry it (long sides already OH = 2). Backup of the purlin-fix obj kept; chain rerun, viewer exported.
- Walker's overnight pushes (v24–v27: white/off-white pages, greener aerial, NW model view, arrow keys on the pack page) were pulled before any of this; always `git pull` both repos first now.

### 4 Oct (later): stable purlins seated on the top chords
- Will: the long tubes under the roofing floated above the trusses and looked hexagonal. `centro-equino-barn.py`: `top = .5/2 + PURL_D/2` (was `COL_D/2 + PURL_D/2`, COL_D = the retired 12 in pipe rafter, a 3 in gap); purlins + eave beams 16-sided, top chords 12-sided. Roof sheets and clerestory hang off `zr = top + PURL_D/2`, so they came down with the purlins (height 20.7 ft). Tubes kept (reuse the ranch's pipe), not rectangular tube.
- Chain run: barn.py -> swap_stable.py -> stable stroke synced into _bak_0928 (inline json copy of 'walker barn 72x40') -> cp _bak -> site_extras -> bleachers -> viewer/export.py -> will-os data.json. No ground change, earthwork unchanged. Backup `centro-equino-barn-2026-10-04-pre-purlin-fix.obj`. Pack not rebuilt (its stable pages are AI paintings + stable_pages_0928 drawings).

### 4 Oct (late): Walker now co-owns the generator · pack v23
- Walker's answers filed as `HANDOFF-2026-10-04-walker-answers.md` (repo + Drive pack folder). Her Claude edits the generator directly: `onestronghive` invited (write) to `shopnerd/coyote-mountain` and `shopnerd/will-os` on 4 Oct; her old repo + `build_all.sh` retired. Gallery stays open. Alfalfa unloading from the road through the end gates confirmed.
- **Stable stalls settled 12 × 14 / runs 12 × 40**; v14's 12 × 12 / 12 × 30 withdrawn. `pack.py`: discussion page `notes={0:[…]}` now seeds the Acuerdos box with the stall + alfalfa decisions; the open question (`notes={1:…}`) is gone. v23 built, copied over the shared `-2026-09-23.pdf`, web pages pushed.
- Walker-facing handoff `HANDOFF-2026-10-04-for-walker.md` §7 now holds her answers + a clone/build/push checklist. `OUTDIR` in `pack.py` is Will's Drive path; she will need to point it at hers (or make it an env var) when she builds.
- Both of us now push to `main` in both repos: pull before building, and keep bumping the `out=` version so PDFs never collide.

- **Elevations:** all 4 sides × Gemini + OpenAI + model now in the gallery section `#alzados` (will.100xbtr.com/equino/#alzados, group `g8`, morning set under Earlier versions as tags prevg/prevo). Will picks with ☆. Drive: `renderings/2026-10-03 stable elevations (eye level)/3 Oct pm - both models/`. Gemini east adds a ridge cupola that isn't there.
- **Walker's v14** = our pages re-footered "GIANT NATURE · oct 2026" + 7 new photo pages that she flattened to 150 dpi JPEG pages. She also relabelled stable stalls 12×12 / runs 12×30 (labels only). **Will decided: keep 12×14 / 12×40**; the question sits on the discussion page (Preguntas abiertas).
- **pack.py now builds v15 in her order and style:** `walker_pages.py` (Plus Jakarta Sans static instances in `projects/fonts/`, cream #efe7da, her captions transcribed) for pp.1–4, 6–8; technical pages unchanged except `tblock` footer (GIANT NATURE, oct 2026). QR on the stable page → public will.100xbtr.com/equino/model/. Output `Centro-Equino-pack-11x17-2026-10-03-v15.pdf` in the Drive pack folder (~29 MB). **The shared `-2026-09-23.pdf` link is NOT overwritten** (Walker edits now; ask first).
- **Photo resolution method:** matplotlib draws vectors only; `place_photos()` inserts each photo afterwards with PyMuPDF as JPEG q92 at native resolution, capped at 400 dpi (`MAXDPI`). Slots + crops in `walker_v14_slots.json`, found by detecting the photo rectangles on her flat pages and SIFT-registering each against ~980 Drive/render images (`walker_v14_match/`). Report per photo: `pack_photo_report.txt`.
- **Still low-res:** 6 slots have no original on Will's Drive (horse cover p1; p7 cobble paving, logs, fallen oak, steel roof, black posts) → crops of her 150 dpi pages in `walker_v14_crops/`. Will is asking Walker to share her source folder; when it lands, add it to the pool in `walker_v14_match/thumbs.py`/`sift.py`, rerun `reg.py`, update the 6 entries in `walker_v14_slots.json`, rerun pack.py. Also low: p4 big NE view 104 dpi and p2 #3 148 dpi (she zoomed into 1,536/2,752 px renders; no larger copies exist; a fresh model shot + finish at a tighter camera would fix it), p6 two of her web images (106/139 dpi).
- **p4 redone 3 Oct:** `modelshots.mjs` takes SHOT_W/SHOT_H/SHOT_DSF; camera `p4-site-ne` rendered at the slot aspect 2752×2406, then `renders/finish_hi.py p4-site-ne 5:4` (Gemini 4K, pads to the aspect and crops back; `paint.google` now takes aspect/size). Attempt 1 used (attempt 2 made the turnout a sand arena). Drive `renderings/2026-10-03 p4 site NE (hi-res)/`. v15 copied over the shared `-2026-09-23.pdf` on Will's yes. Same method fixes p2 #3 if wanted.
- **Walker's originals arrived via the Adobe connector (3 Oct pm):** her folder "Centro Equino - photos, renders & pack (Oct 2026)" (31 files, Cover/Inspiration/Materials subfolders). Method: `asset_search` with `directoryIds`/`mediaType` filter → `asset_get_presigned_urls` → `curl -L` the at.adobe.com link (the `renditionURL` from search is only a 600 px thumbnail; the presigned one is full size). Saved to Drive `renderings/Walker originals (Adobe share 3 Oct)/`; the six slots re-registered; pack v15 rebuilt and copied over the shared link. Nothing in the pack is a page crop any more. Lowest now: p7 logs/oak 167 dpi (her files are 632 px), p6 two web images.
- **Wash-pad trough (3 Oct, Will + Walker):** `site_extras.py` adds `wash pad trough` (12 × 3 ft fieldstone, rim 2 ft, along the pad's outer edge, slope cut back) → `wash-pad-trough.obj`; registered in `viewer/export.py` MATOBJ + STYLE. New elevation camera `el-south-wash` in modelshots.mjs (square to the south wall, 66 ft out; a fence crosses at ~90). **Trap:** a stale `http.server` on 8792 from the morning served an old data.json for hours; kill all python http.server processes before shooting.
- **Trough moved (3 Oct, later):** Will's picture = the 28 Sep `18-stable-west-elev` painting: the trough runs along the pad's WEST edge, out from the stable's SW corner (14 × 3 ft just outside the gable line), not along the south edge. `site_extras.py` updated; viewer re-exported; `18-stable-west-elev` and `el-south-wash` repainted (south-edge versions kept in `gallery4/v1-trough-south/`, `elevations/1003pm/v1-trough-south/`). That picture also shows a WOODEN SLIDING DOOR on the wash room: **Will decided YES (3 Oct, later)**: `centro-equino-barn.py` now hangs a 7 × 9.3 ft plank leaf (mat `wood`) on a steel track above the 6 × 9 opening, parked open to the EAST over the plastered wall; `swap_stable.py` run, `_bak_0928` stable stroke synced, viewer re-exported, pack v16 (stable page text + plan label). Will's 3 Oct gallery notes → actions: 18-stable-west-elev 'fresh render' (done, oct3o), b3-sw 'not cropped' (camera dist 560→660), 14-bleachers-high 'steps natural wood not white' (gallery3 EXTRA), b5-top 'current model + perfect rectangular plan' (b7-plan re-shot at w 470 + b5-top, both painted). Painted set = gallery4 / elevations/1003pm; superseded versions in `v2-open-doorway/` subfolders.
- **Native planting (Will, 3 Oct, red markup on el-west):** `site_extras.py` adds `native planting` (28 low sage/buckwheat mounds, two beds flanking the drive-in between the long trough and the west gable, 9.5 ft off the road) → `native-planting.obj`, mat `sage` (added to viewer MATS in BOTH index.html copies, export STYLE group trees). Briefs: gallery3 EXTRA 20-front-yard/6-west, elevations EXTRA el-west. Will's 8-stable note (no alfalfa in the stable runs, no gully, trailer as modelled) → gallery3 EXTRA 8-stable; repainted.
- **Gallery notes cleared (3 Oct, Will's request):** all 34 notes blanked for a fresh round; stars/removals kept. Backup of the full picks blob: Drive pack folder `gallery-notes-backup-2026-10-03.json`. The picks API is read-modify-write, so two people saving at once can lose a write; re-check after bulk edits. `elevations.py` now has an EXTRA dict (el-east: keep both framing pines, Will's note).
- **Trough views repainted both models after OpenAI credits came back (3 Oct); 11-arena re-shot and repainted too (it shows that corner). Will removed many new-round pictures because of the old trough position; the repainted keys were un-removed so he re-judges them.** Model views now sit behind "Earlier versions" everywhere (Will: not needed for choosing).
- **Road dip fixed (4 Oct, Will spotted an 8 ft trench in the scrub-side road above the stalls):** the covered-stalls pad levelling in `site_extras.py` used the stroke's `foot` bounding box, but covered-stalls.obj is written in EAST/NORTH feet (covered_stalls.py `world`), so the diagonal building's box was a 92 × 98 ft square that flattened a tongue to the road. Now tests the true rotated 92 × 52 rectangle (RXs 46, HDs 26, u/v from the yellow-line frame). Earthwork 3,635/3,154 → **3,344 cut / 2,844 fill yd³**; pack v20 behind the shared link. **Trap:** any code using a stroke's `foot` for the covered stalls must rotate into the building frame first.
- **Viewer "Estructura del techo · Roof structure" switch (4 Oct, key T):** stable trusses/purlins/eave beams tagged `truss` in `centro-equino-barn.py`; covered stalls get rafters + purlins + eave beams from `stalls_frame.py` (appends a `truss` block to covered-stalls.obj and refreshes the stroke in the drawings + _bak_0928 without moving it). **After any covered_stalls.py rebuild, run stalls_frame.py again.** Viewer MATS has `truss`; groups.truss; both index.html copies.
- **Pack v18 (4 Oct):** Walker's alfalfa handoff (`HANDOFF-2026-10-04-walker-alfalfa-layout.md`, her page 10 = 80 × 52 with two 16 × 12 bays, 384 sq ft) vs our model (88 × 52, two 24 × 12 bays = 576 sq ft, same as the old 16 × 36). **Will: keep the 24 ft bays.** `stalls_page.py` redrawn: corridor open through, two bays with pipe panel + gate to the aisle, unloading through end gates from the road, roof 92 × 36, end frame to the DRO. Her three questions answered on the page. Note: Walker now runs her OWN copy of the pack generator (`output/...` paths) — decide who builds. Heredoc trap: the Bash tool turns `\n` into a real newline inside heredoc Python; build escapes with chr(92)+'n'.
- **Pack v17 (4 Oct, Will approved):** finalists placed. p2 = the four stable elevations (W with horse/drive, N, S, E); p3 = covered stalls (1-hero-sw, 5-corridor-out, 2-corridor, 4-hill-s); NEW p4 (`w_renders('3b', …)`, slots `3b-*`) = north side, inside, bleachers picnic, picnic side; p5 site views (NE overview kept, b3-sw oct3o, b7-plan oct3o). p9 Inspirations bottom-left = Walker's "stick and frames.JPG" (finalists folder). Pack is 19 pages. **Page-number trap:** planview is its own page after site views, so Inspirations is p9 (not p8). Gallery: finalists grouped by subject in finalists mode (`FG` list in index.html). Comment repaints: el-south-sun (OpenAI, bands trimmed), el-west-horse (14 ft drive lined with plants both sides; planting now built AFTER the road re-route in site_extras.py).
- **Gallery re-render round (3 Oct pm):** `gallery3.py` takes `GAL_OUT` (→ gallery4), `elevations.py` takes `EL_OUT`, `paint.py` Gemini size via `GEMINI_SIZE=4K`; per-view EXTRA notes added for 18-stable-west-elev, b3-sw (water: `water: true` on the b3-sw camera), 5-corridor-out, 11-arena, 4-hill-s. Gallery section `#ronda3` (class `keep`, group g9, tags oct3g/oct3o) stays visible in finalists-only mode. Gallery now opens in finalists-only; `?all` shows everything.
- Earthwork now 3,635 cut / 3,154 fill yd³ (3 Oct level pad under covered stalls + alfalfa bay, trough wall, road). sheet2 captions A and C updated to say so.
