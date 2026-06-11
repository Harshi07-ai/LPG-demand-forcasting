import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key='AQ.Ab8RN6KENiYIBD6FTZg1ItYI-SM4ojQkfRnd5Q49DrWhGcJZLw')

# Use Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Gemini AI Chatbot")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask anything..."):

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        response = model.generate_content(prompt)

        answer = response.text

        response_placeholder.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    