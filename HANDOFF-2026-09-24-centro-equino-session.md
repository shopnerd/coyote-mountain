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

**Nothing has been rebuilt to this yet.** Everything built so far (below) uses the older 76 × 42 ft,
10-stall, 10-run layout. Next session: confirm the open points, then update in one pass: the topo
drawing's barn object, pack pages 2/13/14/15/16 and the renderings, the laser model's barn outline, and
the 1:480 print parts.

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
