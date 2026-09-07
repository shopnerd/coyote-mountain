# Handoff: drone flight planner + Encino Solo survey import
Date: 2026-09-07. Written by Claude (Fable 5.1) for Will, and for a second opinion from another model.

If you are GPT, Gemini, or another assistant reading this: you have no other context. Everything you need is here. The last section lists the specific claims and decisions I want you to check or challenge. Please separate "this is wrong" from "I would have done it differently."

## 1. Who and what

Will runs a small creative web studio at https://coyotemountainfarm.com for his property, Encino Solo, near Ensenada, Baja California (about 32.0147 N, 116.7780 W). The site is three single-file web pages, plain HTML/JS, no build step, no libraries, hosted on GitHub Pages from the public repo `shopnerd/coyote-mountain`:

- `index.html`: a generative sketch studio.
- `topo.html`: a landscape grading tool. It fetches real elevation for any place (USGS 3DEP in the US, otherwise Mapzen Terrarium tiles, fallback OpenTopoData), draws contours and hachures, lets you sculpt proposed grade, shows cut and fill, exports STL and laser-cut contour stacks, drapes Esri aerial imagery, and loads KML/KMZ/GeoJSON (a property boundary, or a KMZ GroundOverlay image).
- `flight.html`: new today. A drone flight planner for photogrammetry surveys. Described below.

Will does not own a drone right now. He asked for the planner to cover the DJI Mavic Pro and Mini families so it's ready when he buys one.

Will also has a real drone survey of Encino Solo, made with DroneDeploy, sitting in Google Drive at `MEXICO (1)/DroneDeploy/`. He wants a workflow to import high-resolution drone surveys into the topo tool.

## 2. The flight planner (flight.html), as built

Live: https://coyotemountainfarm.com/flight.html. Source: one file, about 700 lines, in the repo above.

### What it does
1. Fetches terrain and the aerial photo for a place, on a 150 by 100 node grid covering a chosen site width (100 to 6000 m). Same data sources as the topo tool.
2. The user clicks the corners of the survey area on the photo, or loads a KML/GeoJSON polygon. A "fit terrain" button recentres the fetch on the polygon.
3. Picks an aircraft from presets or enters a custom camera.
4. Sets height above ground, front and side overlap, line heading (auto = along the longest polygon edge), speed, terrain-following on or off, single grid or crosshatch, gimbal pitch.
5. Computes the flight lines, photo points, waypoints, and statistics, draws them on the map, and draws a profile strip of ground versus drone altitude along the whole route.
6. Exports KML, GeoJSON, Litchi CSV, DJI WPML KMZ, PNG. Save/open as JSON, and a share link that carries the whole plan in the URL.

### The math
Symbols: sensor width `sw` and height `sh` in mm, image width `px` in pixels, 35 mm-equivalent focal length `eq` in mm, height above ground `AGL` in m.

- Real focal length: `f = sw * eq / 36`. (Derived from DJI's published 35 mm equivalent, because DJI spec sheets state the equivalent more consistently than the true focal length.)
- Ground footprint of one photo: across-track `W = sw / f * AGL`, along-track `H = sh / f * AGL`. Assumes the camera's long side is perpendicular to the direction of flight, which is how DJI gimbals are mounted when the drone flies forward.
- Ground sample distance: `GSD = sw * AGL / (f * px)` metres per pixel.
- Line spacing: `W * (1 - side_overlap)`. Photo spacing along a line: `H * (1 - front_overlap)`.
- Lines are laid perpendicular to the chosen heading, centred so the first and last lines are equally inset, each line extended by half a footprint past the polygon edge, in serpentine order. Concave polygons get one continuous pass per line across any notch.
- Terrain following: the ground is sampled every 1 to 10 m along each line (half a grid cell), the target profile is `ground + AGL`, and that profile is simplified with Douglas-Peucker at a tolerance of `max(1.5 m, 8% of AGL)` to produce the waypoints. Fixed-altitude mode uses two waypoints per line at `takeoff ground + AGL`.
- Time: `distance / speed + 4 s per turn + climb and descent at 3 m/s`. Batteries: `ceil(time / (rated minutes * 0.7))`, the 30% reserve covering wind, climb-out, and the flight home.
- Warnings: any point more than 121.92 m (400 ft) over the ground; more than 120 m above the takeoff point (DJI app default limit) and more than 500 m (hardware ceiling); photo interval under 2 s; more than 99 waypoints (Litchi's cap); ground rising above the flight altitude in fixed mode; in fixed mode, the effective overlap and GSD at the highest ground.

### Aircraft presets (sensor mm, image px, 35 mm equivalent, rated minutes)
| Preset | sw x sh | px x py | eq | min |
|---|---|---|---|---|
| Mavic Pro | 6.17 x 4.55 | 4000 x 3000 | 28 | 27 |
| Mavic Pro Platinum | same | same | 28 | 30 |
| Mavic 2 Pro | 13.2 x 8.8 | 5472 x 3648 | 28 | 31 |
| Mavic 2 Zoom (wide) | 6.17 x 4.55 | 4000 x 3000 | 24 | 31 |
| Mavic Air 2 | 6.4 x 4.8 | 4000 x 3000 | 24 | 34 |
| Air 2S | 13.2 x 8.8 | 5472 x 3648 | 22 | 31 |
| Mavic 3 / Classic / Pro wide | 17.3 x 13.0 | 5280 x 3956 | 24 | 46 |
| Mini / Mini SE | 6.17 x 4.55 | 4000 x 3000 | 24 | 30 |
| Mini 2 / Mini 2 SE | same | same | 24 | 31 |
| Mini 3 | 9.6 x 7.2 | 4032 x 3024 | 24 | 38 |
| Mini 3 Pro | same | same | 24 | 34 |
| Mini 4 Pro | same | same | 24 | 34 |

These are from memory of DJI spec sheets, not looked up today. See section 6.

### Export formats
- KML: survey polygon, takeoff point, flight path as a LineString with `altitudeMode absolute`, one Placemark per waypoint and per photo point (photo folder hidden by default).
- GeoJSON: same content as features with properties.
- Litchi CSV: the 46-column Mission Hub format (`latitude, longitude, altitude(m), heading(deg), curvesize(m), rotationdir, gimbalmode, gimbalpitchangle, actiontype1..15 + actionparam1..15, altitudemode, speed(m/s), poi_latitude, poi_longitude, poi_altitude(m), poi_altitudemode, photo_timeinterval, photo_distinterval`). One row per waypoint, altitude relative to takeoff, `altitudemode 0`, `gimbalmode 2` (interpolate), gimbal pitch from the slider, no per-waypoint actions, `photo_distinterval` set to the photo spacing.
- DJI WPML: a KMZ (stored zip written by hand) containing `wpmz/template.kml` and `wpmz/waylines.wpml`, namespace `http://www.dji.com/wpmz/1.0.2`, `heightMode relativeToStartPoint`, one action group covering all waypoints with a `multipleDistance` trigger at the photo spacing that rotates the gimbal and takes a photo. `droneEnumValue` is set to 68.

### Verification done
- Syntax check and unit tests on the line-planning and simplification functions in Node (rectangle, rotated heading, concave L-shape, serpentine order, plateau simplification).
- Loaded in Chrome against live terrain at Encino Solo. Mini 2 at 200 ft over a 31-acre polygon: 0.90 in/px, 412 photos, 24 min, 2 batteries, 12 lines, 49 waypoints. Footprint 300 x 221 ft. These match a hand calculation.
- All five exports generated without errors. KML and KMZ parse as XML, the KMZ passes Python's zipfile CRC test, the CSV has 46 columns on every row.
- Not verified: no export has been loaded into a real drone or into Litchi or DJI Pilot. Will has no drone.

### Known issues
- One Chrome tab froze during testing after a sequence of toggles. The same sequence in a fresh tab did not freeze. Cause unknown.
- The DJI WPML export is untested on hardware, and DJI does not officially support importing WPML into the consumer DJI Fly app.

## 3. Will's question about fixed altitude

Will asked whether photogrammetry requires a fixed flight altitude, since that seems to be how distances are computed, and noted the planner keeps altitude relative to the ground instead.

My answer: photogrammetry software reconstructs camera positions and the surface from overlapping photos plus their GPS tags (structure from motion followed by dense matching). It does not require constant altitude. What it needs is consistent overlap and consistent ground sample distance, and both depend on height above the ground directly below the drone. Fixed altitude above takeoff is the default of consumer apps because it needs no terrain data; on hilly ground it produces varying GSD and overlap. DroneDeploy's "Terrain Awareness" and DJI Pilot 2's terrain follow exist for this reason. On Will's own survey, 37 m of relief inside the area means a fixed 61 m flight varied between roughly 42 and 79 m above the actual ground.

## 4. The Encino Solo DroneDeploy export, inspected

Folder: `C:\Users\zolar\Google Drive\MEXICO (1)\DroneDeploy\`. Export timestamps say "TueMar19", files dated August 2022.

What's there and what each actually is (read from the file headers, not from the file names):

| File | What it is | Verdict |
|---|---|---|
| `EncinoSolo_Orthomosaic_*.tif` | GeoTIFF, 25088 x 27392 px, 4 x 8-bit RGBA, deflate compression with horizontal predictor, 256 px tiles, EPSG:3857 (Web Mercator), pixel 0.018661 m, 790 MB. Origin tie point (-12999898.598, 3765498.215). | Real orthophoto at 1.87 cm/px. |
| `EncinoSolo_NDVI_*.tif` | Same geometry as the orthomosaic, RGBA colour picture of NDVI. | A picture, not an index raster. |
| `EncinoSolo_Elevation_*.tif` | GeoTIFF, 9187 x 9922 px, 4 x 8-bit RGBA, pixel 0.052 m, EPSG:3857. | A colour-ramp picture of elevation. Contains no numeric heights. |
| `EncinoSolo_Elevation_*.pdf` | 1 page, 71 MB, no extractable text. | The legend is rasterised, so the colour ramp cannot be decoded to metres. |
| `modelTue*/scene_mesh_decimated_textured.obj` | Meshlab OBJ, 1,021,033 vertices, 2,037,422 faces. Coordinates: x -196.7 to 204.4, y -208.6 to 221.7, z -54.4 to -17.4. 21 JPEG textures. | The real surface. Local metre frame, x east, y north, z relative to an unknown datum. Includes tree canopy (a DSM, not a DTM). |
| `Encino Solo Topo.obj` | Rhino re-export of the same mesh, y and z swapped (Rhino y-up). | Same data. |
| `*.kml` next to each TIFF | GroundOverlay LatLonBox. Elevation box: N 32.0166639, S 32.0127333, E -116.7758278, W -116.7801194. Ortho/NDVI box: N 32.0166639, S 32.0127694, E -116.7758694, W -116.7800750. | The footprint bounds. |

Footprint check: the elevation LatLonBox is 405.1 x 437.5 m, the mesh bounding box is 402.0 x 431.0 m. The survey itself is a rectangle rotated about 35 degrees inside those boxes, so the boxes are about half empty.

## 5. Derived products, made today

All in `MEXICO (1)\DroneDeploy\coyote-studio-import\` with a README. Scripts need only Python with numpy and Pillow.

- `encino-heightfield.npy` + `.json`: the mesh rasterised onto a 0.5 m grid, 804 x 862 cells, NaN outside the survey. Made by sampling every triangle on a barycentric lattice at half-cell spacing and keeping the maximum height per cell (`mesh2grid.py`). Coverage is 50.8% of the bounding box, which is the rotated rectangle. Small gaps were filled by six passes of neighbour averaging.
- Georeference: I assumed the mesh bounding-box centre coincides with the DroneDeploy elevation LatLonBox centre (32.014699, -116.777974). Estimated uncertainty about 2 m horizontally.
- Vertical datum: mesh z is relative. I sampled the public 30 m terrain (Terrarium tiles, zoom 15) at 236 mesh cells and took the median difference: +309.7 m (mean 310.5, standard deviation 10.4 m, which includes the 30 m smoothing and the canopy). So the survey sits at about 255 to 292 m above sea level, accurate to a few metres.
- `encino-heightfield.png`: hillshade with 1 m contours.
- `encino-ortho.jpg`: the orthomosaic decoded tile by tile (zlib per tile, undo the predictor, alpha-weighted 8 x 8 box filter) to 3136 x 3424 px, about 15 cm/px (`ortho-shrink.py`).
- `encino-solo-ortho.kmz`: that JPEG as a KML GroundOverlay with the orthomosaic LatLonBox (`ortho-kmz.py`). The topo tool can load this today through its existing KMZ button. Not yet tested in the tool.

## 6. Proposed next step (not built, awaiting Will)

A "load drone survey" button in `topo.html` that takes a heightfield package (the npy/json above, or a 16-bit PNG heightmap plus bounds) and replaces the fetched public terrain inside the survey footprint, blending at the edge. Two layers: surface (as delivered) and ground (trees stripped), because the grading tool computes cut and fill against existing grade and canopy is not grade. Tree stripping from the heightfield alone: morphological opening (minimum filter over a window larger than a tree crown, then a maximum filter of the same size) followed by smoothing, or a cloth-simulation filter. Any cell whose surface sits well above the ground estimate is canopy.

## 7. Claims and decisions to cross-check

Please check these specifically. Numbered so Will can point at one.

1. The footprint, GSD, and spacing formulas in section 2. In particular the assumption that DJI cameras fly with the long side across-track.
2. The aircraft table. Sensor dimensions, pixel counts, 35 mm equivalents, and rated flight minutes were written from memory. Any wrong number changes the plan for that drone.
3. Deriving real focal length from the 35 mm equivalent (`f = sw * eq / 36`). Is this accurate enough for planning, given that 35 mm equivalents are diagonal-based and sensors are not 3:2?
4. The Litchi CSV column order and semantics, especially `altitudemode 0` = relative to takeoff, `gimbalmode 2` = interpolate, and whether `photo_distinterval` triggers photos on the Mini 2 and Mavic Pro.
5. Which DJI aircraft Litchi (classic) still supports. I stated Mavic Pro, Mavic Pro Platinum, Mavic 2 Pro and Zoom, Mavic Air 2, Air 2S, Mini, Mini 2, and that the newer Mini 3, Mini 4 Pro, Mavic 3 and Air 3 need "Litchi Pilot" or DJI's own waypoints.
6. The WPML structure and whether `droneEnumValue 68` is sensible for anything. Whether any consumer DJI app imports WPML.
7. The FAA rule as stated: 400 ft above ground for both Part 107 and recreational flying. Note that Encino Solo is in Mexico, so Mexican rules (AFAC) apply there, and I did not look them up.
8. The 30% battery reserve and 4 s per turn as planning defaults.
9. The Douglas-Peucker tolerance of 8% of AGL for terrain-following waypoints. Too coarse, too fine?
10. The claim in section 3 that photogrammetry does not need fixed altitude and that constant height above ground is the better default.
11. The georeferencing assumption in section 5: mesh bounding-box centre equals the DroneDeploy LatLonBox centre. Is there a better way to place a DroneDeploy OBJ export without ground control points, for example an offset stored in the export?
12. The vertical anchoring by median difference to a 30 m public DEM. Is there a better reference?
13. Whether the DroneDeploy "Elevation" GeoTIFF really cannot be turned back into heights. I concluded no because the legend exists only as a raster in the PDF.
14. The tree-stripping approach proposed in section 6.

If you find a better approach to any of these, say what it is and why, in plain language. Will is not a programmer; he is a designer and fabricator who runs a university machine shop, and he reads for the decision, not the code.
