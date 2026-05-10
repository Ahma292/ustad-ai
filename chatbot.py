import streamlit as st
from groq import Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(
    page_title="Ustad AI",
    page_icon="🎓",
    layout="wide"
)

MODE_PROMPTS = {
    "general": """You are Ustad AI, a friendly Pakistani student assistant from Peshawar.
Help students with any topic in Roman Urdu and English mixed style.
Be friendly like a senior student. Use bullet points for clarity.
Start with 'Salam!' or 'Ji bilkul!' and end with encouragement.""",

    "mcq": """You are Ustad AI in MCQ Practice Mode.
When a student gives you a topic, generate 5 multiple choice questions with 4 options each (A, B, C, D).
After student answers, tell them which are correct and explain why.
Always reply in Roman Urdu and English mixed style.
Format MCQs clearly and numbered.""",

    "math": """You are Ustad AI in Math Solver Mode.
Solve any math problem step by step in very simple words.
Show each step clearly with explanation in Roman Urdu and English.
Always verify the answer at the end.""",

    "exam": """You are Ustad AI in Exam Preparation Mode.
Help students prepare for exams by giving important topics, short notes and memory tips.
Always reply in Roman Urdu and English mixed style.""",

    "assignment": """You are Ustad AI in Assignment Helper Mode.
Help students with assignments with clear structured answers.
Always reply in Roman Urdu and English mixed style."""
}

MODE_NAMES = {
    "general": "💬 General Chat",
    "mcq": "❓ MCQ Practice",
    "math": "🔢 Math Solver",
    "exam": "📝 Exam Prep",
    "assignment": "✍️ Assignment Help"
}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "general"

# Sidebar
with st.sidebar:
    st.title("🎓 Ustad AI")
    st.caption("Pakistan ka Pehla AI Tutor")
    st.divider()

    st.markdown("**Mode Select Karo:**")
    for mode_key, mode_name in MODE_NAMES.items():
        if st.button(mode_name, key=mode_key, use_container_width=True):
            st.session_state.mode = mode_key
            st.session_state.messages = []
            st.rerun()

    st.divider()
    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Header
st.title("🎓 Ustad AI")
st.caption(f"آپ کا ذہین پاکستانی استاد | Current Mode: {MODE_NAMES[st.session_state.mode]}")
st.divider()

# Welcome
if len(st.session_state.messages) == 0:
    st.info("👋 Salam! Main Ustad AI hoon! Apna sawal likhein ya sidebar se mode select karein!")

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
placeholder = {
    "general": "Apna sawal likhein...",
    "mcq": "Subject ka naam likhein jaise Physics, Math...",
    "math": "Math problem likhein jaise 2x + 5 = 15...",
    "exam": "Subject aur topic likhein...",
    "assignment": "Assignment topic likhein..."
}

user_input = st.chat_input(placeholder[st.session_state.mode])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Ustad AI soch raha hai... 🤔"):
        messages_with_system = [
            {"role": "system", "content": MODE_PROMPTS[st.session_state.mode]}
        ] + st.session_state.messages

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_with_system
        )
        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)