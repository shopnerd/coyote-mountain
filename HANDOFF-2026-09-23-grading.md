# Handoff · 23 Sep 2026 · Centro Equino graded (supersedes the grading notes in 9/22)

Will's drawing still lives only in his browser (`localStorage['topo-session']` on coyotemountainfarm.com).
Everything below is in it. Read the 9/22 handoff for the traps; they all still apply.

## What was done, in order

1. **Grading reset to natural ground**, then the track's south side straightened (loop 1,188 ft).
2. **Roads: a false start, reverted.** Esri serves different photos at zoom 18 and 19, and here they sit
   about 13 ft apart. topo.html shows zoom 18. Roads fitted to zoom 19 landed in the scrub on Will's
   screen. **Always fit to the photo the app shows (z18, `aerialCache()` via `__dbg`).** Will's
   original roads were right on it and are back.
3. **Pad tool: soft edges** (crisp / soft / softer, soft default), pushed live.
4. **Water plan** (artifact https://claude.ai/artifact/3aVtBDrvF5LAYf6XwhSamw): one flow matters.
   About 10 acres of the scrub hill crosses the road bend by the paddocks, runs through the track
   infield and leaves by the west fence. That page predates the roads and pads below.
5. **Will's markup built** (his red lines became 12 ft truck roads; the parking-to-barn line became a
   5 ft walking path):
   - Pads, balanced, soft edges: barn 1,087.6 ft (1% fall), paddocks 1,082.5 (1%, moved 8.8 ft south
     to fit the road), arena 1,073.3 (1%), round pen 1,080.6 (1%), parking following the ground
     (about 5% west and 2% north, drains to the vineyard, which Will says is fine: one owner).
   - Roads as `path` strokes: track, both existing roads, trail round the track, road between track
     and paddocks (straightened), paddocks to the cross-fence gate, barn to the cross fence, arena and
     round-pen ring roads, main road from the NE gate to the south gate, parking access, walking path.
   - Water, all dug (`S.rec.ditches`, saved as `records.ditches`): main waterway in two legs, the
     infield basin, the branch from the paddock-end inlet, the barn diversion and its outfall to the
     draw, the ditch above the barn road, and the paddock swale. The stale 9/22 interceptor ditch
     was removed.
   - Culvert marks (water colour) at 7 crossings; 11 gate bars (4 perimeter, cross fence, arena,
     round pen, 4 paddocks); 13 parking stalls at 60°, pulling in westbound, west end left open to
     turn round; stone trough (20 ft ring) west of the barn at 1,082.4 ft with a roof-water pipe.
   - Site totals about **cut 4,700 / fill 4,500 yd³**, still ±30–50% on 30 m terrain.

## Later the same day

- **The trail round the track is gone** (Will: the track itself is a road). The ground was rebuilt
  from natural by replaying every pad, ditch and road without it. Two 12 ft spurs replace it: track
  to the north-west gate (61 ft) and track to the south-west gate (207 ft, down the paddocks' west
  side). The road between the track and the paddocks stays.
- New gate on the north fence near the NW corner (Will's red circle). Stray mark deleted.
- **Site and cross fences rebuilt on the graded ground:** a post at least every 20 ft, three wires,
  real openings at the gates (site 164 posts and 5 openings, cross 26 posts and 1). The site
  fence's footprint is now the true fence line, so the plan diagonal across the notch is gone.
- Trap, hit again: stroke indices shift when anything is deleted. Find fence lines by shape
  (the 10-point loop starting at 26.6, 23.6; the 2-point dashed line at i 69.3), never by index.

## Last change of the day

- **Track widened west onto the existing road** (Will: that road already runs gate to gate, and the
  track uses it as its west side). Track 1,224 ft; the two spurs became one "west road, gate to gate"
  (NW gate to SW gate, down the paddocks' west side). Ground rebuilt from natural again.
- Existing **watering station** marked where Will circled it (24 ft round, inside the track's SW).
- Round-pen gate moved to the pen's north side, where Will drew it.
- The round trough became a **12 × 4 ft stone trough, 3 ft tall** (3D object `stone trough 12x4`),
  running from the old spot toward the main road, on a small level apron at 1,082.2 ft; roof pipe
  re-pointed to it.

## Open

- The arena and round-pen 3D fences each carry their own gate bay; the new gate bars may not match
  where those bays are.
- The water plan page predates the roads and pads.
- Walker's barn decision (stone walls, 102 ft, or open bays, 98 ft) is still open.

## Tool changes pushed today

`__dbg` hook now also has `base`, `resetGrading`, `drawPlanNow` (redraw in a hidden tab, where no
animation frames run), `analyzeCore` and `inPoly`. Soft pad edges in `applyPad`.

## Evening: renderings and plan sheets

- Pond dug at the track's SE end beside the paddocks (water pools there by design, ~11,000 gal);
  watering station shrunk to 10 ft and filled (3D); trough rotated 90°; 5 parked cars (3D) in
  the east strip; stepped-model layer thickness set to 1.
- ~30 paintings saved in Downloads (`coyote-topo-painted-*`), all kept, good and bad. Gallery:
  https://claude.ai/artifact/2M6bC7MXYVzZYgq9uUX3XR. gpt-image-2 holds layout far better than
  Gemini here; the model's grey base edge gets painted as a lake or backdrop, so frame it out.
- Bilingual plan set (ES first, EN italic): https://claude.ai/artifact/3aVtBDrvF5LAYf6XwhSamw.
  Sheets D-1 drainage and D-2 sections come from `projects/drain.py`, `sheet1.py`, `sheet2.py`,
  which read an exported project JSON (`Downloads/centro-equino-final-2026-09-23.json`, with the
  app's flow grid in `__flow`). Standing rule: every report or sheet for this project is bilingual.
