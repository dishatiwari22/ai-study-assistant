import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="AI Study Assistant", page_icon="🤖")

st.title("🤖 AI Smart Study Assistant")
st.write("Enter a topic and get AI-generated study notes")

topic = st.text_input("Enter Topic")

if st.button("Generate"):

    if topic:

        with st.spinner("Generating..."):

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

            headers = {
                "Content-Type": "application/json"
            }

            data = {
                "contents": [{
                    "parts": [{
                        "text": f"""
                        Act as a teacher. Create detailed study material on {topic}.

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

            response = requests.post(url, headers=headers, json=data)

            result = response.json()

            try:
                output = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(output)
            except:
                st.error("Error generating response. Check API key or model access.")

    else:
        st.warning("Please enter a topic.")
