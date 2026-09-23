import { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("Waiting for an audio file...");
  const [language, setLanguage] = useState("");
  const [transcription, setTranscription] = useState(
    "Your transcription will appear here.",
  );
  const [processing, setProcessing] = useState(false);

  const [assistantResult, setAssistantResult] = useState(
    "AI assistant response will appear here.",
  );
  const [question, setQuestion] = useState("");
  const [assistantLoading, setAssistantLoading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile) {
      setFile(selectedFile);
      setStatus("Ready to upload");
      setLanguage("");
      setTranscription("Your transcription will appear here.");
      setAssistantResult("AI assistant response will appear here.");
      setQuestion("");
    }
  };

  const handleUpload = async () => {
    if (!file || processing) {
      return;
    }

    setProcessing(true);
    setStatus("Uploading...");
    setLanguage("");
    setTranscription("Waiting for transcription...");
    setAssistantResult("AI assistant response will appear here.");
    setQuestion("");

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

      const maxAttempts = 150;

      for (let attempt = 0; attempt < maxAttempts; attempt++) {
        await new Promise((resolve) => setTimeout(resolve, 2000));

        const transcriptionResponse = await fetch(
          `/api/v1/files/${fileId}/transcription`,
        );

        if (transcriptionResponse.ok) {
          const result = await transcriptionResponse.json();

          setLanguage(result.language || "");
          setTranscription(result.text);
          setStatus("Completed");
          setProcessing(false);

          return;
        }

        if (transcriptionResponse.status === 404) {
          setStatus("Processing...");
          continue;
        }

        throw new Error("Failed to get transcription");
      }

      throw new Error("Transcription timeout");
    } catch (error) {
      console.error(error);
      setStatus("Failed");
      setTranscription("Something went wrong.");
    } finally {
      setProcessing(false);
    }
  };

  const hasTranscription =
    transcription &&
    transcription !== "Your transcription will appear here." &&
    transcription !== "Waiting for transcription..." &&
    transcription !== "Something went wrong.";

  const handleCopy = async () => {
    if (!hasTranscription) return;

    try {
      await navigator.clipboard.writeText(transcription);
    } catch (error) {
      console.error("Copy failed:", error);
    }
  };

  const handleDownload = () => {
    if (!hasTranscription) return;

    const blob = new Blob([transcription], {
      type: "text/plain;charset=utf-8",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = file
      ? `${file.name.replace(/\.[^/.]+$/, "")}.txt`
      : "transcription.txt";

    document.body.appendChild(link);
    link.click();
    link.remove();

    URL.revokeObjectURL(url);
  };

  const handleSummarize = async () => {
    if (!hasTranscription || assistantLoading) {
      return;
    }

    setAssistantLoading(true);
    setAssistantResult("Generating summary...");

    try {
      const response = await fetch("/ai/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: `You are a transcription assistant.

Your task is to summarize the provided transcription.

IMPORTANT RULES:
- Use ONLY information explicitly present in the transcription.
- Do NOT invent or assume any facts.
- Do NOT add information from your own knowledge.
- Do NOT invent people, companies, products, events, dates, numbers, or intentions.
- If the transcription is unclear or incomplete, say so.
- Keep the summary concise and factual.
- Focus on the main topic, important points, decisions, and conclusions.

TRANSCRIPTION:
${transcription}

SUMMARY:`,
        }),
      });

      if (!response.ok) {
        throw new Error("AI request failed");
      }

      const data = await response.json();
      setAssistantResult(data.response);
    } catch (error) {
      console.error(error);
      setAssistantResult("Failed to get a response from AI.");
    } finally {
      setAssistantLoading(false);
    }
  };

  const handleAskAI = async () => {
    if (!hasTranscription || !question.trim() || assistantLoading) {
      return;
    }

    setAssistantLoading(true);
    setAssistantResult("AI is thinking...");

    try {
      const response = await fetch("/ai/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: `You are an assistant that answers questions about a transcription.

IMPORTANT RULES:
- Answer ONLY using information explicitly contained in the transcription.
- Do NOT use outside knowledge.
- Do NOT guess or invent information.
- If the answer is not present in the transcription, say:
  "The transcription does not contain this information."
- If the transcription is unclear, say that it is unclear.
- Keep the answer concise and factual.

TRANSCRIPTION:
${transcription}

USER QUESTION:
${question}

ANSWER:`,
        }),
      });

      if (!response.ok) {
        throw new Error("AI request failed");
      }

      const data = await response.json();
      setAssistantResult(data.response);
    } catch (error) {
      console.error(error);
      setAssistantResult("Failed to get a response from AI.");
    } finally {
      setAssistantLoading(false);
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
            disabled={processing}
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
            disabled={!file || processing}
          >
            {processing ? "Processing..." : "Upload"}
          </button>
        </section>

        <section className="status-card">
          <h2>Status</h2>
          <p>{status}</p>

          {language && (
            <p>
              <strong>Language:</strong> {language}
            </p>
          )}
        </section>

        <section className="transcription-card">
          <h2>Transcription</h2>

          <div className="transcription-text">{transcription}</div>

          <div className="transcription-actions">
            <button
              type="button"
              onClick={handleCopy}
              disabled={!hasTranscription}
            >
              Copy
            </button>

            <button
              type="button"
              onClick={handleDownload}
              disabled={!hasTranscription}
            >
              Download TXT
            </button>
          </div>
        </section>

        <section className="assistant-card">
          <h2>AI Assistant</h2>

          <p>
            Ask questions about your transcription or generate a summary.
          </p>

          <div className="assistant-actions">
            <button
              type="button"
              onClick={handleSummarize}
              disabled={!hasTranscription || assistantLoading}
            >
              {assistantLoading ? "Processing..." : "Summarize"}
            </button>
          </div>

          <div className="ask-ai">
            <input
              type="text"
              placeholder="Ask something about the transcription..."
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              disabled={!hasTranscription || assistantLoading}
            />

            <button
              type="button"
              onClick={handleAskAI}
              disabled={
                !hasTranscription ||
                !question.trim() ||
                assistantLoading
              }
            >
              Ask AI
            </button>
          </div>

          <div className="assistant-result">
            {assistantResult}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
