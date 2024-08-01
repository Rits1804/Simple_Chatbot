import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Chatbot",
    page_icon= "🎅" , 
    layout="centered",  # Page layout option
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to translate roles between Chatbot and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Variable to store previous chat history
if "previous_messages" not in st.session_state:
    st.session_state.previous_messages = []

# Display the chatbot's title on the page
st.title("General Chatbot 🎅 ")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to the model and get the response
    model_response = st.session_state.chat_session.send_message(user_prompt)

    # Append user's message to previous messages
    st.session_state.previous_messages.append(("user", user_prompt))

    # Append model's response to previous messages
    st.session_state.previous_messages.append(("assistant", model_response.text))

    # Display model's response
    with st.chat_message("assistant"):
        st.markdown(model_response.text)

# Sidebar for additional options
st.sidebar.header("Options")

# Button to start a new chat session
if st.sidebar.button("Start New Chat"):
    # Clear the chat history displayed on the main screen
    st.session_state.chat_session = model.start_chat(history=[])
    # Force a rerun of the app to update the UI
    st.experimental_rerun()

# Button to display previous chat history
if st.sidebar.button("Previous History"):
    for role, message in st.session_state.previous_messages:
        with st.chat_message(role):
            st.markdown(message)
