import streamlit as st
import requests

API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(page_title="AI Study Chat Assistant", page_icon="🤖", layout="centered")

# ================= HEADER =================
st.title("🤖 AI Smart Study Chat Assistant")
st.markdown("Chat with your AI tutor like ChatGPT 📚")
st.divider()

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Study Notes", "MCQs Only", "Quick Revision"]
)

exam_mode = st.sidebar.checkbox("🎯 Exam Mode")

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= USER INPUT =================
user_input = st.chat_input("Ask anything (e.g. Explain photosynthesis)")

if user_input:

    # store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # ================= BUILD PROMPT =================
    prompt = f"""
You are an expert AI teacher.

Mode: {mode}

Student question: {user_input}

Generate:
- Simple explanation
- Key points
- Examples
- If needed MCQs or summary

Make it easy to understand.
"""

    if exam_mode:
        prompt += "\nFocus on exam-relevant short answers and important questions."

    # ================= API CALL =================
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            response = requests.post(url, json=data)
            result = response.json()

            try:
                output = result["candidates"][0]["content"]["parts"][0]["text"]

                st.markdown(output)

                # save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": output
                })

            except:
                error_msg = "Sorry, I couldn't generate a response. Check API key or model."
                st.error(error_msg)
