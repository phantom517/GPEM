import streamlit as st
import json
import subprocess
import os
import signal
import pandas

DATA_FILE = "data.json"
BOT_PROCESS = None

# Helper functions
def load_posts():
    try:
        with open(DATA_FILE, "r") as file:
            posts = json.load(file)
            if not isinstance(posts, list):  # Ensure posts is a list
                return []
            return posts
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def start_bot():
    """Start the Discord bot as a subprocess."""
    global BOT_PROCESS
    if BOT_PROCESS is None:
        BOT_PROCESS = subprocess.Popen(["python", "bot.py"])
        st.success("Bot started successfully!")
    else:
        st.warning("Bot is already running!")

def stop_bot():
    """Stop the Discord bot subprocess."""
    global BOT_PROCESS
    if BOT_PROCESS is not None:
        os.kill(BOT_PROCESS.pid, signal.SIGTERM)
        BOT_PROCESS = None
        st.success("Bot stopped successfully!")
    else:
        st.warning("Bot is not running!")

# Streamlit UI
st.set_page_config(page_title="Podcast and Information Sharing")

st.title("Podcast and Information Sharing Platform")
st.subheader("Posts can only be added, edited, or deleted via the Discord bot.")

# Bot Control
st.header("🤖 Discord Bot Control")
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Bot"):
        start_bot()

with col2:
    if st.button("Stop Bot"):
        stop_bot()

# Display Posts
st.header("📜 Posts")
posts = load_posts()

if posts:
    for post in posts:
        st.subheader(post["title"])
        st.write(post["content"])
        if post.get("image_url"):
            st.image(post["image_url"])
        if post.get("video_url"):
            st.video(post["video_url"])
else:
    st.write("No posts yet. Use the Discord bot to add posts!")

st.write("Made with ❤️ using Streamlit and Discord.py.")
