# Handoff · 22 Sep 2026 · Centro Equino in the topo tool

Read this first. It covers a long session on **Walker's Centro Equino** at Chichihuas, worked live in
Will's Chrome on `https://coyotemountainfarm.com/topo.html`, plus five features added to the tool.

## Where the drawing stands

Will's drawing lives in **his browser only** (`localStorage` key `topo-session` on
coyotemountainfarm.com). It is NOT a file in this repo. Site: **1,312 ft wide**, centred
**31.9999, −116.7641**, sheet rotated 318–320°.

Objects in it (all `.obj` imports, all in `projects/`):

| object | what it is |
|---|---|
| walker barn 76x42 | Walker's barn from her artifact: 76 × 42 stone, eave 12, ridge 17, ten 12×12 stalls, 14 ft aisle, 12×30 runs, gable at **65.84°**, centre **32.0002846, −116.7632631** |
| trailer 8 x 40 | the parked tractor trailer, deck 4 ft up, roof at 13 ft |
| arena fence | 3-rail pipe round the oval arena, 454 ft, one 12 ft gate bay |
| round pen fence | same round the 60 ft pen, 190 ft, one 10 ft gate bay |
| site fence | his red boundary loop, **3,096 ft**, posts every 20 ft, three wires |
| cross fence | his red dashed line across the site, **484 ft** |
| four paddocks | the small blue rectangle: 4 paddocks 67.5 × 75 ft, each with a 12 × 16 three-sided covered stall |

Drawn work: oval **arena 182 × 78** (was a rectangle, now a stadium with 39 ft ends), **round pen 60 ft**,
two roads he drew, a **1,200 ft × 12 ft track** loop (60 ft corner radii) as a `path`, plan-drawn fence
lines for the site loop and the cross line, 222 spot heights, and his sketch markup (16 lines, hideable).

Grading applied to the terrain, in order: barn pad + all runs (76 × 102), arena pad, round pen pad,
parking pad (his oval by the road), the stable bench regraded to **2% falling north-west, cut = fill 303 yd³**,
a **310 yd³ interceptor ditch** 35 ft off the road's uphill side, the **track corridor smoothed to a 2.5%
cap** (1,424 cut / 873 fill), and a **level pad 20,250 ft² under the paddocks** (2,023 yd³ each way, level
1,086.8 ft). Site totals read about **cut 5,700 yd³ / fill 3,800 yd³**.

## The last thing done, and what is left

Will asked for the paddocks back, clear of the track, on flat ground. Done: the rectangle was **shifted
60 ft south-east** (centre now **31.9990304, −116.7640588**), which leaves **26 ft to the track centreline,
20 ft to its edge**; that ground was levelled first, then the paddocks and the site fence were rebuilt
draped. He stopped the session there ("turning off the generator").

Open:

- **The swale outlet is not designed.** Everything the ditch collects lands at its west end, 1,102.8 ft,
  and will cut a gully. Needs a spreader, a basin or a culvert.
- **His drawn roads sit on the west edge of the real track**, about 10 ft off centre. Everything measured
  from them inherits that. Nudging them east once would improve the pad clearance and the swale offset.
- **Terrain is 30 m public data.** Vertical error runs to several feet and the DEM cannot see the road cut,
  the benches or the terraces. All volumes are planning numbers, ±30–50%. A drone survey (SITE → lot and
  survey → drone survey DEM) is the real fix and would let every pad be re-cut in minutes.
- Walker is waiting on a decision: **stone walls (42 ft deep barn, 102 ft footprint) vs open bays on piers
  (38 ft deep, 98 ft)**. Her layout draws 98, the model builds 102.
- He rejected traced vineyards twice. The rows are in `projects/vineyard-rows.json` (133 rows, 9.7 ft
  apart at 142.7°) if they ever come back; 68 of them fall outside the 1,312 ft sheet.

## Tool features added this session (all pushed, all live)

1. **select can pick a placed object** — objects hit by their footprint and win ties against shapes they
   sit inside, so the barn is selectable inside the site outline.
2. **select turns and scales** — buttons, typed degrees or percent, `[` and `]` keys; it also reads the
   picked thing's sides, length and area.
3. **measure tool** (SHAPE → measure) — click point to point, close on the first point for area, keep it as
   a drawn line or shape. Reads ft² and acres.
4. **sketch hide/show** — `#penHide`, saved with the project as `hideSketch`. It hides freehand lines only,
   so **markup drawn with line/rect/circ has to be flipped to `shape:false` to be hidden** (that is how
   his markup gets hidden; `show` brings it back).
5. **exact sizes for line/rect/circ** — type length and width, drag only to point it; end snapping is
   switched off while a size is typed.
6. **paint prompt + check the painting** — the prompt now names every built thing at its true size
   (smallest rectangle that holds the footprint, so a turned barn reads 102 × 76, not its bounding box),
   forbids inventing or reshaping, and says red freehand marks are marks. **check the painting** sends the
   model view, the painting and a plain inventory to Gemini (`gemini-flash-latest`, then `gemini-3.6-flash`,
   `gemini-pro-latest`, `gemini-2.5-flash`), or OpenAI if only that key is present, and returns
   `{verdict, summary, issues[{item, problem, fix}]}` with tick boxes and a **paint again with these fixes**
   button. Verified by hand against a real painting: verdict `drift`, two issues, fixes fed back and
   repainted. **Gemini holds geometry better; both engines stay.**
7. **check-road.html** — the saved drawing laid over live Esri imagery, read straight out of the browser.
   Roads red, shapes cyan, ditches orange, objects white. This is the tool that proved the drawing is
   georeferenced correctly and that the 30 m terrain simply cannot follow the photo.

## Traps worth knowing

- **An imported object gets ONE ground height, sampled at its centre.** A 3,000 ft fence across 45 ft of
  fall ends up half buried, half floating. The fix used here: build the mesh with the terrain baked in
  (each post dropped onto its own ground, rails cut into 10 ft pieces) and set `st.lift` to the mesh's
  minimum, because `objFromMesh` lifts the lowest point to zero. `window.__drape2` in the page does this;
  it is **not** in the repo, so a reload loses it — the recipe is in this file and in the git log.
- **The `.obj` files in `projects/` are flat.** The draped versions exist only in Will's drawing. Re-grade
  under a fence and it must be re-draped.
- **An OBJ can carry its own place**: `# geo <lat> <lon>`, `# unit ft`, `# name ...`. topo.html lands it
  there at true north. The rotation slider only moves in 5° steps, so bake bearings into the mesh.
- **Stroke indices shift** whenever he erases. Always re-find strokes by geometry or colour, never by a
  remembered index.
- **Write into `z` without calling `snapshot()` first and undo cannot take it back.** That happened once
  with the track grading. Every grading call needs `snapshot()`.
- **Changing site width or detail refetches the terrain and wipes ALL grading** (`resetGrading`), and
  clears undo. Shapes and objects keep their positions.
- **His undo can remove work silently** — it took out the site fence and the paddocks mid-session, and the
  inset track. Check `S.strokes.filter(s=>s.kind==='obj')` before assuming something is there.
- **localStorage fills up.** Project snapshots are ~430 KB each; eleven backups exhausted the quota and
  blocked an import. Two are kept: `topo-backup-before-pads` (before any grading) and
  `topo-backup-before-fences`.
- **Vertical exaggeration (1.5×) is 3D and section only.** Plan contours and every measurement are true.
- Gemini retires exact model names; ask by the floating aliases first.

## Email

Renderings went to Walker at **onestronghive@gmail.com only** — Will's standing rule now, saved in memory.
Never `oramomi@gmail.com`. Sent via `trading-lab/send-email.py`, 7 attachments, in his Gmail Sent folder.

## Files added to this repo today

`projects/centro-equino-barn.py` + `.obj`, `projects/trailer-8x40.py` + `.obj`, `projects/pipe-fence.py`
+ `arena-fence.obj` + `roundpen-fence.obj`, `projects/site-fence.py` + `site-fence.obj` + `cross-fence.obj`,
`projects/stall-barn.py` + `.obj` (the rejected 28-stall double row, kept), `projects/paddocks.py` + `.obj`,
`projects/vineyard-rows.json`, `check-road.html`. Every generator takes its dimensions at the top.
