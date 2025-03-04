# Video Summarizer

A Streamlit-based application that summarizes YouTube videos or local video files by downloading or uploading them, extracting audio, transcribing it using Whisper, and generating a structured summary with Gemini. Users can choose between "Short," "Medium," or "Long" summary lengths via checkboxes.

## Features
- **Dual Input**: Summarize videos from YouTube URLs or upload local files (`.mp4`, `.avi`, `.mov`, `.mkv`).
- **Progress Tracking**: Displays a progress bar for YouTube downloads; skips it for uploaded files.
- **Summary Length**: Select "Short" (50–150 tokens), "Medium" (100–300 tokens), or "Long" (200–500 tokens) via exclusive checkboxes.
- **Structured Output**: Summaries include bolded "Main Topic" and "Key Details" with bullet points.
- **Docker Support**: Run the app in a containerized environment.

## Project Structure
```
video-summarizer/
├── app/
│   ├── __init__.py         # Marks app/ as a package
│   ├── main.py             # Entry point for Streamlit
│   ├── ui.py               # UI rendering and user input handling
│   ├── processing.py       # Video processing (download, extract, transcribe, summarize)
│   └── utils.py            # Helper functions (e.g., cleanup)
├── static/
│   └── styles.css          # CSS styles for the app
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

- **`app/`**: Modular Python code split into logical components.
- **`static/`**: External CSS for consistent styling.
- **`Dockerfile`**: Sets up the app with Python and FFmpeg.
- **`requirements.txt`**: Lists required Python packages.

## Prerequisites
- Python 3.11+
- FFmpeg installed (for audio extraction)
- A Gemini API key from Google AI Studio

## Setup Instructions

### Local Installation
1. **Clone or Download**:
   - Download the project to `C:\Users\benam\Downloads\Video-summarizer` or clone it:
     ```bash
     git clone <repository-url>
     cd youtube-summarizer
     ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - Note: If using `openai-whisper`, replace `whisper` with `openai-whisper` in `requirements.txt`.

3. **Set API Key**:
   - Open `app/processing.py` and replace `"YOUR_API_KEY_HERE"` with your Gemini API key.

4. **Run the App**:
   ```bash
   streamlit run app/main.py --server.fileWatcherType none
   ```
   - Open `http://localhost:8501` in your browser.

### Docker Installation
1. **Build the Docker Image**:
   - From `youtube-summarizer/`:
     ```bash
     docker build -t youtube-summarizer .
     ```

2. **Run the Container**:
   ```bash
   docker run -p 8501:8501 youtube-summarizer
   ```
   - Open `http://localhost:8501`.

## Usage
1. **Input Video**:
   - **YouTube URL**: Enter a URL (e.g., `https://www.youtube.com/watch?v=Q4xCR20Dh1E`) to download and process.
   - **Local File**: Upload a video file (`.mp4`, `.avi`, `.mov`, `.mkv`) from your Windows Explorer to process directly.
   - Note: Provide either a URL or a file, not both.

2. **Select Summary Length**:
   - Tick one checkbox: "Short," "Medium," or "Long." Only one can be selected at a time (default: "Medium").

3. **Summarize**:
   - Click "Summarize Video" to start processing.
   - **URL**: See a progress bar during download, then status updates ("Extracting audio...", etc.).
   - **Upload**: See status updates starting with "Processing uploaded video..." (no progress bar).

4. **View Results**:
   - After processing, a "Done!" message appears with:
     - A collapsible "Full Transcript" expander.
     - A styled "Summary" box with bolded "Main Topic" and "Key Details."

## Example Output
- **Medium Length (URL or Upload)**:
  ```
  Main Topic:
  • This text explains how to make a perfect smash burger, emphasizing ingredients and techniques.

  Key Details:
  • **Beef:** High-quality 80/20 ground beef for optimal flavor and texture.
  • **Shaping:** Shape into balls, smash for crispy edges.
  • **Sauce:** Includes pickles, mayo, honey, mustard, and spices.
  • **Cooking:** Use cast iron, toast buns for steam.
  • **Assembly:** Layer patties, cheese, pickles, and sauce.
  ```

## Dockerfile Details
- Base: `python:3.11-slim`
- Installs: FFmpeg for audio extraction, Python dependencies from `requirements.txt`.
- Runs: `streamlit run app/main.py` on port 8501 with `--server.fileWatcherType none`.

## Troubleshooting
- **ModuleNotFoundError: No module named 'app'**:
  - Run from the `youtube-summarizer/` root directory:
    ```bash
    cd C:\path\to\youtube-summarizer
    streamlit run app/main.py
    ```
- **Progress Bar Issues**:
  - If it appears for uploaded files, ensure `ui.py` correctly skips it for `uploaded_file` inputs.
- **FFmpeg Errors**:
  - Local: Install FFmpeg (`choco install ffmpeg` on Windows with Chocolatey) and add to PATH.
  - Docker: Verify FFmpeg installation in the container (`docker exec -it <container> ffmpeg -version`).
- **API Key Issues**:
  - Replace `"YOUR_API_KEY_HERE"` in `app/processing.py` with a valid Gemini API key.

## Development Notes
- Built with Python 3.11, Streamlit 1.31.0, yt-dlp, ffmpeg-python, Whisper, and google-generativeai.
- Modular design separates UI (`ui.py`), processing (`processing.py`), and utilities (`utils.py`).
- Last updated: March 4, 2025.

## Contributing
Feel free to fork, submit issues, or PRs to enhance functionality (e.g., more video formats, additional summary options).

---
Built with ❤️ by Aziz Ben Amira using Streamlit, Whisper, and Gemini.


