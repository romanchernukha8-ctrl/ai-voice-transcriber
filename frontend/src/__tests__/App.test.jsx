import {
  describe,
  it,
  expect,
  beforeEach,
  afterEach,
  vi,
} from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import App from "../App";

describe("AI Voice Transcriber", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  function mockPollingTimer() {
    const realSetTimeout = globalThis.setTimeout;

    vi.spyOn(globalThis, "setTimeout").mockImplementation(
      (callback, delay, ...args) => {
        if (delay === 2000) {
          return realSetTimeout(callback, 0, ...args);
        }

        return realSetTimeout(callback, delay, ...args);
      },
    );
  }

  function selectAudioFile() {
    const file = new File(["audio content"], "recording.wav", {
      type: "audio/wav",
    });

    fireEvent.change(screen.getByLabelText("Choose audio file"), {
      target: { files: [file] },
    });

    return file;
  }

  function mockSuccessfulUpload(text = "Hello world") {
    mockPollingTimer();

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: "file-123" }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          language: "en",
          text,
        }),
      });

    vi.stubGlobal("fetch", fetchMock);

    return fetchMock;
  }

  async function uploadAndWaitForTranscription(text = "Hello world") {
    const fetchMock = mockSuccessfulUpload(text);

    render(<App />);

    const file = selectAudioFile();

    fireEvent.click(screen.getByRole("button", { name: "Upload" }));

    expect(await screen.findByText(text)).toBeInTheDocument();

    return { file, fetchMock };
  }

  it("renders the application interface", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: "AI Voice Transcriber" }),
    ).toBeInTheDocument();

    expect(
      screen.getByText("Upload an audio file and get its transcription."),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { name: "Transcription" }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { name: "AI Assistant" }),
    ).toBeInTheDocument();
  });

  it("disables Upload when no file is selected", () => {
    render(<App />);

    expect(
      screen.getByRole("button", { name: "Upload" }),
    ).toBeDisabled();
  });

  it("enables Upload after selecting an audio file", () => {
    render(<App />);

    selectAudioFile();

    expect(screen.getByText("recording.wav")).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: "Upload" }),
    ).toBeEnabled();

    expect(screen.getByText("Ready to upload")).toBeInTheDocument();
  });

  it("disables transcription actions when no transcription exists", () => {
    render(<App />);

    expect(screen.getByRole("button", { name: "Copy" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Download TXT" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Summarize" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Ask AI" })).toBeDisabled();
  });

  it("does not send an AI request when no transcription exists", () => {
    const fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Summarize" }));

    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("uploads an audio file and displays the transcription", async () => {
    const { file, fetchMock } =
      await uploadAndWaitForTranscription("Hello world");

    expect(screen.getByText("Completed")).toBeInTheDocument();
    expect(screen.getByText("Language:")).toBeInTheDocument();
    expect(screen.getByText("en")).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledTimes(2);

    expect(fetchMock).toHaveBeenNthCalledWith(
      1,
      "/api/v1/files/upload",
      expect.objectContaining({
        method: "POST",
        body: expect.any(FormData),
      }),
    );

    const uploadedForm = fetchMock.mock.calls[0][1].body;

    expect(uploadedForm.get("file")).toBe(file);

    expect(fetchMock).toHaveBeenNthCalledWith(
      2,
      "/api/v1/files/file-123/transcription",
    );
  });

  it("displays an error when the audio upload fails", async () => {
    const fetchMock = vi.fn().mockResolvedValueOnce({
      ok: false,
    });

    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(console, "error").mockImplementation(() => {});

    render(<App />);

    selectAudioFile();

    fireEvent.click(screen.getByRole("button", { name: "Upload" }));

    expect(await screen.findByText("Failed")).toBeInTheDocument();

    expect(screen.getByText("Something went wrong.")).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it("displays an error when retrieving the transcription fails", async () => {
    mockPollingTimer();

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: "file-123" }),
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(console, "error").mockImplementation(() => {});

    render(<App />);

    selectAudioFile();

    fireEvent.click(screen.getByRole("button", { name: "Upload" }));

    expect(await screen.findByText("Failed")).toBeInTheDocument();

    expect(screen.getByText("Something went wrong.")).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("retries transcription polling when the transcription is not ready", async () => {
    mockPollingTimer();

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: "file-123" }),
      })
      .mockResolvedValueOnce({
        ok: false,
        status: 404,
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          language: "en",
          text: "Transcription after retry",
        }),
      });

    vi.stubGlobal("fetch", fetchMock);

    render(<App />);

    selectAudioFile();

    fireEvent.click(screen.getByRole("button", { name: "Upload" }));

    expect(
      await screen.findByText("Transcription after retry"),
    ).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledTimes(3);
    expect(screen.getByText("Completed")).toBeInTheDocument();
  });

  it("copies the transcription to the clipboard", async () => {
    const { fetchMock } = await uploadAndWaitForTranscription(
      "Text to copy",
    );

    const writeText = vi.fn().mockResolvedValue(undefined);

    vi.stubGlobal("navigator", {
      ...globalThis.navigator,
      clipboard: { writeText },
    });

    fireEvent.click(screen.getByRole("button", { name: "Copy" }));

    await waitFor(() => {
      expect(writeText).toHaveBeenCalledWith("Text to copy");
    });

    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("downloads the transcription as a TXT file", async () => {
    await uploadAndWaitForTranscription("Text to download");

    const createObjectURL = vi.fn(() => "blob:test-url");
    const revokeObjectURL = vi.fn();

    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL,
      revokeObjectURL,
    });

    const clickSpy = vi
      .spyOn(HTMLAnchorElement.prototype, "click")
      .mockImplementation(() => {});

    fireEvent.click(
      screen.getByRole("button", { name: "Download TXT" }),
    );

    expect(createObjectURL).toHaveBeenCalledTimes(1);

    const blob = createObjectURL.mock.calls[0][0];

    expect(blob).toBeInstanceOf(Blob);
    expect(await blob.text()).toBe("Text to download");

    expect(clickSpy).toHaveBeenCalledTimes(1);
    expect(revokeObjectURL).toHaveBeenCalledWith("blob:test-url");
  });

  it("summarizes an existing transcription using AI", async () => {
    const { fetchMock } = await uploadAndWaitForTranscription(
      "The meeting starts at ten.",
    );

    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: "The meeting starts at 10 AM.",
      }),
    });

    fireEvent.click(screen.getByRole("button", { name: "Summarize" }));

    expect(
      await screen.findByText("The meeting starts at 10 AM."),
    ).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledTimes(3);

    expect(fetchMock).toHaveBeenLastCalledWith(
      "/ai/generate",
      expect.objectContaining({
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: expect.any(String),
      }),
    );

    const requestBody = JSON.parse(fetchMock.mock.calls[2][1].body);

    expect(requestBody.prompt).toContain("The meeting starts at ten.");
  });

  it("answers a question about an existing transcription", async () => {
    const { fetchMock } = await uploadAndWaitForTranscription(
      "The server runs on port 8003.",
    );

    fetchMock.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: "The server uses port 8003.",
      }),
    });

    const questionInput = screen.getByPlaceholderText(
      "Ask something about the transcription...",
    );

    fireEvent.change(questionInput, {
      target: {
        value: "Which port does the server use?",
      },
    });

    fireEvent.click(screen.getByRole("button", { name: "Ask AI" }));

    expect(
      await screen.findByText("The server uses port 8003."),
    ).toBeInTheDocument();

    expect(fetchMock).toHaveBeenCalledTimes(3);

    const requestBody = JSON.parse(fetchMock.mock.calls[2][1].body);

    expect(requestBody.prompt).toContain("The server runs on port 8003.");

    expect(requestBody.prompt).toContain(
      "Which port does the server use?",
    );
  });

  it("does not send an AI request when the question is empty", async () => {
    const { fetchMock } = await uploadAndWaitForTranscription(
      "Some transcription text.",
    );

    fireEvent.click(screen.getByRole("button", { name: "Ask AI" }));

    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("displays an error when the AI request fails", async () => {
    const { fetchMock } = await uploadAndWaitForTranscription(
      "Some transcription text.",
    );

    fetchMock.mockResolvedValueOnce({
      ok: false,
    });

    vi.spyOn(console, "error").mockImplementation(() => {});

    fireEvent.click(screen.getByRole("button", { name: "Summarize" }));

    expect(
      await screen.findByText("Failed to get a response from AI."),
    ).toBeInTheDocument();
  });
});