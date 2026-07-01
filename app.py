import streamlit as st
import requests

API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(
    page_title="AI Smart Study Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Smart Study Assistant")
st.markdown("Your personal AI tutor for study notes, revision, quizzes and interview preparation.")
st.divider()

st.sidebar.title("⚙️ Study Settings")

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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask your study question...")

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

    elif mode == "MC
    
