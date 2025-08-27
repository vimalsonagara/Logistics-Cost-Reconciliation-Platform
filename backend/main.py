from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import routes_upload
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI(title="Logistics Cost Reconciliation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files (JS, CSS, etc.) from /static
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ✅ Serve the main HTML file on root "/"
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return Path("frontend/index.html").read_text()
app.include_router(routes_upload.router, prefix="/upload", tags=["Upload"])

# @app.get("/")
# def health():
#     return {"status": "ok"}
