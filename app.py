import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from environment (.env locally / Secrets in cloud)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Use stable model
model = genai.GenerativeModel("gemini-2.5-flash")

# Page setup
st.set_page_config(
    page_title="AI Smart Study Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Smart Study Assistant")
st.write("Enter any topic and get structured study material instantly.")

# Input
topic = st.text_input("Enter a Topic")

# Button
if st.button("Generate"):
    if topic:

        with st.spinner("Generating study material..."):

            prompt = f"""
            Act as a professional teacher.

            Create structured study notes on: {topic}

            Include:
            1. Explanation
            2. Short Notes
            3. Key Points
            4. 5 MCQs with answers
            5. 3 Interview Questions
            6. Summary

            Make it clear, simple and exam-ready.
            """

            response = model.generate_content(prompt)

            st.markdown(response.text)

    else:
        st.warning("Please enter a topic.")