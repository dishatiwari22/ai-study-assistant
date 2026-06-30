import streamlit as st
import requests

API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="AI Study Assistant", page_icon="🤖", layout="centered")

# ================= UI HEADER =================
st.title("🤖 AI Smart Study Assistant")
st.markdown("### Your personal AI tutor for instant learning 📚")
st.divider()

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Study Settings")

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Study Notes", "MCQs Only", "Quick Revision"]
)

exam_mode = st.sidebar.checkbox("🎯 Exam Mode")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 History")

if "history" not in st.session_state:
    st.session_state.history = []

# ================= INPUT =================
topic = st.text_input("Enter a Topic")

# ================= GENERATE =================
if st.button("🚀 Generate"):

    if topic:

        st.session_state.history.append(topic)

        with st.spinner("Generating your AI study material... 🤖"):

            prompt = f"""
You are an expert teacher and exam coach.

Topic: {topic}
Mode: {mode}

Generate:

1. Simple explanation (easy language)
2. Short exam notes
3. Key points
4. Real-life examples
5. 5 MCQs with answers
6. 3 interview questions
7. Quick revision summary

Make it structured, clear, and student-friendly.
"""

            if exam_mode:
                prompt += "\nFocus only on high probability exam questions and short answers."

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

            data = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }

            response = requests.post(url, json=data)
            result = response.json()

            try:
                output = result["candidates"][0]["content"]["parts"][0]["text"]

                st.success("Generated Successfully 🎉")

                # ================= OUTPUT =================
                st.markdown("## 📘 Your Study Material")
                st.markdown(output)

                # ================= DOWNLOAD BUTTON =================
                st.download_button(
                    label="📥 Download Notes",
                    data=output,
                    file_name=f"{topic}_study_notes.txt",
                    mime="text/plain"
                )

            except:
                st.error("Something went wrong. Please check API key or model.")

    else:
        st.warning("⚠️ Please enter a topic!")

# ================= HISTORY UI =================
if st.session_state.history:
    st.sidebar.write("Recent Topics:")
    for item in reversed(st.session_state.history[-5:]):
        st.sidebar.write("•", item)
