# How the café-in-the-trees renders were made

Centro Equino, 10–12 Oct 2026. Walker's Claude.

None of this used Photoshop. Every image is an AI image edit (Google Gemini, model `gemini-3.1-flash-image`). The AI gets one or more pictures plus written instructions and returns a new picture. Photoshop is only needed for exact fixes the AI won't make (see "Limits").

## The ingredients

| Image | What it controls | Where it came from |
|---|---|---|
| **Site photo** | The place: trees, ground, hill, sky, light, camera | Walker's phone photo of the spot (`cafe-option2-site-photo.jpg`) |
| **Topo app view** | Exact position, size and orientation of the building | Will's topo app, 3D view of the option 2 drawing, exported as PNG |
| **Texture photos** | What the materials really look like | The real trailer: `will-os/equino/model/trailer-side.jpg` and `trailer-end.jpg` |
| **Design render** | The style of the parts: platforms, roof, people | An earlier gallery render (`23-picnic-side-oct4o`) |

## The steps

1. **Place the building in the model.** Move or turn the object in the topo drawing, then save it as a new drawing (`centro-equino-2026-10-10-cafe-option2-trees.json`).
2. **Take the camera view.** In the topo app's 3D view, aim at the building, then export a PNG. This is the "layout" image.
3. **Send everything to the AI in one request.** Number each image in the prompt and say what each one controls, for example:
   - *Image 1 sets the camera and layout; keep everything where it is. Ignore the drawing marks (contours, red site line, fence lines, label text).*
   - *Image 2 is a real photo of this spot: use its trees, grass, hill and light.*
   - *Images 3 and 4 are the real trailer: it must look exactly like this. No signs or lettering.*
   - *Image 5 shows the style of the platforms.*
   - Then the design rules: *platforms on the north side only; tables near the trailer; no cars.*
4. **Make three versions at once** and compare them side by side next to the source. The AI varies a lot from version to version, so pick the most faithful one, not the prettiest.
5. **Fix one thing at a time.** Give the chosen image back to the AI with a narrow instruction: *"Change ONLY the end wall… keep everything else exactly the same."* That's how the post was removed, the trailer end was cleaned up and the porch was added.
6. **Zoom out if needed.** Put the picture in the middle of a bigger grey frame and ask the AI to fill the grey with the rest of the scene.
7. **Into the pack:** save the result in `coyote-studio/projects/renders/picks/`, point the slot in `walker_v14_slots.json` at it, rebuild with `pack.py`, and publish.

## Where it runs

- The requests are sent **from inside the topo app's browser tab**, because Walker's Gemini key is saved there (Topo → AI / paint → key). The key never leaves that page.
- Claude adds a hidden file box to the tab, loads the images into it, sends the request, and the results save to **Downloads**.
- The same thing works from Will's `projects/renders/paint.py` if `GEMINI_API_KEY` or `OPENAI_API_KEY` is set on the computer.

## Tips

- **Name what each image is for.** Otherwise the AI mixes them up. Our first café came out as a white cabin because the reference render was read as "the building".
- **Describe the real object in words too,** as well as giving the photo: *"ribbed faded grey aluminium, olive stripe, rusty end."*
- **Say what to leave out.** The AI invents things: signs ("FIELD CAFE"), an Airstream, stone walls, vans, cars. *"Add nothing. No signs or lettering."*
- **Gemini is dramatic; OpenAI is more faithful to the model.** Will's rule of thumb.
- **Keep the light and camera from the photo** if you want it to look like the real site.

## Limits

- **Size and proportion edits mostly fail.** Asking it to lower the café roof three times changed almost nothing. For exact geometry, either move the building in the model and re-render, or fix it in Photoshop (select, move, then Generative Fill the gap).
- **The topo camera can't go all the way to standing eye level** through the connector. Eye-level shots used the site photo's own viewpoint instead.
- **The renders don't update automatically.** When the model changes, for example the porch moving to the road end, the pictures don't follow. They have to be repainted.
