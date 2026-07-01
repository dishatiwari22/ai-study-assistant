import streamlit as st
import requests
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


st.set_page_config(
    page_title="AI Smart Study Assistant",
    page_icon="🤖",
    layout="wide"
)

API_KEY = st.secrets["GEMINI_API_KEY"]


def create_pdf(messages):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter
    y = height - 40

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "AI Smart Study Assistant")
    y -= 30

    pdf.setFont("Helvetica", 11)

    for msg in messages:
        role = msg["role"].capitalize()

        lines = msg["content"].split("\n")

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, role)
        y -= 18

        pdf.setFont("Helvetica", 11)

        for line in lines:

            if y < 50:
                pdf.showPage()
                y = height - 40

            pdf.drawString(60, y, line[:100])
            y -= 15

        y -= 10

    pdf.save()
    buffer.seek(0)
    return buffer

# ---------------- HEADER ----------------
st.title("🤖 AI Smart Study Assistant")

st.markdown(
    """
Ask any study question and receive AI-generated explanations,
notes, examples, MCQs, interview questions and summaries.
"""
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Study Settings")

mode = st.sidebar.selectbox(
    "Learning Mode",
    [
        "Study Notes",
        "Quick Revision",
        "MCQs Only"
    ]
)

exam_mode = st.sidebar.checkbox("🎯 Exam Mode")

st.sidebar.divider()

st.sidebar.subheader("💡 Suggested Topics")

topics = [
    "Python",
    "Machine Learning",
    "Artificial Intelligence",
    "Operating System",
    "DBMS",
    "Computer Networks",
    "Data Structures",
    "Java"
]

for t in topics:
    st.sidebar.write("•", t)

st.sidebar.divider()

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SHOW CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
question = st.chat_input("Ask your study question...")

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    prompt = f"""
You are an expert teacher.

Learning Mode:
{mode}

Student Question:
{question}

Generate:

1. Easy Explanation

2. Important Concepts

3. Key Points

4. Real-life Examples

5. 5 MCQs with Answers

6. 3 Interview Questions

7. Quick Revision Summary

Write in simple English.

Use headings and bullet points.
"""

    if exam_mode:
        prompt += """

Focus on:
- High probability exam questions
- Important definitions
- Short answers
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={API_KEY}"
    )

    body = {
        "contents":[
            {
                "parts":[
                    {
                        "text":prompt
                    }
                ]
            }
        ]
    }

    with st.chat_message("assistant"):

        with st.spinner("Generating..."):

            response = requests.post(url, json=body)

            data = response.json()

            try:

                answer = data["candidates"][0]["content"]["parts"][0]["text"]

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role":"assistant",
                        "content":answer
                    }
                )

            except:

                st.error("Unable to generate response.")

# ---------------- SIDEBAR TOOLS ----------------
st.sidebar.divider()

st.sidebar.subheader("📄 Export Chat")

if st.session_state.messages:

    pdf = create_pdf(st.session_state.messages)

    st.sidebar.download_button(
        "⬇ Download PDF",
        pdf,
        file_name="Study_Chat.pdf",
        mime="application/pdf"
    )

st.sidebar.divider()

st.sidebar.subheader("📊 Chat Statistics")

user_questions = len(
    [m for m in st.session_state.messages if m["role"]=="user"]
)

assistant_answers = len(
    [m for m in st.session_state.messages if m["role"]=="assistant"]
)

st.sidebar.write(f"Questions : {user_questions}")
st.sidebar.write(f"Responses : {assistant_answers}")

st.sidebar.divider()

if st.sidebar.button("🗑 Clear Chat"):

    st.session_state.messages=[]

    st.rerun()
