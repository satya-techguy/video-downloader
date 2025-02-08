from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path

router = APIRouter()

# Define the downloads directory
BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"

# Ensure the downloads directory exists
DOWNLOAD_DIR.mkdir(exist_ok=True)

@router.get("/files/{filename}")
async def get_file(filename: str):
    file_path = DOWNLOAD_DIR / filename

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(str(file_path), media_type="application/octet-stream", filename=filename)
