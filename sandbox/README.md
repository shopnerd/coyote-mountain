# coyote mountain sandbox

A depth camera over a box of sand, a projector above it, and the topo tool in a browser. Shape the sand and the
contours, water and rain follow your hands. Load a design and the box shows where to add and remove sand to build it.

Two pieces:

- `bridge.py` reads the camera (Femto Bolt, Azure Kinect, Kinect v1 or an Orbbec Astra / Gemini) and serves depth frames on `http://localhost:8787`. It is the only thing that knows
  about the hardware. Python 3.9 or newer plus numpy; nothing else.
- The topo tool, served by the bridge at `http://localhost:8787/topo.html`, does everything else: floor
  calibration, contours, hydrology, the cut-and-fill wash, and the projector window with a four-corner keystone.

## Camera: Orbbec Femto Bolt

1. Download the Orbbec K4A wrapper for Windows from
   https://github.com/orbbec/OrbbecSDK-K4A-Wrapper/releases (the `_windows_` zip, about 5 MB) and unzip it.
2. Plug the Femto Bolt into a USB 3 port. Run `bin/k4aviewer.exe` from the unzipped folder. If you see a depth
   image, the camera and firmware are fine. If you do not, nothing below will work either, and the fix is the
   camera's firmware (1.1.2 or newer) or the USB port, not the software.
3. Start the bridge, pointing it at that `bin` folder:

       python bridge.py --mode k4a --dll "C:\path\to\OrbbecSDK_K4A_Wrapper\bin"

   `--wide` uses the wide field of view if the box fills more than the narrow one sees.
   You should see `camera streaming narrow`. Open `http://localhost:8787/info` in a browser to check.

Any other camera that speaks the Azure Kinect API works the same way: point `--dll` at its `k4a.dll`.

## Which camera

| camera | price (Oct 2026) | mode | driver |
|---|---|---|---|
| Kinect v1 (Xbox 360, model 1414 or 1473) | $15–40 used, with its USB power adapter | `kinect1` | libfreenect, or Kinect for Windows SDK 1.8 |
| Orbbec Astra+ | about $165 new | `orbbec` | `pyorbbecsdk` 1.x (Python 3.11 or older) |
| Orbbec Astra Mini Pro / Mini S / older Astra | about $150 new, less used | `orbbec` | OpenNI2 |
| Orbbec Astra 2, Gemini 330 series | about $250–350 | `orbbec` | `pyorbbecsdk2` (Python 3.8 to 3.13) |
| Orbbec Femto Bolt / Mega, Azure Kinect | about $400+ | `k4a` (or `orbbec`) | Orbbec K4A wrapper |

All of them see a sandbox of about 1 × 0.75 m from about 1 m above. The Kinect v1 needs at least 0.8 m between camera and
sand; the Astras 0.6 m. The tool's flip x / flip y fix a mirrored picture (the Kinect SDK mirrors; libfreenect doesn't).

## Camera: Kinect v1 (Xbox 360)

The camera most AR sandboxes use. It needs its USB power adapter (the Xbox plug is not USB).

- **Linux** (the UC Davis-style sandbox box): `sudo apt install libfreenect-dev`, then `python3 bridge.py --mode kinect1`.
- **macOS**: `brew install libfreenect`, then `python3 bridge.py --mode kinect1`.
- **Windows, easiest**: install Microsoft's *Kinect for Windows SDK 1.8* (it puts `Kinect10.dll` in Windows), plug the
  Kinect in, then `python bridge.py --mode kinect1`.
- **Windows, open source**: build libfreenect, give the camera's "Xbox NUI Camera" device the libusbK driver with Zadig,
  then `python bridge.py --mode kinect1 --dll "C:\path\to\libfreenect\bin"` (the folder with `freenect_sync.dll`).

The bridge tries libfreenect first, then the Kinect SDK. `/info` names the one in use under `camera`.

## Camera: Orbbec Astra, Gemini or Femto

- **Astra 2, Gemini 330, Femto**: `python -m pip install pyorbbecsdk2` (Python 3.8 to 3.13), then `python bridge.py --mode orbbec`.
- **Astra+ or Astra Pro Plus**: Orbbec's new SDK no longer supports these; use the older package with Python 3.11 or
  older: `py -3.11 -m pip install pyorbbecsdk`, then `py -3.11 bridge.py --mode orbbec`.
- **Astra Mini Pro, Mini S or an older Astra**: these speak OpenNI. `python -m pip install openni`, download Orbbec's
  OpenNI2 package, then `python bridge.py --mode orbbec --dll "C:\path\to\OpenNI2\Redist"` (the folder with `OpenNI2.dll`).

The bridge tries Orbbec's SDK first, then OpenNI2. With no camera attached it says so on `/info` (shown in the tool)
rather than starting the SDK, which crashes outright if no camera is there.

## Without a camera

    python bridge.py --mode fake

serves invented dunes that drift, with a hand passing over the box every twelve seconds. Use it to set up the
projector and learn the controls. `GET /snap` saves the current frame; `--mode replay --file frame-1.bin` plays it back.

## In the topo tool

1. Open **http://localhost:8787/topo.html**. The bridge serves the tool itself, so the whole sandbox runs on one
   machine with no internet. Press **new** for a blank sheet, set the site width to what the box should stand for.
2. Press **sandbox · live**. The rail shows the frame size and the floor height. Flatten the sand and press
   **calibrate floor** once. **flip x** / **flip y** if the projection is mirrored. **box width** is the real width the
   camera sees; **height gain** exaggerates the sand.
3. **sand is the ground**: the box is the site. Press 4 for the analysis view; rain runs when a hand is held over the box.
4. **match the design**: whatever ground is on screen when you press it becomes the target. The wash on the sand shows
   ember where sand must come off and grey where it must go on, and the earthwork line counts what is left to move.
   Load any project first, then match it: a grading design from the tool becomes a thing students build by hand.
5. **projector** opens a second window with the sheet alone. Drag it to the projector screen, press **f** for full
   screen, **k** to show the four corner handles and drag them to the corners of the sand, **r** to reset. The corners
   are remembered.

The camera's image and the projector's throw are two different rectangles. Calibrate the corners once with the
projector showing the sheet, and the contours land on the sand they came from.

## Ports

The bridge listens on 8787. Change it with `--port` and the tool's URL in `SAND.url` at the top of the sandbox
section of `topo.html`.
