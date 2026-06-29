import streamlit as st
import requests
import os

# Get API key from Streamlit Secrets (NOT dotenv)
API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="AI Study Assistant", page_icon="🤖")

st.title("🤖 AI Smart Study Assistant")

topic = st.text_input("Enter Topic")

if st.button("Generate"):

    if topic:

        with st.spinner("Generating..."):

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

            data = {
                "contents": [{
                    "parts": [{
                        "text": f"""
                        Act as a teacher and create study notes on {topic}.

                        Include:
                        1. Explanation
                        2. Short Notes
                        3. Key Points
                        4. 5 MCQs with answers
                        5. 3 Interview Questions
                        6. Summary
                        """
                    }]
                }]
            }

            response = requests.post(url, json=data)
            result = response.json()

            try:
                output = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(output)
            except:
                st.error("Failed to generate response. Check API key.")

    else:
        st.warning("Please enter a topic.")
