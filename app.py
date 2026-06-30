import streamlit as st
import requests
import os

# Get API key from Streamlit Secrets
API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="AI Study Assistant", page_icon="🤖")

# ⭐ UI HEADER
st.title("🤖 AI Smart Study Assistant")
st.markdown("### Learn any topic in seconds with AI-generated notes")
st.divider()

# ⭐ STEP 2: SIDEBAR CONTROLS
st.sidebar.title("Study Settings")

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Study Notes", "MCQs Only", "Quick Revision"]
)

exam_mode = st.sidebar.checkbox("Exam Mode")

# INPUT
topic = st.text_input("Enter Topic")

# BUTTON
if st.button("Generate"):

    if topic:

        with st.spinner("Generating your study material... 🤖"):

            # ⭐ STEP 3: BUILD PROMPT WITH MODES
            prompt = f"""
            Act as an expert teacher and exam coach.

            Topic: {topic}
            Mode: {mode}

            Generate:

            1. Simple explanation (easy language)
            2. Short exam notes
            3. Key points
            4. Real-life examples
            5. 5 MCQs with answers
            6. 3 Interview Questions
            7. Quick revision summary

            Make it structured and student-friendly.
            """

            if exam_mode:
                prompt += "\nFocus only on important exam questions and short answers."

            # API CALL
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }

            response = requests.post(url, json=data)
            result = response.json()

            try:
                output = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(output)

            except:
                st.error("Failed to generate response. Check API key or model.")

    else:
        st.warning("Please enter a topic.")
