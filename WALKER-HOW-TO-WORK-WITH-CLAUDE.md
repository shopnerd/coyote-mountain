# Walker · how to have Claude change the topo drawing for you

*Cómo pedirle a Claude que cambie el dibujo topográfico por ti (versión en español abajo).*

This is the way Will and Claude built Centro Equino on 22–23 Sep 2026. You talk; Claude does the
work directly in the topo app in your own Chrome, and you watch it happen.

## What you need (once)

1. **Chrome** with the **Claude in Chrome** extension installed and signed in:
   https://chromewebstore.google.com/detail/fcoeoabgfenejglbffodgkkbkcdhcgfn
2. **Claude Code** (the desktop app, Code tab), so Claude can drive your browser and save files.
3. **The drawing.** It lives in the browser, not in a file. Will exports it from the app
   (SITE → project → save) and sends you the `.json`; you open https://coyotemountainfarm.com/topo.html
   and load it (SITE → project → open). From then on your Chrome keeps its own copy.
   Keep the `.json` as your backup.

## How to start a session

Open the topo page in Chrome, then in Claude Code paste:

> Read `WebDev/coyote-studio/HANDOFF-2026-09-23-grading.md` and
> `WebDev/coyote-studio/HANDOFF-2026-09-22-equine.md`. Then open my topo drawing in Chrome
> (coyotemountainfarm.com/topo.html), tell me what's in it, and wait for my changes.

Claude will check what's there (barn, fences, roads, pads, water) before touching anything.

## How to ask for changes

- **Draw it, don't describe it.** Sketch on the drawing with the red pen (SHAPE → sketch):
  a line for a road, a rectangle for where something goes, a circle for a gate or a spot.
  Then say what it means: "the red line is a truck road, the circle is a gate."
  Claude reads your marks as exact coordinates. Screenshots work, but drawing in the app is better.
- **Say sizes in feet** when you know them ("12 ft trough, 3 ft tall").
- **One change at a time** is easiest to check, but a list is fine.
- **Ask to see it:** "show me a screenshot," "paint a top view," "paint a 3/4 view at golden hour."

## What Claude can do in the drawing

- Move, turn, resize or delete things (barn, paddocks, trough, cars, fences).
- Draw and grade roads, the track, pads, ditches, swales, the pond.
- Rebuild fences to follow the ground, with gate openings.
- Reset the grading and replay it after a layout change.
- Paint renderings (top, 3/4, eye level, green season, white site model) and save every one.
- Make bilingual plan sheets: drainage, grading, sections.

## Rules that keep the drawing safe

- **Only one topo tab open at a time.** An old tab can save over the new drawing.
- **Export a backup before big changes** (SITE → project → save). Undo is not always reliable.
- Claude asks before anything outside the drawing (email, sharing, buying).
- Tell Claude when you're stepping away; it stops and summarises.

## The finished design, in one line

Barn 76 × 42 ft (stone to 4.5 ft, stacked sticks above, sky-blue roof, 10 stalls with 12 × 30 ft
runs), four paddocks with shade stalls, oval arena, 60 ft round pen, 1,224 ft track using the west
road, pond at the track's south-east end, 12 × 4 ft stone trough fed by the barn roof, 10 ft round
watering station, parking in the east strip. Every sheet is in Spanish and English.

---

## En español

Así trabajaron Will y Claude en el Centro Equino. Tú hablas; Claude hace los cambios directamente
en la app topográfica, en tu propio Chrome, y tú lo ves pasar.

**Lo que necesitas (una vez):** Chrome con la extensión Claude in Chrome (enlace arriba) y
Claude Code. El dibujo vive en el navegador: Will te manda el archivo `.json` y lo abres en
coyotemountainfarm.com/topo.html (SITE → project → open). Guarda el `.json` como respaldo.

**Para empezar:** abre la página y pega en Claude Code el mensaje de arriba ("Read ... Then open my
topo drawing ..."). Claude revisa lo que hay antes de tocar nada.

**Para pedir cambios:**
- **Dibújalo, no lo describas.** Marca con la pluma roja: una línea para un camino, un rectángulo
  para dónde va algo, un círculo para una puerta. Luego di qué significa.
- Da las medidas en pies o metros.
- Pide ver el resultado: "muéstrame una captura", "pinta una vista desde arriba".

**Para cuidar el dibujo:** una sola pestaña abierta; guarda un respaldo antes de cambios grandes;
Claude pregunta antes de cualquier cosa fuera del dibujo.
