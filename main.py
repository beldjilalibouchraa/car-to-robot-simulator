import mimetypes
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Make sure .glb files are served with the correct content type
mimetypes.add_type("model/gltf-binary", ".glb")

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "robot.glb"

MODEL_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Car to Robot Simulator")


class NoCacheStaticFiles(StaticFiles):
    """Static files without browser caching, so a re-exported GLB always reloads."""

    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-store"
        return response


app.mount("/models", NoCacheStaticFiles(directory=str(MODEL_DIR)), name="models")


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html", headers={"Cache-Control": "no-store"})


@app.get("/health")
def health():
    found = MODEL_FILE.exists()
    return {
        "status": "running",
        "project": "Car to Robot Simulator",
        "model_found": found,
        "model_size_kb": round(MODEL_FILE.stat().st_size / 1024, 1) if found else None,
    }


if __name__ == "__main__":
    if not MODEL_FILE.exists():
        print(f"WARNING: {MODEL_FILE} not found. Put your exported file there and name it robot.glb")
    print("Open http://127.0.0.1:8000")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)