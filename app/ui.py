import streamlit as st
from time import sleep

def update_length_selection(selected_key):
    """Callback to ensure only one checkbox is selected."""
    for key in ["short", "medium", "long"]:
        if key != selected_key:
            st.session_state[key] = False

def render_ui(summarize_callback):
    """Renders the Streamlit UI and handles user input."""
    st.markdown('<div class="header"><h1>🎥 YouTube Video Summarizer</h1><p>Extract and summarize video content effortlessly</p></div>', unsafe_allow_html=True)
    
    url = st.text_input("YouTube URL", placeholder="e.g., https://www.youtube.com/watch?v=Q4xCR20Dh1E")
    uploaded_file = st.file_uploader("Or upload a video file", type=["mp4", "avi", "mov", "mkv"], accept_multiple_files=False)
    
    st.write("Select Summary Length:")
    col1, col2, col3 = st.columns(3)
    with col1:
        short = st.checkbox("Short", value=False, key="short", on_change=update_length_selection, args=("short",))
    with col2:
        medium = st.checkbox("Medium", value=True, key="medium", on_change=update_length_selection, args=("medium",))
    with col3:
        long = st.checkbox("Long", value=False, key="long", on_change=update_length_selection, args=("long",))
    
    summary_length = "Short" if short else "Long" if long else "Medium"
    
    if st.button("Summarize Video"):
        if not url and not uploaded_file:
            st.warning("Please enter a YouTube URL or upload a video file.")
            return
        
        with st.status("Processing your video...", expanded=True) as status:
            # Progress callback only for URL downloads
            progress_callback = None
            if url:
                progress_bar = st.progress(0, text="Download Progress: 0%")
                def update_progress(percent, text):
                    progress_bar.progress(percent, text=text)
                    if percent == 100:
                        sleep(0.5)
                        progress_bar.empty()
                progress_callback = update_progress
            
            summary, transcript = summarize_callback(url, uploaded_file, summary_length, status, progress_callback)
        
        if summary and transcript:
            st.success("Done! Here’s your video summary:")
            with st.expander("📜 Full Transcript", expanded=False):
                st.markdown("### Transcript")
                st.text_area("Full text", transcript, height=200, disabled=True)
            st.markdown("### ✨ Summary")
            st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit, Whisper, and Gemini")