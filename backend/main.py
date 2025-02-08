import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI()

# Allow frontend access (update origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the directory where downloaded files are stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get current directory
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")  # Ensure it looks inside 'backend/downloads'

# Ensure download directory exists
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.get("/files/{filename}")
def get_file(filename: str):
    """Download a file from the 'downloads' directory."""
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    
    # Check if file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Serve file as a download
    return FileResponse(
        file_path,
        filename=filename,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/status")
def status():
    """Check if API is running."""
    return {"message": "API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
