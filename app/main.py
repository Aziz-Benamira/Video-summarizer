import streamlit as st
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ui import render_ui
from app.processing import summarize_video

def main():
    st.set_page_config(page_title="YouTube Summarizer", page_icon="🎥", layout="wide")
    
    # Load CSS from static folder
    with open("static/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    render_ui(summarize_video)

if __name__ == "__main__":
    main()