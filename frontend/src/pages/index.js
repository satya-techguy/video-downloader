import { useState } from "react";

export default function Home() {
    const [url, setUrl] = useState("");
    const [format, setFormat] = useState("mp4");
    const [downloadUrl, setDownloadUrl] = useState("");

    const handleDownload = async () => {
        const response = await fetch("http://localhost:8000/download", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url, format }),
        });

        const data = await response.json();
        if (response.ok) {
            setDownloadUrl(data.download_url);
            // Automatically trigger download
            window.location.href = data.download_url;
        } else {
            alert(`Error: ${data.detail}`);
        }
    };

    return (
        <div style={{ textAlign: "center", padding: "50px" }}>
            <h1>Video Downloader</h1>
            <input 
                type="text" 
                placeholder="Enter video URL" 
                value={url} 
                onChange={(e) => setUrl(e.target.value)} 
                style={{ width: "300px", padding: "10px" }}
            />
            <select value={format} onChange={(e) => setFormat(e.target.value)}>
                <option value="mp4">MP4</option>
                <option value="mp3">MP3</option>
            </select>
            <button onClick={handleDownload} style={{ marginLeft: "10px", padding: "10px 20px" }}>
                Download
            </button>
            {downloadUrl && (
                <p>
                    Your file is downloading... If it doesn’t start, <a href={downloadUrl} download>click here</a>.
                </p>
            )}
        </div>
    );
}
