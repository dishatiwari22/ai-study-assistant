import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client (NEW SDK)
client = genai.Client(api_key=api_key)

# Page config
st.set_page_config(
    page_title="AI Smart Study Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Smart Study Assistant")
st.write("Enter any study topic and let AI generate study material.")

# Input
topic = st.text_input("Enter a Topic")

# Button
if st.button("Generate"):
    if topic:

        with st.spinner("Generating..."):

            prompt = f"""
            Give detailed study material on {topic}.

            Include:
            1. Explanation
            2. Short Notes
            3. Key Points
            4. Five MCQs with answers
            5. Three Interview Questions
            6. Summary
            """

            # Gemini API call (CORRECT MODEL)
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )

            st.markdown(response.text)

    else:
        st.warning("Please enter a topic.")