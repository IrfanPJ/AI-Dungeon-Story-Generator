import os
import streamlit as st
from story_generator import generate_story
from genres import GENRES
from utils import save_story_to_file

# Directory where saved stories are stored
SAVED_STORIES_DIR = "saved_stories"

# Ensure saved stories directory exists
if not os.path.exists(SAVED_STORIES_DIR):
    os.makedirs(SAVED_STORIES_DIR)

# Custom CSS styling for cyberpunk glass look
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');

    /* Background gradient */
    .stApp {
        background: radial-gradient(circle at center, #0f0c29, #302b63, #24243e);
        color: #c0c0ff;
        font-family: 'Russo One', sans-serif;
        min-height: 100vh;
        padding: 2rem;
    }

    /* Glass container with blur */
    .main-container {
        background: rgba(18, 18, 25, 0.7);
        border-radius: 16px;
        padding: 2rem;
        max-width: 900px;
        margin: 0 auto;
        box-shadow:
            0 4px 30px rgba(0, 0, 0, 0.5),
            0 0 15px #00fff7;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 255, 247, 0.3);
    }

    /* Title styling */
    h1 {
        font-size: 3rem;
        text-align: center;
        color: #00fff7;
        text-shadow: 0 0 10px #00fff7;
        margin-bottom: 1.5rem;
    }

    /* Subheader styling */
    h2 {
        color: #00e6d9;
        text-shadow: 0 0 6px #00e6d9;
        margin-top: 2rem;
    }

    /* Text area styling */
    textarea {
        background-color: #1a1a2e !important;
        color: #c0c0ff !important;
        border-radius: 10px !important;
        border: 1px solid #00fff7 !important;
        font-size: 1rem !important;
        padding: 10px !important;
        resize: vertical !important;
        box-shadow: 0 0 6px #00fff7;
    }

    /* Selectbox styling */
    div[role="listbox"] {
        background-color: #1a1a2e !important;
        color: #c0c0ff !important;
        border-radius: 10px !important;
        border: 1px solid #00fff7 !important;
        box-shadow: 0 0 6px #00fff7;
    }

    /* Slider styling */
    input[type=range] {
        accent-color: #00fff7;
    }

    /* Button styling */
    div.stButton > button {
        background: linear-gradient(45deg, #00fff7, #006677);
        border: none;
        color: #0f0c29;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.5rem 2rem;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 0 10px #00fff7;
        transition: background 0.3s ease, color 0.3s ease;
        margin-top: 1rem;
    }

    div.stButton > button:hover {
        background: linear-gradient(45deg, #006677, #00fff7);
        color: #fff;
        box-shadow: 0 0 20px #00fff7;
    }

    /* Story text container */
    .story-text {
        background: rgba(0, 255, 247, 0.1);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 0 10px #00fff7;
        color: #d0f0ff;
        font-size: 1.1rem;
        line-height: 1.5;
        margin-bottom: 1rem;
        white-space: pre-wrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main container start
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🧙 AI Dungeon Story Generator")

# Select genre, prompt, and number of samples
genre = st.selectbox("Select Genre", list(GENRES.keys()))
prompt = st.text_area("Enter your story prompt:", height=120)
num_samples = st.slider("Number of story continuations:", 1, 3, 1)

if "stories" not in st.session_state:
    st.session_state.stories = []

# Generate story button logic
if st.button("Generate Story"):
    if not prompt.strip():
        st.warning("Please enter a prompt!")
    else:
        with st.spinner("Summoning the story..."):
            stories = generate_story(prompt, genre, num_samples)
            st.session_state.stories = stories

# Display generated stories
if st.session_state.stories:
    for i, story in enumerate(st.session_state.stories):
        st.subheader(f"Story {i + 1}")
        st.markdown(f'<div class="story-text">{story}</div>', unsafe_allow_html=True)

        if st.button(f"Save Story {i + 1}", key=f"save_{i}"):
            filename = save_story_to_file(story, genre=genre)
            st.success(f"Story {i + 1} saved to {filename}")
            st.markdown(f"[📥 Download your story]({filename})", unsafe_allow_html=True)

# Checkbox to show saved stories
show_saved = st.checkbox("Show Saved Stories")

if show_saved:
    st.subheader("📂 Saved Stories")
    saved_files = sorted(os.listdir(SAVED_STORIES_DIR))
    if saved_files:
        for fname in saved_files:
            filepath = os.path.join(SAVED_STORIES_DIR, fname)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                st.markdown(f"### {fname}")
                st.markdown(f'<div class="story-text">{content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error reading {fname}: {e}")
    else:
        st.info("No saved stories found.")

# Main container end
st.markdown('</div>', unsafe_allow_html=True)
