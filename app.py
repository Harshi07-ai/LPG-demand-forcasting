import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.getenv("AQ.Ab8RN6LGozogthij2tDj3c99iZDtvCXSJv5Q3stcmF9kBvPpeA"))
model = genai.GenerativeModel("gemini-1.5-flash")
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖 Gemini AI Chatbot")
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Ask anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        answer = response.text
        st.markdown(answer)
 st.session_state.messages.append({"role": "assistant", "content": answer})
