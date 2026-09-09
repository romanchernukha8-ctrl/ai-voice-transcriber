import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("Waiting for an audio file...");
  const [transcription, setTranscription] = useState(
    "Your transcription will appear here.",
  );
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setStatus("Ready to upload");
      setTranscription("Your transcription will appear here.");
    }
  };

  const handleUpload = async () => {
    if (!file || uploading) {
      return;
    }

    setUploading(true);
    setStatus("Uploading...");
    setTranscription("Waiting for transcription...");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const uploadResponse = await fetch("/api/v1/files/upload", {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error("Upload failed");
      }

      const uploadedFile = await uploadResponse.json();
      const fileId = uploadedFile.id;

      setStatus("Processing...");

      let completed = false;

      while (!completed) {
        await new Promise((resolve) => setTimeout(resolve, 2000));

        const transcriptionResponse = await fetch(
          `/api/v1/files/${fileId}/transcription`,
        );

        if (transcriptionResponse.ok) {
          const result = await transcriptionResponse.json();

          setTranscription(result.text);
          setStatus("Completed");
          completed = true;
        } else if (transcriptionResponse.status === 404) {
          setStatus("Processing...");
        } else {
          throw new Error("Failed to get transcription");
        }
      }
    } catch (error) {
      console.error(error);
      setStatus("Failed");
      setTranscription("Something went wrong.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="app">
      <main className="container">
        <header className="header">
          <h1>AI Voice Transcriber</h1>
          <p>Upload an audio file and get its transcription.</p>
        </header>

        <section className="upload-card">
          <label htmlFor="audio-file" className="file-label">
            Choose audio file
          </label>

          <input
            id="audio-file"
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
            disabled={uploading}
          />

          {file && (
            <div className="selected-file">
              <span>Selected file:</span>
              <strong>{file.name}</strong>
            </div>
          )}

          <button
            type="button"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? "Processing..." : "Upload"}
          </button>
        </section>

        <section className="status-card">
          <h2>Status</h2>
          <p>{status}</p>
        </section>

        <section className="transcription-card">
          <h2>Transcription</h2>
          <div className="transcription-text">{transcription}</div>
        </section>
      </main>
    </div>
  );
}

export default App;
