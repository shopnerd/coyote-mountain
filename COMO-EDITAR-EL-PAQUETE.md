# Cómo editar el paquete · How to edit the pack (Centro Equino, 4 oct 2026)

**Editor:** https://will.100xbtr.com/equino/pack/edit/  (works on a laptop or an iPad · funciona en laptop o iPad)

## Para Walker y Will · For Walker and Will

1. Abre el editor y elige la página arriba (1–19). · Open the editor and pick the page at the top (1–19).
2. Escribe tu nombre en **¿Quién?** para que quede en el historial. · Type your name in **¿Quién?** so it shows in the history.
3. **Mover · Move** (modo normal):
   - Arrastra una **foto** (borde naranja) o un **dibujo** (borde azul) para moverlo. · Drag a **photo** (orange edge) or a **drawing** (blue edge) to move it.
   - La **esquina** cambia el tamaño. Los dibujos conservan su forma; las fotos se recortan solas a la nueva forma. · The **corner** resizes. Drawings keep their shape; photos re-crop themselves to the new shape.
   - Flechas del teclado = ajuste fino; Mayús + flecha = más. · Arrow keys nudge; Shift + arrow nudges more.
4. **Cambiar una foto · Swap a photo:** toca la foto. En el panel de la derecha: · Tap the photo. In the right-hand panel:
   - **Subir foto · Upload** una foto nueva (del teléfono o la compu), o · a new photo (from the phone or computer), or
   - **busca en la galería** (ej. "stable", "east", "picnic") y toca la que quieras. · **search the gallery** and tap the one you want.
   - **Encuadre · Framing:** el control *Acercar · Zoom* y las flechas ← → ↑ ↓ mueven el recorte. · the Zoom slider and the arrow buttons move the crop.
5. **Texto · Text:** cambia al modo **Texto**, toca cualquier texto (títulos, pies de foto, párrafos, etiquetas de los planos), escríbelo de nuevo y **Guardar**. Los párrafos se vuelven a acomodar solos. · Switch to **Text** mode, tap any text (titles, captions, paragraphs, labels on the drawings), rewrite it and **Save**. Paragraphs rewrap by themselves.
6. **Deshacer · Undo** (Ctrl+Z) y **Restablecer · Reset** en cada elemento devuelven lo anterior. · Undo and the Reset button on each item put things back.

Todo se guarda solo. Lo que ves en el editor es una **vista previa**: el PDF y la página pública cambian cuando se reconstruye el paquete. · Everything saves by itself. What you see in the editor is a **preview**: the PDF and the public page change when the pack is rebuilt.

**Para publicar, pídele a Claude · To publish, ask Claude:** *"reconstruye el paquete con los cambios del editor" · "rebuild the pack with the editor changes"*.

## Para el Claude de Walker (o el de Will) · For Walker's (or Will's) Claude

```
cd coyote-studio/projects
git pull                      # and git pull in will-os
python pull_layout.py         # editor changes -> pack_layout.json; fetches swapped/uploaded photos (Drive: renderings/uploads, from-gallery)
python pack.py                # bump the out= version first; builds the PDF + will-os/equino/pack (pages, zoom crops, layout.json)
```
Then: copy the new PDF over `Centro-Equino-pack-11x17-2026-09-23.pdf` in the Drive pack folder, look at the changed pages, commit
coyote-studio (pack_layout.json + any slot changes) and push will-os (`equino/pack`). Read `HANDOFF-2026-09-24-centro-equino-session.md` §18 first.

How it works (so it can be extended): `layout_ov.py` loads `pack_layout.json` → photo slots merge into `walker_v14_slots.json`
values; texts are keyed by the crc32 of their ORIGINAL source text (`tkey`), paragraphs via `para()`/`wpara()` rewrap; drawings
are axes named with `set_gid` (e.g. `p03:plan`) and moved by mapping their visible extent onto the saved box. The editor reads
`will-os/equino/pack/layout.json`, saves to `/equino/api/layout` (Netlify Blobs `equino-layout`), uploads to `/equino/api/upload`
(`equino-uploads`). To make a new drawing movable, give its axes a gid; any axes over 1.2 % of the page is already listed.

Limits today: the drainage/irrigation sheet notes are drawn line by line, so editing one changes only that line; page order and
type sizes are not in the editor (ask Claude).
