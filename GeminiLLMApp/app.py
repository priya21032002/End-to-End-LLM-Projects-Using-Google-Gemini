from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from google import genai

# Configure client with new SDK
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=question        
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "Quota exceeded. Please wait a minute and try again."
        elif "404" in error_msg:
            return "Model not found. Run list_models.py to see available models."
        elif "403" in error_msg:
            return "Invalid API key. Please check your .env file."
        else:
            return f"Unexpected error: {error_msg}"

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

user_input = st.text_input("Ask anything:", key="input", placeholder="e.g. Write a poem about cherry blossoms")
submit = st.button("Ask Gemini")

if submit:
    if not user_input.strip():
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Thinking..."):
            response = get_gemini_response(user_input)
        st.subheader("Response:")
        st.write(response)