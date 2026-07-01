import streamlit as st
import requests

API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(
    page_title="AI Smart Study Assistant",
    page_icon="🤖",
    layout="wide"
)
st.markdown("""
<style>

.stApp{
    background: linear-gradient(to right,#f8fbff,#eef4ff);
}

.main-title{
    font-size:42px;
    font-weight:bold;
    text-align:center;
    color:white;
    padding:18px;
    border-radius:15px;
    background: linear-gradient(90deg,#6C63FF,#8E2DE2,#FF4B91);
}

.subtitle{
    text-align:center;
    color:#555;
    font-size:18px;
    margin-top:10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
'<div class="main-title">🤖 AI Smart Study Assistant</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="subtitle">Your Personal AI Tutor powered by Gemini AI</div>',
unsafe_allow_html=True
)

st.divider()

st.sidebar.markdown("""
# 📚 AI Study Assistant

Welcome!

Customize your learning experience.
""")

mode = st.sidebar.selectbox(
    "Learning Mode",
    [
        "Study Notes",
        "Quick Revision",
        "MCQs Only",
        "Quiz Mode"
    ]
)

difficulty = st.sidebar.selectbox(
    "Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

exam_mode = st.sidebar.checkbox("Exam Mode")

st.sidebar.divider()

st.sidebar.subheader("Suggested Topics")

topics = [
    "Artificial Intelligence",
    "Machine Learning",
    "Python",
    "Java",
    "DBMS",
    "Operating System",
    "Computer Networks",
    "Data Structures"
]

for topic in topics:
    st.sidebar.write("•", topic)

st.sidebar.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:

    st.info("""
### 👋 Welcome!

Try asking:

• 🤖 Explain Artificial Intelligence

• 🐍 Teach me Python Basics

• 📚 Revise DBMS

• 🧠 Create a Quiz on Machine Learning

Happy Learning! 🚀
""")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "💬 Ask anything... Example: Explain Machine Learning in simple words"
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    if mode == "Quiz Mode":

        prompt = f"""
You are an expert teacher.

Create a quiz on:

{question}

Difficulty Level:
{difficulty}

Generate:

1. 10 Multiple Choice Questions

2. Four options for each question

3. Do not reveal answers immediately.

4. After all questions provide the answer key.

Keep the questions suitable for {difficulty} learners.
"""

    elif mode == "MCQs Only":

        prompt = f"""
Generate 10 MCQs on:

{question}

Difficulty:
{difficulty}

Include answers after every question.
"""

    elif mode == "Quick Revision":

        prompt = f"""
Create quick revision notes on:

{question}

Difficulty:
{difficulty}

Include:

• Important points

• Definitions

• Formulae (if applicable)

• Summary

Keep it concise.
"""

    else:

        prompt = f"""
You are an expert AI teacher.

Topic:
{question}

Difficulty:
{difficulty}

Generate:

1. Easy explanation

2. Key concepts

3. Important points

4. Real-life examples

5. Five MCQs with answers

6. Three interview questions

7. Quick revision summary

Explain according to the selected difficulty level.
"""

    if exam_mode:
        prompt += """

Also focus on:

• Important exam questions

• Frequently asked concepts

• Short answer format

• Revision tips
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    with st.chat_message("assistant"):

      with st.spinner("🧠 AI is preparing your study material..."):

            response = requests.post(url, json=body)

            result = response.json()

            try:

                answer = result["candidates"][0]["content"]["parts"][0]["text"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except:

                st.error("Unable to generate response.")

st.sidebar.divider()

questions = len(
    [m for m in st.session_state.messages if m["role"] == "user"]
)

answers = len(
    [m for m in st.session_state.messages if m["role"] == "assistant"]
)

st.sidebar.markdown("## 📊 Dashboard")

st.sidebar.metric("📖 Questions Asked", questions)

st.sidebar.metric("🤖 Responses Generated", answers)
st.sidebar.divider()

if st.session_state.messages:

    chat = ""

    for msg in st.session_state.messages:
        chat += f"{msg['role'].upper()}\n{msg['content']}\n\n"

    st.sidebar.download_button(
        "📥 Download Chat",
        chat,
        file_name="Study_Chat.txt",
        mime="text/plain"
    )

st.sidebar.divider()

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.divider()

st.markdown(
"""
<div style='text-align:center; color:gray; font-size:16px;'>

Made with ❤️ by Disha using Streamlit & Gemini AI

</div>
""",
unsafe_allow_html=True
)
