import yt_dlp
import ffmpeg
import whisper
import google.generativeai as genai
import os
import uuid
from app.utils import cleanup_files
from dotenv import load_dotenv
import streamlit as st
# Load environment variables from .env file
load_dotenv()

# Configure Gemini API with the loaded API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def download_video(url, output_path="video.mp4", progress_callback=None):
    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes > 0 and progress_callback:
                percent = int((downloaded_bytes / total_bytes) * 100)
                progress_callback(percent, f"Download Progress: {percent}%")
        elif d['status'] == 'finished' and progress_callback:
            progress_callback(100, "Download Progress: 100%")

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'progress_hooks': [progress_hook],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path if os.path.exists(output_path) else None

def extract_audio(video_path, audio_path="audio.wav"):
    print("Extracting audio...")
    try:
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(stream, audio_path, acodec='pcm_s16le', ar='16000', ac=1)
        ffmpeg.run(stream, overwrite_output=True)
        print("Audio extraction complete!")
        return audio_path if os.path.exists(audio_path) else None
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e}")
        return None

def transcribe_audio(audio_path):
    print("Transcribing audio...")
    if not audio_path or not os.path.exists(audio_path):
        print("Audio file not found for transcription.")
        return None
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print("Transcription complete!")
    return result["text"]

def summarize_text(text, length="Medium"):
    print("Summarizing text...")
    if not text:
        print("No transcript available to summarize.")
        return None
    
    length_options = {
        "Short": (150, 50),
        "Medium": (300, 100),
        "Long": (500, 200)
    }
    max_length, min_length = length_options.get(length, (300, 100))
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = (
        f"Summarize the following text into a structured format with two sections: 'Main Topic' and 'Key Details'. "
        f"The 'Main Topic' should capture the primary focus or theme (like the first sentence or declarative statements with 'is', 'are', 'discusses', or 'explains'). "
        f"The 'Key Details' should include supporting points or examples (like sentences with 'shows', 'includes', 'features', or 'example'), with each key item bolded (e.g., '**Beef:**', '**Sauce:**'). "
        f"Keep the summary between {min_length} and {max_length} tokens. Format it with '**Main Topic:**' and '**Key Details:**' as bold headers followed by bullet points (•). "
        f"Here’s the text to summarize:\n\n{text}"
    )
    
    try:
        response = model.generate_content(prompt)
        raw_summary = response.text.strip()
        structured_summary = raw_summary.replace("**Main Topic:**", "<b>Main Topic:</b>").replace("\n", "<br>")
        print("Summarization complete!")
        structured_summary=structured_summary.replace("**Key Details:**", "<b>Key Details:</b>")
        structured_summary=structured_summary.replace("•", "<br>•")
        structured_summary=structured_summary.replace("**", "")
        return structured_summary
    except Exception as e:
        st.error(f"Gemini API error: {str(e)}")
        return None

def summarize_video(url, uploaded_file, length, status, progress_callback=None):
    """Orchestrates the video/audio summarization process."""
    video_file = None
    audio_file = None
    
    if url:
        status.update(label="Downloading video...")
        video_file = download_video(url, progress_callback=progress_callback)
        if not video_file:
            status.update(label="Video download failed!", state="error")
            return None, None
        
        status.update(label="Extracting audio...")
        audio_file = extract_audio(video_file)
        if not audio_file:
            status.update(label="Audio extraction failed!", state="error")
            cleanup_files(video_file)
            return None, None
    
    elif uploaded_file:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        if file_ext == "mp3":
            status.update(label="Processing uploaded audio...")
            audio_file = "uploaded_audio.mp3"
            with open(audio_file, "wb") as f:
                f.write(uploaded_file.read())
            if not os.path.exists(audio_file):
                status.update(label="Audio upload failed!", state="error")
                return None, None
        else:  # Video file (mp4, avi, mov, mkv)
            status.update(label="Processing uploaded video...")
            video_file = f"uploaded_video.{file_ext}"
            with open(video_file, "wb") as f:
                f.write(uploaded_file.read())
            if not os.path.exists(video_file):
                status.update(label="Video upload failed!", state="error")
                return None, None
            
            status.update(label="Extracting audio...")
            audio_file = extract_audio(video_file)
            if not audio_file:
                status.update(label="Audio extraction failed!", state="error")
                cleanup_files(video_file)
                return None, None
    
    status.update(label="Transcribing audio...")
    transcript = transcribe_audio(audio_file)
    if not transcript:
        status.update(label="Transcription failed!", state="error")
        cleanup_files(video_file, audio_file)
        return None, None
    
    status.update(label="Summarizing text...")
    summary = summarize_text(transcript, length)
    if not summary:
        status.update(label="Summarization failed!", state="error")
        cleanup_files(video_file, audio_file)
        return None, None
    
    cleanup_files(video_file, audio_file)
    status.update(label="Processing complete!", state="complete")
    return summary, transcript