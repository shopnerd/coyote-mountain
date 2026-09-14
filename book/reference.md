# Coyote Mountain topo · reference

Every task, tool and control in coyotemountainfarm.com/topo.html, with what each one does. Generated from the tool itself by `book/tools/make-reference.js`, so it matches the page. Run it again after the tool changes.

Generated 2026-09-14.

## Around the drawing

### Top bar

- **project**: save, open, copy a link or start a new project
- **undo**: step back (ctrl+z), 40 steps
- **delete all**: a flat, empty sheet: no ground, no grading, no sketch
- **save**: download this project as a small file
- **new**: start over: a blank flat sheet with default settings, nothing kept (undo brings it back)
- **open**: open a saved project file
- **copy link**: copy a link that opens this place with the current width, rotation, contour interval, units and layers. no file needed
- **redo**: step forward again (ctrl+shift+z)
- **learn**: short chapters on the sample site; your project comes back after each
- **gallery**: pictures, sheets and clips made with the tool
- **flight**: the flight planner, on this place
- **dark**: dark or light around the drawing; the paper stays paper

### Views

- **Plan**: the drawing sheet from above (1)
- **3D**: the model; right drag orbits, the wheel zooms (2)
- **Section**: the ground cut along the section line (3)

### Camera (3D)

- **top**: straight down, north up; orbit again to tilt
- **front**: from the south at eye level: an elevation with the buildings
- **back**: from the north at eye level
- **left**: from the west at eye level
- **right**: from the east at eye level
- **axon**: a 45° corner at the isometric tilt
- **persp**: switch between parallel projection (measurable) and perspective (as the eye sees it)
- **eye**: the camera near the ground, looking in: the section-perspective view

### Layers & look

Opened with the layers & look button over the drawing. Some appear only in 3D or where the site has them.

- **aerial photo**: satellite photo under the plan and on the model
- **no photo**: no satellite photo
- **contour interval**: vertical spacing between contour lines; every fifth one is an index contour
- **labels**: show elevation numbers and labels
- **no labels**: hide every label
- **cut · fill wash**: ember hatching is fill, grey is cut, stronger with depth; the same wash the model shows
- **plain sheet**: no cut and fill wash on the sheet
- **hachures**: how many short downhill ticks between contours; 0 for none
- **read uphill**: contour numbers face uphill, the old drafting convention; off, they simply never read upside down
- **existing dashed**: existing contours dashed wherever the ground has been graded, so proposed reads against existing
- **vertical exaggeration**: stretch heights so relief reads in the model and section; 1 is true
- **show it**: chips on the map for every look or moving picture that is on, each with a way to turn it off
- **hide it**: no strip: looks stay where they were set, as before
- **stops history and rain**: animate history stops when you leave site history, and rain when you leave water; undo on the strip brings it back
- **keeps them running**: history and rain keep running wherever you go, as before
- **points**: the loaded point cloud drawn over the model as dust: every point a speck of its own colour, brighter near the eye, thinner far away. from a drone survey or a lidar file, converted with tools/cloud2bin.py
- **no points**: no points
- **night**: survey points glowing on a dark ground
- **load**: open a points file (.bin from cloud2bin.py). it stays in this browser and reloads with the page; needs real terrain so the points know where they sit
- **paper**: plain paper tones
- **elevation**: green low to ember high
- **slope**: paper flat to ember steep
- **aspect**: which way each slope faces
- **animate history**: every version of the satellite picture this place has had since 2014, played in order: each one rises up the valleys over the last, and the ground that changed between them pulses ember. below, how green the place was each year, from sentinel-2. needs real terrain
- **smooth**: the ground as a continuous surface
- **stepped**: the ground as the cardboard stack you would cut

### Status bar

The place, cut and fill for the whole design, and units, always in sight.

- **units**: imperial or metric, everywhere: sheet, notes, exports

### Learn

Short chapters on a sample site; your own project comes back after each. Some steps wait for you to do the thing.

## Site

Where you are: the place and how much ground, your lot and drone survey, the site through time, the sandbox.

### Site · place

Find a place and fetch its ground; site width sets how much comes in.

*site width sets how much ground is fetched; detail sets the grid; contours are set in layers & look*

| control | what it does |
| --- | --- |
| place or lat, lng (slider) | a place name, or lat, lng. then press fetch |
| fetch terrain | pull real elevation for the place or lat, lng above |
| home | back to the default project |
| site width · area to fetch (slider) | how wide a piece of the world to fetch. wider means coarser ground; it refetches when this changes |
| pick an area on a map | a satellite map around the site: draw a box to fetch a new site that size |
| zoom to a box on the sheet | drag a box over part of the plan and fetch just that ground, in more detail |
| site rotation (slider) | turn the fetched area so a long feature lies along the sheet |
| detail 1× | the standard 150 × 100 grid |
| detail 2× | a 300 × 200 grid: cells half the size, four times the work per redraw. terrain refetches at the finer grid |

### Site · lot and survey

Load your lot boundary, a drone survey or a points file.

| control | what it does |
| --- | --- |
| kml / kmz / geojson | load a lot or property line from a kml, kmz or geojson file, and any image overlay a kmz carries; both stay pinned to their real coordinates |
| drone survey dem | load a drone survey elevation model (GeoTIFF: float or integer heights, in lat/lon, web mercator or UTM; deflate or LZW packed is fine). it replaces the public ground where it has coverage, blended at the edge, and stays on through refetches. drape its orthomosaic with the kml/kmz button |
| load a points file | a point cloud from a drone or scanner, shown in 3d |
| plan a flight | open the flight planner on this place: same width and units, and the lot boundary becomes the survey area |
| clear | remove the boundary |

### Site · site history

Every satellite, landsat and old map picture of the place, oldest first, rising up the ground.

| control | what it does |
| --- | --- |
| animate history | every version of the satellite picture this place has had since 2014, played in order: each one rises up the valleys over the last, and the ground that changed between them pulses ember. below, how green the place was each year, from sentinel-2. needs real terrain |

### Site · field notes

Field notes on the map: photos, soil tests, erosion, vegetation, and readings from rain gauges and probes.

*what you find on the land: notes, photos, soil and erosion checks, and sensor readings over time*

| control | what it does |
| --- | --- |
| what kind (menu) | the kind of observation: a note, a photo, a soil or erosion check, a reading |
| how it was measured (menu) | phone, eye or tape, survey, sensor or lab: it sets how accurate the note is |
| value (box) | the measured value, in the unit shown |
| date (box) | the day it was done |
| note (box) | a few words on what you saw or did |
| add a photo | take or pick a photo; it is shrunk and kept inside the note |
| note it where I stand | place the note at the phone’s position, with its accuracy |
| note it on the plan | tap the plan where the observation was made |
| import readings · csv | a date or time column and a value column, from a rain gauge, moisture probe or level logger; they attach to the highlighted note, or to a new sensor note at the site centre |
| see them in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Site · species surveys

A biodiversity atlas: survey spots and routes, visits with counts, compared fairly by effort and season.

*repeat surveys on fixed spots and routes: what was counted, for how long, in which season*

| control | what it does |
| --- | --- |
| survey method (menu) | how this spot or route is surveyed: point count, walked route, camera, sound or pollinator watch |
| add a survey spot: tap the plan | tap the plan to fix a spot you will survey again and again |
| add a walked route: tap along it | tap along a route you will walk each time you survey |
| sensitive species (box) | species whose places stay private: left out of the survey export |
| see them in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Site · nature records

Plants and animals people have recorded here on iNaturalist, plus bird lists from eBird, Merlin or BirdNET.

*plants and animals recorded on this ground, from iNaturalist, and your own bird lists*

| control | what it does |
| --- | --- |
| fetch iNaturalist observations | observations people have posted on iNaturalist for this ground, the newest thousand |
| which observations (menu) | all, only research grade (confirmed by others), or those still needing an ID |
| import bird records · csv | eBird "download my data" (Merlin checklists end up there) or a BirdNET results file; records outside this site are left out |
| see them in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Site · sandbox

The live sandbox: a table you shape by hand, read and projected back.

| control | what it does |
| --- | --- |
| sandbox · live | live sand: the bridge script reads the depth camera over the sandbox and this page turns it into ground, ten times a second. run python sandbox/bridge.py first |
| projector | the projector window: the plan sheet alone, full screen, warped to the box with k |

## Shape

Change the ground and draw on it: sculpt, pads, grading, paths, plants, sketches and objects.

### Shape · select

Pick a drawing, plant or object on the plan to move, restyle, duplicate or delete it.

*click a drawing, a plant or an object on the plan to pick it; drag to move it*

| control | what it does |
| --- | --- |
| draw it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · sculpt

Raise, lower, smooth or flatten the ground with a brush, in plan or 3d.

*drag on the ground, in plan or 3d*

| control | what it does |
| --- | --- |
| raise | brush that lifts the ground where you drag |
| lower | brush that cuts the ground where you drag |
| smooth | brush that softens bumps and steps |
| flatten | brush that pulls the ground toward the level where you started the stroke |
| radius (slider) | brush size; it scales with the site width |
| strength (slider) | how hard each pass moves the ground |

### Shape · pad

A level pad cut into the hill; cut and fill show in the bottom bar.

| control | what it does |
| --- | --- |
| rect | drag corner to corner |
| oval | drag the box the oval fits in |
| draw | draw the outline freehand; it closes when you let go |
| balance cut and fill | the pad height is found so the cut equals the fill: no earth to bring in or haul off |
| at the start | the pad sits at the ground height where you started the drag |
| pad grade (slider) | tilt the pad along the direction you dragged, for drainage; 0 is dead level |
| slopes | the pad edges run out to daylight at the side slope |
| walls if needed | a retaining wall wherever the edge drops or rises more than 2 ft, slopes elsewhere; the wall is drawn, measured and noted |
| walls | a retaining wall all round: the ground outside stays as it is |
| side slopes (slider) | how the sides of the graded strip meet the ground: 3:1 is three across for one down. fill slopes down, cut slopes up, until they daylight |
| topsoil strip (slider) | topsoil taken off every disturbed area before grading and set aside; reported separately from cut and fill |
| swell (slider) | how much dug earth bulks up when loose; the haul volume uses it |
| draw it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · grade a→b

An even slope from a to b with side slopes.

| control | what it does |
| --- | --- |
| grade (slider) | percent fall from A to B along the grade line; negative rises, 0 makes it level |
| side slopes (slider) | how the sides of the graded strip meet the ground: 3:1 is three across for one down. fill slopes down, cut slopes up, until they daylight |
| draw it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · path

A path or road carved into the ground.

| control | what it does |
| --- | --- |
| path width (slider) | how wide the path is, edge to edge |
| bare | plain edges |
| gravel | the corridor fills with gravel stipple on the sheet |
| paving | the corridor fills with paving on the sheet |
| raise or sink (slider) | raised for a berm or a built-up road, sunk for a trail or a swale; sunk about 6 in is easy to see on a print |
| draw it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · dam and spillway

Dam and spillway: wall height, length and earth, spillway width for the flood, storage ratio, a year of water.

*the wall across the valley at the dam site and the spillway beside it, sized from the pond and the flood: a planning check, not a design*

| control | what it does |
| --- | --- |
| at the keypoint | put the dam where the main valley flattens, the keypoint the water analysis found |
| tap a site | tap the valley floor where the wall should cross; the wall runs across the valley from there |
| full water depth (menu) | how deep the water stands against the wall when the pond is full; the same as the dam height in study · water |
| storm intensity (box) | the heaviest rain the spillway must pass, in a burst as long as the catchment takes to drain: ask the local weather service for the 1 in 50 or 1 in 100 year figure |
| spillway width (menu) | rule of thumb: about the square root of the catchment in hectares, in metres; wider passes the flood shallower and slower |
| freeboard (menu) | height of wall above the flood running over the spillway: at least 1 m in the dam-failure guide; 0.75 to 1 m for small ponds |
| spillway side (menu) | which end of the wall the spillway is cut beside, looking downstream; auto picks the gentler side |
| rain a year (box) | the average yearly rainfall here |
| runoff a year (box) | the share of a year of rain that runs off to the pond: a few percent on dry, open ground (0 to 7.5% where 250 to 400 mm falls, in the dam guide) |
| evaporation (box) | open water lost to the air in a year: up to 2.5 m in hot dry country |
| save the wall line · csv | every quarter cell along the wall: distance, latitude, longitude, ground height and the height of fill, for setting out |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · check dams

Check dams: one-rock dams laid out along a gully, headcut treatments, rock counts, and a log after rain.

*one-rock dams along a gully, Zuni bowls at headcuts and media lunas on sheet flow, laid out for a work day and logged after rain*

| control | what it does |
| --- | --- |
| trace a gully: tap its top, then its bottom | the line follows the water down from the top tap; one-rock dams are laid along it |
| mark a headcut | a step in the gully bed where it is eating back uphill: gets a Zuni bowl or a rundown |
| mark sheet flow for a media luna | a spot where water runs off in a sheet rather than a channel |
| see them in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · steps

Steps up a slope: draw the line, get the risers, treads, stride check and cut and fill.

*a flight of steps up a slope: risers and treads from the ground under a drawn line, checked against an easy stride*

| control | what it does |
| --- | --- |
| draw a flight: tap its centreline | tap where the steps start and where they end, with points between for a bend; the bottom is read from the ground. press again to stop |
| draw in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · plant

Trees, shrubs, hedges, gravel and paving drawn on the plan.

*pick a tree, shrub or hedge to plant, or gravel or paving to fill an area, then draw*

| control | what it does |
| --- | --- |
| tree | tap to plant a tree with a 20 ft canopy, or drag from the trunk to size it. click again for plain ink |
| shrub | shrub mass: trace a bed, or use rect / circ for a clean one. click again for plain ink |
| hedge | hedge row along a line, or around a rect / circ. click again for plain ink |
| gravel | gravel stipple inside a traced or rect / circ area. click again for plain ink |
| paving | flagstone paving inside a traced or rect / circ area. click again for plain ink |
| stroke width (slider) | width of new pen strokes |
| opacity (slider) | ink opacity of new pen strokes |
| draw it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · agroforestry

Orchards, shelterbelts and hedgerows from a species library, grown with a year slider.

*trees and shrubs from a library, grown year by year: canopy, crowding, water, and when they flower and fruit*

| control | what it does |
| --- | --- |
| species (menu) | the tree, shrub or vine to plant, with its typical size and seasons |
| plant one: tap the plan | tap the plan to plant the chosen species; press again to stop |
| plant a row: tap its two ends | tap the two ends of a row; trees are spaced by their mature size |
| row spacing (menu) | how close the row is planted: overlapping as a hedgerow, touching, or open |
| years from planting (box) | grow every library tree to this age, on the plan and in 3d |
| plant in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · sketch

Pen lines, dashes, an eraser and spot heights on the sheet.

| control | what it does |
| --- | --- |
| ink | black pen |
| red | red pen |
| blue | blue pen |
| dash | dashed strokes on or off |
| clear | remove every pen stroke |
| stroke width (slider) | width of new pen strokes |
| opacity (slider) | ink opacity of new pen strokes |
| eraser | rub out pen lines, plants and spot heights where you drag |
| spot height | tap to label the ground height there; it follows later grading |
| smart | freehand that tidies itself on lift: straight lines, circles, boxes, clean polylines |
| free | freehand kept exactly as drawn |
| line | drag a straight line |
| rect | drag a rectangle corner to corner |
| circ | drag a circle from its centre |
| draw it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · grazing

Rotate animals by recovery: paddocks drawn on the terrain, forage, rest and water.

*paddocks, the herd, grazing days and rest, and the next moves as plants recover*

| control | what it does |
| --- | --- |
| herd (menu) | the animals: it sets how much forage a head eats a day |
| head (box) | how many animals in the herd |
| kg of forage a head a day (box) | dry forage one animal eats a day, about 2 to 3% of its weight |
| days of rest (box) | how long a paddock rests before it is ready again |
| share grazed, % (box) | how much of the forage the herd takes; take half, leave half is the usual start |
| draw a paddock: tap its corners | tap the corners of a paddock on the plan |
| mark a water point | tap where a trough, tank or pond is |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · visitor walks

Ecotourism walks routed around sensitive ground, with seasons, limits and costs beside revenue.

*walks and stops for visitors: how hard, where they need care, seasons, limits, and what they cost and bring in*

| control | what it does |
| --- | --- |
| draw a walk: tap along it | tap along the path visitors will walk |
| stewardship cost a month (box) | what trail care, water and sanitation cost a month |
| see them in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Shape · earthwork budget

Price the earthwork, walls, surfaces and planting on this plan with your own rates.

*the grading and planting on this plan, priced with your rates: a likely range, truck trips and diesel*

| control | what it does |
| --- | --- |
| excavation rate (box) | cut in place, dug and moved on site |
| fill, placed and compacted rate (box) | fill in place |
| haul off the surplus rate (box) | loose, after swell |
| bring in fill rate (box) | loose, after swell |
| topsoil strip and respread rate (box) | kept on site for planting |
| retaining walls rate (box) | wall face |
| gravel surfaces rate (box) | paths and areas |
| paving rate (box) | paths and areas |
| trees rate (box) | planted |
| shrub beds rate (box) | bed area |
| hedges rate (box) | length |
| how firm are the prices (menu) | sets the likely range: quoted prices are tight, an early idea is wide |
| currency (box) | the currency sign shown on the budget |
| truck load (box) | how much one truck carries, loose |
| haul distance one way (box) | how far a truck drives to tip or fetch, one way |
| save budget · csv | every line, the total, the range and the trucking, as a spreadsheet |
| example rates again | put back the example rates, replacing your own |

### Shape · object

Place an stl or obj model on the ground.

| control | what it does |
| --- | --- |
| import stl / obj | open an stl or obj (binary or text). files over 40,000 faces are simplified on the way in |
| remove | remove the selected object; the eraser on its centre does the same |
| object units (slider) | what one unit in the file means; cad usually exports millimetres |
| object rotation (slider) | turn the selected object on the sheet |
| object scale (slider) | scale the selected object; 1 is the file as exported |
| lift above ground (slider) | raise the selected object above the ground at its centre, or sink it |
| draw it in plan · 3D | this tool works on the plan; its settings stay here in every view |

## Study

Read the ground: sections, where the water goes, sun and shadow.

### Study · section

Draw a line across the ground in plan, then see it cut in section.

*draw a line across the ground in plan, then look at it in section; the tabs pick which line*

| control | what it does |
| --- | --- |
| draw in plan | go to the plan and drag a line across the ground to cut a section |
| look at it in section | see the ground cut along the section line |

### Study · water

Where water flows, gathers and could be held; rain shows it falling.

| control | what it does |
| --- | --- |
| flow | blue lines where water runs, thicker with more ground feeding them |
| catchments | each outlet's basin, tinted, with its area |
| ridges | dashed ember lines along the ridges |
| keypoints | keypoints: where a valley's steep upper slope eases, the classic small-dam site |
| keyline | the contour through the keypoint plus parallel plow lines in its catchment |
| swales | on-contour ditches stepping down from the keyline |
| dam site | a dam at the keypoint or wherever you place it, with the pond it holds |
| wetness | topographic wetness: where water gathers and lingers, from how much ground drains to each spot and how flat it is; deeper blue is wetter |
| landforms | landforms read from the ground alone, ten kinds: peak, ridge, shoulder, spur, slope, hollow, footslope, valley, pit and flat |
| rain (r) | animated raindrops running downhill and pooling, here and on the model (r) |
| pause | freeze the drops and pools (p) |
| tap: keyline | a tap on the sheet sets the keyline point |
| tap: dam | a tap on the sheet places the dam |
| storm rain (slider) | rain falling on the whole site in one storm; the runoff share says how much of it runs rather than soaks in |
| stream threshold (slider) | how much upstream ground it takes to count as a stream |
| runoff share (slider) | the share of storm rain that runs over the ground; the rest soaks in. flood and rain volumes use it |
| plow spacing (slider) | distance between plow lines, measured on the ground |
| swale drop (slider) | vertical drop from one swale to the next |
| dam height (slider) | wall height of the dam; the pond fills to its crest |

### Study · sun

Sun and shadow through the day and the year.

| control | what it does |
| --- | --- |
| sun study | shadows at an hour, or sun hours per day, for the site's latitude |

### Study · water budget

How much water the design holds from a storm and a year, against what the planting needs.

*one storm and one year on this ground: what soaks in, what the hollows, ponds, swales and tanks hold, and what leaves*

| control | what it does |
| --- | --- |
| storm rain (slider) | rain falling on the whole site in one storm; the runoff share says how much of it runs rather than soaks in |
| runoff share (slider) | the share of storm rain that runs over the ground; the rest soaks in. flood and rain volumes use it |
| rain in a year, in (box) | the long-run average rain for the place |
| swale holds, ft² of cross-section (box) | the water a length of swale holds: width times depth, roughly halved |
| water tanks (box) | tanks fed by a roof, and the size of each |
| each tank, gal (box) | tanks fed by a roof, and the size of each |
| roof feeding tanks, ft² (box) | the roof area that drains into the tanks |
| each tree, gal a week (box) | water one established tree needs a week |
| shrub beds, gal per ft² a week (box) | water a unit of shrub bed needs a week |
| dry weeks a year (box) | how many weeks a year the planting depends on stored water |
| keep as A | remember this design’s water numbers to compare with another |
| keep as B | remember this design’s water numbers to compare with another |
| clear | forget what was kept or loaded here |

### Study · what grows where

What grows where: each plant in the library read against slope, sun side, wetness and frost pockets, as zones on the plan.

*which plants in the library suit which ground: slope, the sunny or shaded side, where water gathers, where frost settles*

| control | what it does |
| --- | --- |
| ground zones | the site split into kinds of ground, each named with the plants that suit it best |
| one plant | how well one plant suits each part of the site |
| rain only | plants that need water do best where water gathers |
| with watering | as if every plant is watered: slope, sun side, frost and drainage still count |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Study · landscape fit

Suitability: hard limits never traded, preferences weighed, the three best spots and their tradeoffs.

*where an orchard, road, basin, classroom or building fits with the least conflict, limits kept firm*

| control | what it does |
| --- | --- |
| what to place (menu) | what you are looking for a place for; each has its own size and limits |
| draw a protected area: tap its corners | woodland, a spring, nesting ground: somewhere nothing goes, whatever it would score. recovery areas and paddocks left ungrazed count too |
| import protected areas · geojson or kml | protected polygons from a geojson or kml file |
| weigh sun (menu) | how much a sunny, sun-facing spot matters |
| weigh low, wetter ground (menu) | how much low, wetter ground matters, or should be avoided |
| weigh high ground and views (menu) | how much raised ground with views matters |
| weigh near water (menu) | how much being near water or a stream matters |
| weigh near a road (menu) | how much being near a mapped road matters |
| weigh low fire risk (menu) | how much a low fire risk matters |
| show fit | show the fit wash and the best spots on the plan |
| hide | hide this layer on the plan |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Study · recovery

Plan and track the recovery of eroded, bare or damaged ground against goals and an untreated comparison.

*damaged ground brought back: goals, treatments, measurements over time and an untreated patch to compare*

| control | what it does |
| --- | --- |
| draw a recovery area: tap its corners | tap the corners of damaged ground to treat, or of a similar patch left alone to compare |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Study · fire ready

A wildfire planning layer: slope, sunny sides, wind and cover, with defensible space around buildings.

*where fire would run hardest, and the defensible space each building needs*

| control | what it does |
| --- | --- |
| wind from (menu) | the dangerous wind for the place; Santa Ana winds come from the east and northeast |
| ground cover (menu) | what mostly covers the ground: it sets how hard fire would burn |
| mark a building | tap the plan where a house, barn or shed stands |
| show on plan | show this layer on the plan |
| hide | hide this layer on the plan |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Study · carbon

A carbon and biomass ledger: estimates as ranges, soil samples as measurements.

*carbon the planting may store over 30 years, as a range, beside soil carbon measured*

| control | what it does |
| --- | --- |
| sample depth, cm (box) | how deep the soil samples were taken |
| soil density, g/cm³ (box) | soil bulk density; a lab measures it from a core of known volume |
| save carbon ledger · csv | the carbon range by year and the soil samples, marked estimate or measured |

### Study · ground change

Compare two drone surveys: where soil was lost, where it built up, and how much.

*two drone surveys of the same ground, before and after: ember where soil was lost, blue where it built up*

| control | what it does |
| --- | --- |
| before survey | the drone survey flown before: a storm, a season or the earthwork |
| after survey | the drone survey flown after |
| line up heights | remove the height drift between two flights, using the ground that did not move |
| heights as flown | compare the surveys exactly as they came |
| ignore changes under (slider) | differences smaller than this are survey noise, not change |
| change wash | show where soil was lost (ember) and built up (blue) |
| hide | hide this layer on the plan |
| clear | forget what was kept or loaded here |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

## Make

Turn the site into pictures, video, drawing sheets, 3d prints, laser-cut models and files.

*pictures and sheets*

### Make · render

The model with real sun, sky and a section cut.

| control | what it does |
| --- | --- |
| model · 3D | the working model: paper tones, contour lines, labels |

### Make · paint

A painted picture of the 3d view by an ai painter.

| control | what it does |
| --- | --- |
| plain · 3D | the render as drawn |
| photograph · 3D | painted as a photograph |
| watercolour · 3D | painted as a loose watercolour over ink |
| ink wash · 3D | painted as an ink wash, a few tones, no colour |
| map mash-up · 3D | the surface colour stays as the data map it is, and real vegetation, buildings, water and shadows are painted standing on it |
| white model · 3D | a photograph of a white card model: ground and buildings matte white with the contour steps, only the planting and the water painted in |

### Make · landscape story

One captioned video of the place: today, the ground, the water, the design and the planting growing.

*the place told in chapters: today, the ground, the water, the design, the planting growing, with your captions, as one video*

| control | what it does |
| --- | --- |
| title card (box) | tick to include this chapter in the story |
| caption for title card (box) | the words shown on this chapter of the story |
| today, with the photo (box) | tick to include this chapter in the story |
| caption for today, with the photo (box) | the words shown on this chapter of the story |
| the ground in 3d, turning (box) | tick to include this chapter in the story |
| caption for the ground in 3d, turning (box) | the words shown on this chapter of the story |
| the water (box) | tick to include this chapter in the story |
| caption for the water (box) | the words shown on this chapter of the story |
| the design and its earthwork (box) | tick to include this chapter in the story |
| caption for the design and its earthwork (box) | the words shown on this chapter of the story |
| the planting growing 0 to 15 years (box) | tick to include this chapter in the story |
| caption for the planting growing 0 to 15 years (box) | the words shown on this chapter of the story |
| the history pictures (load them first) (box) | tick to include this chapter in the story |
| caption for the history pictures (load them first) (box) | the words shown on this chapter of the story |
| closing card (box) | tick to include this chapter in the story |
| caption for closing card (box) | the words shown on this chapter of the story |
| play the story | play the ticked chapters with their captions; press again to stop |
| record the story · video | play the story and save it as one video with the captions in it |
| chapters as they were | put the chapters and captions back to how they started |

### Make · video

Record the view as a video, or animate the section.

*record video captures the view until you press it again*

| control | what it does |
| --- | --- |
| record video | record the view as a video; press again to stop and save it |
| animate the section | play the section line sweeping across the site |

### Make · drawing sheet

A drawing sheet: plan, model and section with a title block.

*the preview draws the sheet without painting; the export paints it when a painter key is set*

| control | what it does |
| --- | --- |
| paper (slider) | paper size for the drawing sheet set |
| model picture (slider) | the model picture on the sheet: the render, or the ground drawn only in lines laid over it (straight rows, rays from one point, or crossing diagonals) |
| lines (slider) | how many lines the line drawing lays over the ground |
| line height (slider) | how much the line drawing stretches the heights, so gentle ground still reads |
| save the line drawing · png | the line drawing on its own, large, as a png |
| drawing sheet · pdf + png | the drawing sheet: the model as it stands and the active section, both painted in the chosen style, over the plan, the analysis and the notes at true scale, with the title block. two calls to the painter; without a key the two pictures are drawn instead |
| save png | save the current view as an image |
| preview | draw the result here before exporting |

### Make · line drawings

Line drawings: nine ways to draw the site only in lines, in separate layers and inks, as a png, plates or a layered svg for a pen plotter.

*the site in lines and layers: rows, rays, water, terraces, sun, keyline, before and after, a section fan; png, plates and a plotter svg*

| control | what it does |
| --- | --- |
| style (menu) | straight rows, rays from a point and crisscross lay lines over the ground; water lines follow the drops downhill; stacked contours step the ground into terraces; sun lines shade with line density; keyline pattern runs parallel to the keyline; before and after overlays two grounds; section fan stacks sections turning about one point |
| lines (menu) | how many lines, contour steps or sections |
| height × (menu) | how much the heights are stretched, so gentle ground still reads |
| from the south | the ground seen from the south and above, nearer ground hiding what is behind |
| in plan | straight down, as a map |
| terrain (menu) | the ink for this layer; each layer is separate in the svg and as a plate |
| water (menu) | the stream network as its own layer, heavier where more water gathers |
| design (menu) | paths, planting, sketches, the lot line, steps, check dam gullies and the keyline, as their own layer |
| paper (menu) | the page the drawing and the svg are sized to, in millimetres |
| landscape | the page on its side |
| portrait | the page upright |
| save png | the whole drawing in its inks, 3600 px wide |
| save svg · plotter layers | every layer as its own layer, in millimetres at the paper size, a 0.3 mm pen: for a pen plotter, a laser or cnc engraving, or inkscape |
| save each layer as a plate | one black-on-white png per layer, aligned, for risograph or screen printing one ink at a time |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

*physical models*

### Make · 3d print

The site as a solid model for a 3d printer.

| control | what it does |
| --- | --- |
| scale (slider) | how much the site shrinks to become the object, and how wide it comes out |
| 3d model (slider) | which file the model export writes. stl is the solid to print. obj, glb and wrl carry the ground as a texture: the photo, the painted ground, or the surface colour showing on the model, with the base in plain paper. glb is one file in metres; obj and wrl come zipped with their picture |
| export stl | the model on its base slab at the fabricate scale, written in the file chosen above |
| preview | draw the result here before exporting |

### Make · laser-cut model

Contour layers nested on sheets for a laser cutter.

| control | what it does |
| --- | --- |
| scale (slider) | how much the site shrinks to become the object, and how wide it comes out |
| material thickness (slider) | thickness of the cardboard or plywood you will cut |
| sheet (slider) | the laser bed in mm; layers get nested onto sheets this size |
| hollow layers (slider) | hollow each layer, leaving a ledge this wide for the next one to sit on; 0 keeps them solid |
| export laser | cardboard layers nested on sheets for the laser cutter |
| dxf | the same laser file as a DXF in millimetres: layers CUT (red), ENGRAVE (blue), MATERIAL (yellow); for laser software that takes DXF better than SVG |
| preview | draw the result here before exporting |

*in the field*

### Make · walk the line

Follow a designed line on the ground with your phone and flag it.

*walk a keyline, swale, path or lot line with your phone, and drop flags on the ground*

| control | what it does |
| --- | --- |
| which lines (menu) | the kind of line to walk: keyline and swales, paths, drawn lines or the lot line |
| line to walk (menu) | the one line to follow now |
| follow my position | use the phone’s position to show how far you are from the line |
| no gps here? tap the plan to stand | tap the plan to stand somewhere, to try it without a position |
| drop a flag here | mark where you stand; flags save with the project |
| target grade % (box) | 0 for a swale on contour; 0.5 to 1% for a drain |
| use the phone as a level | lay the phone along a straight board to read its tilt |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

### Make · field build

Grade stakes, landxml surfaces for machine control, keep-out zones and the as-built check.

*stake the grading, hand the surfaces to machine control, keep out of protected ground, and check what was built*

| control | what it does |
| --- | --- |
| stake spacing (menu) | how far apart the grade stakes are |
| stakes · csv | every stake with lat, lon, utm, existing and design height and cut or fill |
| stakes · gpx | the stakes as waypoints, named with their cut or fill |
| design surface · landxml | the designed ground as a surface for machine control |
| existing surface · landxml | the ground as it is now, as a surface for machine control |
| keep-out zones · kml (0) | protected, recovery and ungrazed ground, to set out before digging |
| check an as-built survey against the design | open ground change to compare what was built with the design |
| show stakes | show the stakes on the plan |
| hide | hide this layer on the plan |
| see it in plan · 3D | this tool works on the plan; its settings stay here in every view |

*files*

### Make · cnc and maps

Cnc lines, google earth kml and a geotiff for maps.

| control | what it does |
| --- | --- |
| scale (slider) | how much the site shrinks to become the object, and how wide it comes out |
| cnc lines · dxf | a dxf at the model's scale, in inches or millimetres to match the units setting: site edge, contours, building footprints, path edges, lot line, on their own layers. for engraving on the cnc, or any cad |
| kml | the drawing at its real coordinates: contours with heights, lot, buildings, paths, pen lines, trees, sections, spots and placed objects, in folders; opens in google earth or any gis |
| geotiff | the graded ground as a geotiff: one height per cell in metres, georeferenced; opens in any gis, and in cad that reads rasters |

## Keys

- **1 · 2 · 3**: plan, 3D, section
- **/**: find a tool
- **ctrl+z · ctrl+shift+z or ctrl+y**: undo, redo
- **r**: rain in study · water
- **0**: fit the drawing to the window

## Flight planner

coyotemountainfarm.com/flight.html plans drone survey flights for the ground models the topo tool reads. Its tasks:

### Area

- **site**: type a place or lat, lng and fetch the terrain; site width sets how much ground comes in
  - place or lat, lng: a place name, or lat, lng, then fetch the terrain
  - fetch terrain: pull the real ground for the place above
  - home: Encino Solo
  - site width · area to fetch: how wide a piece of ground to fetch around the place
  - pick an area on a map: a satellite map around the site: draw a box to fetch a new site that size
  - aerial photo: the satellite photo under the plan, or shaded relief of the ground
  - shaded relief: the satellite photo under the plan, or shaded relief of the ground
- **survey area**: click the corners on the map and double-click to close; takeoff places the home point
  - draw: click to add corners (d)
  - takeoff: click to place the takeoff point (t)
  - pan: drag to pan (p)
  - clear area: delete the survey area and start over
  - undo corner: remove the last corner (backspace)
  - kml / kmz / geojson: a polygon from Google Earth or a GIS export becomes the survey area
  - fit terrain: recentre the terrain on the survey area and refetch at a fitting width
- **drone survey**: your own elevation model replaces the public ground where it has coverage
  - drone survey dem: load a drone survey elevation model (GeoTIFF from DroneDeploy, Pix4D, WebODM, Metashape; lat/lon, web mercator or UTM). it replaces the public ground where it has coverage and stays on through refetches. use the surface (dsm) file so trees and roofs count as ground to clear
  - open in topo: open the topo tool on this place: same width and units, and the survey area becomes the lot boundary there

### Aircraft

- **drone and camera**: the sensor and rated flight time drive every number in the plan
  - drone: the aircraft and its camera: they set every number in the plan

### Flight

- **height and overlap**: height and the two overlaps set line spacing, photo spacing and ground sample
  - altitude above ground: height above the ground under the drone; the exports convert it to height above the takeoff point
  - front overlap: how much each photo overlaps the one before it along the line
  - side overlap: how much neighbouring lines overlap
  - follow terrain: every waypoint climbs and descends with the ground so the height above ground stays constant
  - fixed altitude: one altitude above the takeoff point, the way a plain waypoint mission flies
- **lines and speed**
  - line heading: the direction the flight lines run; auto picks the longest side of the area
  - auto heading: lines run along the longest edge of the area
  - speed: how fast the drone flies along each line
  - single grid: one set of parallel lines: the standard for maps and elevation models
  - crosshatch: a second set at 90°: better for 3d models of buildings and steep ground
  - gimbal pitch: -90 looks straight down; tilt it for crosshatch 3d work

### Plan

- **plan**
- **export**: kml and geojson for maps, litchi csv for the older aircraft, dji fly kmz for the newer ones; aircraft says which flies yours
  - export kml: the survey area, the flight path with absolute altitudes, every waypoint and photo point; opens in Google Earth
  - geojson: the same plan as geojson for QGIS or any GIS
  - litchi csv: waypoint mission for classic Litchi: Mavic Pro and 2, Air 2 and 2S, Mini 1, 2 and SE. Mini 3 family flies from Litchi Pilot; Mavic 3 and newer from DJI Fly or Litchi Hub, use the kmz. altitudes relative to takeoff, a photo every photo-spacing metres
  - dji fly kmz: DJI's WPML mission file (kmz), the format DJI Fly imports on the Mavic 3, Air 3 and Mini 4 Pro and Litchi Hub passes through. experimental: written to DJI's published format, not yet flown on a real aircraft. altitudes relative to takeoff
  - save png: save the plan as an image

---
Coyote Mountain · free for learning and the commons · PolyForm Noncommercial 1.0.0
