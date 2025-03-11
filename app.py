import streamlit as st
from Support_Bot import SupportBotAgent
import logging

st.title("Customer Support Bot")

# Initialize bot
if 'bot' not in st.session_state:
    try:
        st.session_state.bot = SupportBotAgent("sample.pdf")
        logging.info("Support bot initialized.")
    except Exception as e:
        st.error(f"Error initializing bot: {e}")
        st.stop()

# Initialize chat history and feedback tracking
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}

# Display chat history with feedback
chat_container = st.container()

with chat_container:
    for idx, (role, message) in enumerate(st.session_state.chat_history):
        with st.chat_message(role):
            st.markdown(message)

        if role == "Bot":
            col1, col2 = st.columns(2)  # Place buttons side by side

            # Ensure only one feedback is given per bot response
            if idx not in st.session_state.feedback:
                with col1:
                    if st.button("👍", key=f"up_{idx}"):
                        st.session_state.feedback[idx] = "positive"
                        logging.info(f"User feedback: Positive (Message {idx})")
                        st.rerun()  # Refresh the app to update the UI
                with col2:
                    if st.button("👎", key=f"down_{idx}"):
                        st.session_state.feedback[idx] = "negative"
                        logging.info(f"User feedback: Negative (Message {idx})")
                        st.rerun()  # Refresh the app to update the UI

# Input box at the bottom center
with st.form(key='input_form', clear_on_submit=True):
    query = st.text_input("You:", key="input", value="", placeholder="Type your message here...")
    submit_button = st.form_submit_button(label='Send')

if submit_button and query:
    try:
        response = st.session_state.bot.query_handler.answer_query(query)
        st.session_state.chat_history.append(("You", query))
        st.session_state.chat_history.append(("Bot", response))
        st.rerun()  # Refresh the app to update the chat history
    except Exception as e:
        st.error(f"Error processing query: {e}")
        logging.error(f"Error processing query: {e}")
