from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI()

# Directory to store downloads
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class VideoRequest(BaseModel):
    url: str
    format: str = "mp4"

@app.post("/download")
def download_video(request: VideoRequest):
    video_url = request.url
    format_type = request.format
    
    # Generate a unique filename
    filename = f"{uuid.uuid4()}.{format_type}"
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    
    # yt-dlp options
    ydl_opts = {
        'format': 'best',
        'outtmpl': filepath,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # Return a direct download link
        return {
            "message": "Download successful",
            "download_url": f"http://localhost:8000/files/{filename}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{filename}")
def get_file(filename: str):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path, 
        filename=filename, 
        media_type="application/octet-stream",  # Forces download
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/status")
def status():
    return {"message": "API is running"}
