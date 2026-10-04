# Centro Equino · handoff for Walker (and Walker's Claude) · 4 Oct 2026

How the design pack, the website and the 3D model are built and kept in step, so changes made on either side land
in the right place. Written by Will's Claude; Will approved the decisions listed below.

## 1. What is published, and where
| | Link | What it is |
|---|---|---|
| **Presentation page** | https://will.100xbtr.com/equino/pack/ | The whole pack, page by page, with buttons to the 3D model and the PDF. Public, no sign-in. This is the one link to share. |
| **3D model** | https://will.100xbtr.com/equino/model/ | Turn the site in the browser; switches for roofs, roof structure, roads, water, contours, fences; sun slider; side panel with both floor plans and the schedule of spaces. Public. |
| **PDF pack** | Drive › `MEXICO / Chichihaus / 2026-09-23 Centro Equino pack / Centro-Equino-pack-11x17-2026-09-23.pdf` | Always the newest version under that fixed name, so the shared link never breaks. Dated copies (`…-2026-10-04-v22.pdf` etc.) sit next to it. |
| Renderings gallery | https://will.100xbtr.com/equino/ | Working tool for Will and Walker only: star finalists, remove, leave notes. Not linked from anything public. |
| Adobe folder | "Centro Equino – photos, renders & pack (Oct 2026)" | Walker's originals (photos, materials, inspiration). Will's Claude pulls full-size files from here. |

## 2. Where the truth lives
- **The pack is generated, not drawn by hand.** One script (`pack.py` in Will's `coyote-studio` repo) builds every page:
  Walker's v14 layout and branding (cream pages, Plus Jakarta Sans, GIANT NATURE footer) is built into it, every
  photo is placed at native resolution, and the technical pages (plans, structure, topo, grading, drainage, sections)
  are drawn from the same 3D model and terrain the viewer shows.
- **One build does everything:** new PDF → copied over the shared name on Drive → page images written for the
  presentation page → the site is pushed. The 3D model updates from the same source files.
- **Therefore: please don't edit the PDF itself** (in Acrobat, Express or another generator). An edited PDF can't be
  carried forward: the next build would overwrite it. The v14 edits were folded into the generator by hand once;
  from here on, changes go through the generator.

## 3. How Walker makes a change (two good ways)
**A. Hand it off (works today, nothing to install).** Put the change where Will's Claude will find it:
1. Drop any new files into the Drive pack folder, `renderings / 2026-09-28 finalists` (photos, marked-up pages,
   sketches). Full-size originals, not screenshots, when it's a photo for the pack.
2. Write a short handoff like the alfalfa one (`HANDOFF-alfalfa-layout-2026-10-04.md` was perfect): what changed,
   the numbers, what it affects, open questions. Email it to Will, or drop it in the same Drive folder.
3. Say which pages it touches. Will's Claude folds it into the generator, rebuilds, and republishes everything in one go.

**B. Edit the generator directly (when Walker has the laptop).** Will can give the `coyote-studio` repo to Walker's
GitHub (onestronghive). Then Walker's Claude edits `projects/pack.py` (page order, captions), `projects/walker_pages.py`
(the photo pages), `projects/walker_v14_slots.json` (which photo goes in which slot) or the model scripts, runs
`python pack.py`, and pushes `will-os` to publish. The handoff that explains the scripts is
`coyote-studio/HANDOFF-2026-09-24-centro-equino-session.md`, section 18 (newest notes at the top of §18).

Either way: **one generator.** If two copies exist, the pack forks and someone's work gets lost.

## 4. The gallery (how the picks reach the pack)
- Open https://will.100xbtr.com/equino/ on the iPad. It opens on **Finalistas, por tema**: everything starred, grouped
  by subject. "Ver todas" shows every round. ☆ marks a finalist, "Quitar" removes a picture, the note box saves a
  comment. Everything saves for both of you at once; no sign-in.
- Notes are read as instructions: a note on a picture ("make the steps wood", "sunnier", "add a horse at the trough")
  becomes a repaint; a star on a picture puts it in the pack at the next build. Walker's notes from 3 Oct were all
  acted on this way.
- The gallery is not public-facing and isn't linked anywhere; the address is just not advertised.

## 5. The 3D model
- https://will.100xbtr.com/equino/model/ is exported from the same drawing the pack uses. Switches: **Techos**
  (roofs), **Estructura del techo** (trusses, purlins, eave beams; key T), roads, water, contours, fences, labels.
  "A la altura de los ojos" walks you in at eye level; the sun slider is real solar time for the site.
- The side panel's plans and "Espacios" table are kept to the current numbers (see §6).
- Walker's earlier viewer artifact on claude.ai is superseded by this page; the QR on the stable plan points here.

## 6. Decisions made 3–4 Oct (so they are not re-proposed)
- **Covered stalls:** corridor runs straight through; **two alfalfa bays of 24 × 12 ft** either side of the corridor
  (576 sq ft, the same hay as the old 16 × 36 bay), **88 × 52 ft** overall, roof 92 × 36. Pipe panel with a gate between
  each bay and the aisle; alfalfa unloads through gates in the end panels from the main road, truck stays out of the
  aisle. (Walker's page 10 drew 16 × 12 bays within 80 ft; Will chose the 24 ft bays.) The end frame goes to the engineer.
- **Stable:** wash room gets a **wooden sliding door** (7 × 9 ft leaf on a track, parked east of the 6 × 9 opening);
  a 14 × 3 ft stone trough along the **west edge** of the 12 × 24 concrete pad; the long stone trough stays 57 ft off the
  gable; the **entry drive is 14 ft wide and lined with native planting** (sage, buckwheat, deer grass) on both sides from
  the trough to the gable. Stalls stay 12 × 14 with 12 × 40 runs.
- **Pack order (v22, 18 pages):** cover · stable elevations · stable plan · stable structure · covered-stalls renders ·
  covered-stalls drawing · north side / inside / bleachers / picnic · site views · plan view · text and references ·
  materials · inspirations (sticks-in-frames photo bottom left) · topo · grading · operator sheet · drainage ·
  sections · discussion. Logistics page dropped.
- **Earthwork** now 3,344 cut / 2,844 fill yd³ (a grading bug that flattened a square up to the scrub road was fixed 4 Oct).

## 7. Open questions for Walker
1. Who edits the generator from here: Walker's Claude with repo access (§3 B), or handoffs to Will's Claude (§3 A)?
2. Should the gallery be locked behind a sign-in? It is reachable by anyone with the address today.
3. Discussion page (18): the "Acuerdos" box is Walker's to fill; the open stall-size question is written there.
4. The alfalfa handoff asked where the hay unloads; the pack now says "from the road through the end gates". Confirm.

## 8. Contacts and names
Will: zolaray25@gmail.com (Gmail is the channel for this project). Walker: onestronghive@gmail.com. The ranch
manager's name is **Andrés**. Everything in the pack is bilingual, Spanish first, English in italic.
