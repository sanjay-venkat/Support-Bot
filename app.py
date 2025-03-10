import streamlit as st
from Support_Bot import SupportBotAgent
import logging

# Initialize bot (do this outside the chat loop)
if 'bot' not in st.session_state:
    try:
        document_path = "sample.pdf"  # Or make this configurable
        st.session_state.bot = SupportBotAgent(document_path)
        logging.info("Support bot initialized.")
    except Exception as e:
        st.error(f"Error initializing bot: {e}")
        st.stop()  # Stop execution if bot initialization fails

# Streamlit UI
st.title("Customer Support Bot")

# CSS to center elements
st.markdown(
    """
    <style>
    .centered {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh; /* Optional: Full height */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Chat history (using session state)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history =[]

# Input box
query = st.text_input("You:", key="input")

# Process query and display response
if query:
    try:
        response = st.session_state.bot.query_handler.answer_query(query)
        logging.info(f"Received query: {query}")
        logging.info(f"Bot's response: {response}")
        st.session_state.chat_history.append(("You", query))
        st.session_state.chat_history.append(("Bot", response))
    except Exception as e:
        st.error(f"Error processing query: {e}")
        logging.error(f"Error processing query: {e}")

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)
