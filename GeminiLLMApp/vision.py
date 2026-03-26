from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from google import genai
from google.genai import types
from PIL import Image
import io

# Configure client with new SDK
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, image=None):
    try:
        if image is not None:
            # Send both image and text
            contents = [
                types.Part.from_bytes(
                    data=image,
                    mime_type="image/jpeg"
                ),
                question
            ]
        else:
            contents = question

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=contents
        )
        return response.text

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "Quota exceeded. Please wait a minute and try again."
        elif "404" in error_msg:
            return "Model not found. Run list_models.py to see available models."
        elif "403" in error_msg:
            return "nvalid API key. Please check your .env file."
        else:
            return f"Unexpected error: {error_msg}"

st.set_page_config(page_title="Gemini Image Q&A")
st.header("Gemini Image Understanding App")

# Text input
user_input = st.text_input(
    "Ask anything about the image:",
    key="input",
    placeholder="e.g. What is in this image?"
)

# Image upload
uploaded_file = st.file_uploader(
    "Upload an image (optional):",
    type=["jpg", "jpeg", "png", "webp"]
)

# Show uploaded image preview
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit = st.button("Ask Gemini")

if submit:
    if not user_input.strip():
        st.warning("Please enter a question before submitting.")
    else:
        # Convert image to bytes if uploaded
        image_bytes = None
        if uploaded_file is not None:
            image_bytes = uploaded_file.getvalue()

        with st.spinner("Analyzing..."):
            response = get_gemini_response(user_input, image_bytes)

        st.subheader("Response:")
        st.write(response)