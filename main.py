import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

PRIMARY_MODEL = "models/gemini-1.5-flash"

st.set_page_config(
    page_title="Chat with Gemini",
    page_icon="🧠",
    layout="centered",
)

st.title("🤖 Gemini ChatBot by Harshad")

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

model = genai.GenerativeModel(PRIMARY_MODEL)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

for msg in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(msg.role)):
        st.markdown(msg.parts[0].text)

user_prompt = st.chat_input("Ask Gemini...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    try:
        response = st.session_state.chat_session.send_message(user_prompt)
    except ResourceExhausted as e:
        st.error("Quota exceeded. Please wait a moment or try again later.")
        response = None
    except Exception as e:
        st.error(f"Something went wrong: {e}")
        response = None

    if response:
        with st.chat_message("assistant"):
            st.markdown(response.text)
