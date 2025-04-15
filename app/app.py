import os
import tempfile
import streamlit as st
from rag import ChatCSV

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(page_title="Resume Chatbot", page_icon="🤖")

# Paths to avatar icons
hr_icon_path = "/Users/sushilkumarbarai/Documents/My_Github_Project/rag_chat_bot_project/static/hr.png"
bot_icon_path = "/Users/sushilkumarbarai/Documents/My_Github_Project/rag_chat_bot_project/static/robot.png"

# -------------------------------
# Display chat messages
# -------------------------------
def display_messages():
    st.subheader("💬 Chat with HR Bot")

    # Check if image files exist
    if not os.path.exists(hr_icon_path):
        st.error(f"User icon not found: {hr_icon_path}")
    if not os.path.exists(bot_icon_path):
        st.error(f"Bot icon not found: {bot_icon_path}")

    # Render previous messages
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        avatar_path = hr_icon_path if is_user else bot_icon_path

        # Layout for chat messages
        col1, col2 = st.columns([1, 7])
        with col1:
            st.image(avatar_path, width=40)
        with col2:
            alignment = "left" if is_user else "left"  # You can adjust this if needed
            st.markdown(
                f"<div style='text-align: {alignment}; margin-top: 5px;'>{msg}</div>",
                unsafe_allow_html=True
            )

    # Empty spinner for async appearance
    st.session_state["thinking_spinner"] = st.empty()

# -------------------------------
# Process user input
# -------------------------------
def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()

        # Show spinner while the bot generates a response
        with st.session_state["thinking_spinner"], st.spinner("Thinking..."):
            agent_text = st.session_state["assistant"].ask(user_text)

        # Append messages
        st.session_state["messages"].append((user_text, True))   # HR's message
        st.session_state["messages"].append((agent_text, False)) # Bot's response

        # Clear input field
        st.session_state["user_input"] = ""

# -------------------------------
# Handle file upload and ingestion
# -------------------------------
def read_and_save_file():
    st.session_state["assistant"].clear()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}..."):
            st.session_state["assistant"].ingest(file_path)

        os.remove(file_path)

# -------------------------------
# Main Streamlit Page
# -------------------------------
def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatCSV()

    st.title("🧠 Resume Shortlisting HR Bot")
    st.caption("Upload resumes (CSV format) and ask HR-style questions!")

    # File upload section
    st.subheader("📄 Upload CSV Resumes")
    st.file_uploader(
        label="Upload one or more CSV files",
        type=["csv"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.session_state["ingestion_spinner"] = st.empty()

    # Chat section
    display_messages()

    # Input field
    st.text_input(
        label="Ask a question about the candidates...",
        key="user_input",
        on_change=process_input,
        placeholder="e.g., Who has more than 5 years of experience in Python?"
    )

# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    page()
