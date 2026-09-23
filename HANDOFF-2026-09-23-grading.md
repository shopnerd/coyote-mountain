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

## Open

- **Re-drape the site fence and cross fence 3D objects.** They were bent to the 9/22 ground and
  now float or sink. The `__drape2` recipe is in the 9/22 session transcript.
- Stroke at grid (91.9, 60–62), a lone small red mark by the round pen. Not yet asked what it is.
- The arena and round-pen 3D fences each carry their own gate bay; the new gate bars may not match
  where those bays are.
- Walker's barn decision (stone walls, 102 ft, or open bays, 98 ft) is still open.

## Tool changes pushed today

`__dbg` hook now also has `base`, `resetGrading`, `drawPlanNow` (redraw in a hidden tab, where no
animation frames run), `analyzeCore` and `inPoly`. Soft pad edges in `applyPad`.
