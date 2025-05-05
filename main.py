from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class PosesAndImage(BaseModel):
    poses: List[List[float]]
    image: str  # base64-encoded image string

app = FastAPI()

# Enable CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/size/poses_and_image")
async def size_poses_and_image(
    payload: PosesAndImage,       # <-- JSON body according to this schema
    request: Request              # <-- to grab raw bytes if you still want them
):
    """
    Expects JSON: { poses: [...], image: "<base64>" }
    Returns the raw byte length of the request body.
    """
    raw = await request.body()
    return {"size_bytes": len(raw)}

@app.post("/size/base64_image")
async def size_base64_image(
    raw_body: bytes = Body(..., media_type="text/plain")
):
    """
    Expects a raw base64-encoded image string in the request body.
    Returns the byte length of that body.
    """
    return {"size_bytes": len(raw_body)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
