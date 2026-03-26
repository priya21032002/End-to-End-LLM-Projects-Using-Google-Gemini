import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. LOAD ENVIRONMENT VARIABLES
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. PAGE CONFIGURATION
st.set_page_config(
    page_title="Nutritionists GenAI Doctor",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 3. CUSTOM CSS
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        color: #f8fafc;
    }
    
    /* Glassmorphism containers */
    div[data-testid="stVerticalBlock"] > div:has(div.floating-card) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Antigravity Glow Headers */
    .glow-text {
        color: #38bdf8;
        text-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
        font-weight: 800;
        text-align: center;
    }

    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.4);
        border: none;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 4. HEADER SECTION
st.markdown("<h1 class='glow-text' style='font-size: 3.5rem; margin-bottom: 0;'>Calories Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem; letter-spacing: 2px;'>NUTRITIONISTS GENAI DOCTOR</p>", unsafe_allow_html=True)
st.markdown("---")

# 5. LAYOUT: TWO COLUMNS
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='floating-card'>", unsafe_allow_html=True)
    st.subheader("Scan Meal")
    uploaded_file = st.file_uploader("Drop food image here...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Current Plate", use_container_width=True, output_format="PNG")
    else:
        st.info("Please upload a photo of your meal to begin analysis.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='floating-card'>", unsafe_allow_html=True)
    st.subheader("AI Diagnostics")
    
    if uploaded_file:
        analyze_btn = st.button("RUN NUTRITIONAL SCAN", use_container_width=True)
        
        if analyze_btn:
            if not GOOGLE_API_KEY:
                st.error("API Key not found. Please check your .env file.")
            else:
                with st.spinner("Initializing Bio-Scan..."):
                    try:
                        # Initialize Client
                        client = genai.Client(api_key=GOOGLE_API_KEY)
                        
                        # System Prompt
                        analysis_prompt = """
                        Identify all food items in this image. 
                        Provide a detailed response with the following sections:
                        1. **Food Identification**: List items and estimated portions.
                        2. **Calorie Breakdown**: Table with Item | Portion | Calories.
                        3. **Total Energy**: Grand total calories.
                        4. **Macros breakdown**: Carbohydrates, Proteins, and Fats in grams.
                        5. **GenAI Doctor's Advice**: A health-focused recommendation based on this meal.
                        
                        Use professional medical tone but keep it readable. Use Markdown tables.
                        """
                        
                        # Generate Content (Gemini 2.5 Flash)
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[analysis_prompt, image]
                        )
                        
                        # Display results
                        st.markdown("### Analysis Results")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"Scan failed: {str(e)}")
    else:
        st.write("Awaiting data input...")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. FOOTER
st.markdown("<br><hr><center><p style='color: #475569;'>© 2026 Antigravity Labs | Advanced Bio-Intelligence</p></center>", unsafe_allow_html=True)