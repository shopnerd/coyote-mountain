# Field card 12 · Fly a drone survey

Photos from a drone, turned into an elevation model of the ground, for grading design, ground change and as-built checks.

**People:** 2 (a pilot and a spotter)  
**Tool:** coyotemountainfarm.com/flight.html, then photogrammetry software  

## Plan it

1. **Area · site:** fetch the place. **Survey area:** click the corners, or **pick an area on a map**.
2. **Aircraft · drone and camera:** your drone.
3. **Flight · height and overlap:** 80% front and 70% side overlap are good for ground models. Lower flying gives more detail and more photos.
4. **Plan:** check the photos, time and batteries.
5. **Export:** dji fly kmz for newer DJI drones, litchi csv for older ones. The aircraft panel says which yours takes.

## Before flying

- Check the local rules for flying drones and any permission you need.
- Check wind, light and batteries. Overcast, even light gives the best models.
- For heights you can trust between surveys, set out ground control points (marked targets measured with a survey GPS) and note their positions.

## Fly

1. Load the mission, fly it, keep the drone in sight.
2. Swap batteries where the plan says. The mission resumes.

## Make the elevation model

1. Load the photos into photogrammetry software.
2. Export a **terrain model (DTM)** as a GeoTIFF, in lat/lon, web mercator or UTM. A surface model (DSM) includes plants and roofs; use the DTM for ground.
3. Site · lot and survey · **drone survey dem** loads it onto the plan.

## Good to know

- For comparing surveys (card 13), fly the same way each time: same height, overlap, season and time of day.
- Without ground control, heights drift between flights. The tool's **line up heights** corrects most of it, but ground control is better.

## Done when

The GeoTIFF loads and covers the site.

---
Coyote Mountain · free for learning and the commons · PolyForm Noncommercial 1.0.0
