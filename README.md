# Car to Robot: 3D Transformation Simulator

An interactive 3D simulation of a car that transforms into a standing humanoid robot, running in the browser.

I designed the mechanism in **Onshape** as a set of simple rectangular blocks (torso, legs, two arms), exported it as a `.glb` file, and wrote a web viewer that animates the transformation with a rig computed from the geometry of the model.

Live demo: https://beldjilalibouchraa.github.io/car-to-robot-simulator/

## What it does

- Shows the model as a **car lying flat**, with its largest face on the ground.
- One button, **Transform to Robot / Transform to Car**, plays the animation forwards or backwards.
- Lets you orbit, pan and zoom the 3D view with the mouse.

### Transformation sequence

| Phase | Part | Motion |
|-------|------|--------|
| 1 | Legs | Tip forward around the foot edge until they stand upright on the ground |
| 2 | Torso | Swings up around the hip until it stands on top of the legs |
| 3 | Arms | Swing 45° sideways, away from the torso |

Playing it in reverse folds the arms first, then the torso, then the legs.

## How it works

1. **CAD:** the mechanism is modelled in Onshape. Each moving part is a separate component (`dof_legs`, `dof_torso`, `dof_right_arm`, `dof_left_arm`) and the assembly is exported as `models/robot.glb`.
2. **Backend:** a small [FastAPI](https://fastapi.tiangolo.com/) server (`main.py`) serves the page and the model file.
3. **Viewer:** `index.html` uses [Three.js](https://threejs.org/) (WebGL) to load the model and animate it.
4. **Automatic rig:** a GLB file only contains geometry, not the joints defined in CAD. So the viewer measures the bounding box of each block and works out:
   - which side of the model is the thinnest (this becomes "up", so the car lies on its largest face),
   - where the foot edge, the hip and the shoulders are,
   - which way each arm has to rotate to swing away from the torso.

   Each part is placed in a pivot group on its hinge point, so it rotates around the correct point and stays attached to its neighbour. Parts are chained (legs, then torso, then arms on the torso), which is what makes the motion look like a real linkage.

This is a **kinematic animation** (the motion is defined by joint angles). It is not a physics simulation.

## Tech stack

- **Python 3** with **FastAPI** and **Uvicorn** (server)
- **JavaScript** with **Three.js** (3D rendering, loaded from a CDN)
- **HTML / CSS** (interface)
- **Onshape** (CAD design) and **glTF Binary** (`.glb`) as the exchange format

## Project structure

```
car-to-robot-simulator/
├── README.md
├── requirements.txt
├── main.py              # FastAPI server
├── index.html           # 3D viewer, rig and animation
├── models/
│   └── robot.glb        # CAD model exported from Onshape
```

## Run it locally

You need Python 3.9 or newer and an internet connection (Three.js is loaded from a CDN).

```bash
# 1. clone the repository
git clone https://github.com/<your-username>/car-to-robot-simulator.git
cd car-to-robot-simulator

# 2. (optional) create a virtual environment
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

# 3. install the dependencies
pip install -r requirements.txt

# 4. start the server
python main.py
```

Then open **http://127.0.0.1:8000** in your browser.

> Open the page through the server. Double-clicking `index.html` will not work, because browsers block loading the model file that way.

### Hosting (GitHub Pages)

The viewer only needs static files, so the Python server is optional. The live demo is served directly by GitHub Pages from the `main` branch (Settings, Pages, "Deploy from a branch", `main` / root). FastAPI is only used for local development.

A health check is available at `http://127.0.0.1:8000/health`.

## Settings

All settings are at the top of the script in `index.html`:

| Setting | Meaning |
|---------|---------|
| `DURATION_MS` | Total animation time |
| `ARM_ANGLE_DEG` | How far the arms swing away from the body (default 45) |
| `SPANS` | When the legs, torso and arms move during the animation |
| `FLIP_UPSIDE_DOWN` | Turn the car over if it starts on the wrong face |
| `FLIP_STAND_DIRECTION` | Swap the standing direction if the robot stands upside down |
| `UP_AXIS` | Force the axis that becomes the robot's height (`auto`, `x` or `z`) |

## What I learned

- Designing a simple mechanism with revolute joints in CAD (Onshape).
- Why exported 3D models lose their joints, and how to rebuild the kinematics from geometry.
- Rotations in 3D: pivot points, rotation axes, quaternions and chained transforms.
- Building a small client-server web application with FastAPI and Three.js.

## Possible improvements

- Add wheels and a proper car body.
- Add physics (for example with PyBullet) so the robot balances.
- Smoother, more realistic motion curves and sound.
- A live demo hosted online.

## Author

**<Beldjilali Bouchra>**

## License

Released under the MIT License. See `LICENSE` if included, or replace this section with the license you prefer.
