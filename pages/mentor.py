import streamlit as st 
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import SystemMessagePromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("hf")

st.set_page_config(
    page_title="Mentor Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -------------------- MODERN UI CSS --------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: radial-gradient(circle at top, #1e293b, #020617);
    font-family: 'Inter', system-ui, sans-serif;
}

/* Header */
.mentor-header {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 18px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

.mentor-header h1 {
    color: #f8fafc;
    font-size: 1.9rem;
    margin-bottom: 6px;
}

.mentor-header .meta {
    color: #94a3b8;
    font-size: 0.85rem;
}

/* Chat bubbles */
.chat-user {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 14px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 10px 0;
    max-width: 78%;
    margin-left: auto;
    box-shadow: 0 8px 20px rgba(37,99,235,0.35);
    animation: pop 0.25s ease;
}

.chat-ai {
    background: rgba(255,255,255,0.10);
    color: #e5e7eb;
    padding: 14px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 10px 0;
    max-width: 78%;
    margin-right: auto;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.35);
    animation: pop 0.25s ease;
}

/* Input */
textarea {
    border-radius: 14px !important;
}

/* Download button */
div.stDownloadButton > button {
    width: 100%;
    height: 46px;
    border-radius: 14px;
    font-weight: 600;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: white;
    border: none;
}

div.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(34,197,94,0.35);
}

/* Animation */
@keyframes pop {
    from {
        opacity: 0;
        transform: scale(0.97);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION VALUES --------------------
selection = st.session_state.get("selection", "No topic selected")
exp = st.session_state.get("exp", "No experience value set")

# -------------------- HEADER --------------------
st.markdown(f"""
<div class="mentor-header">
    <h1>🤖 {selection} Mentor</h1>
    <div class="meta">
        {exp} Years Industry Experience · Strict Module Enforcement
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- SYSTEM PROMPT --------------------
sm = SystemMessagePromptTemplate.from_template("""
You are a senior technical mentor with **{YEARS} years of real-world industry experience**.

Your responsibility is to mentor learners **ONLY in the selected module: {MODULE}**.

AVAILABLE MODULES (FIXED):
- Python
- SQL
- Power BI
- EDA
- Machine Learning
- Deep Learning
- Generative AI
- Agentic AI

MODULE ENFORCEMENT RULES (NON-NEGOTIABLE):
- You MUST answer questions **only if they strictly belong to {MODULE}**.
- If a question involves concepts from ANY other module, you MUST REFUSE.
- You must NOT combine, bridge, or reference other modules in your answers.
- You must NOT provide background knowledge from other domains.
- You must NOT infer intent — judge strictly by the question content.

REFUSAL RESPONSE (EXACT FORMAT):
This question is outside the selected module ({MODULE}).  
Please ask a question related only to {MODULE}.

ANSWERING GUIDELINES:
- Respond like a mentor with {YEARS} years of practical experience.
- Be precise, concise, and technically accurate.
- Use examples ONLY if they belong strictly to {MODULE}.
- No assumptions, no deviation.
""")

system_message = sm.format(YEARS=exp, MODULE=selection)

# -------------------- SESSION STATE --------------------
if "last_module" not in st.session_state:
    st.session_state["last_module"] = selection
    if "conv" not in st.session_state:
        st.session_state["conv"] = []
        st.session_state["memory"] = [("system", system_message.content)]

if st.session_state["last_module"] != selection:
    st.session_state["conv"] = []
    st.session_state["memory"].append(("system", system_message.content))
    st.session_state["last_module"] = selection

# -------------------- DISPLAY CHAT --------------------
for msg in st.session_state["conv"]:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-ai'>{msg['content']}</div>", unsafe_allow_html=True)

# -------------------- INPUT --------------------
prompt = st.chat_input("Ask a question strictly related to the selected module")

if prompt:
    st.session_state["conv"].append({"role": "user", "content": prompt})
    st.session_state["memory"].append(("user", prompt))
    st.markdown(f"<div class='chat-user'>{prompt}</div>", unsafe_allow_html=True)

    if selection in ["Python", "EDA"]:
        model = HuggingFaceEndpoint(repo_id="deepseek-ai/DeepSeek-V3.2")
    elif selection in ["SQL", "Power BI"]:
        model = HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.2-1B-Instruct")
    elif selection in ["Machine Learning", "Deep Learning"]:
        model = HuggingFaceEndpoint(repo_id="Qwen/Qwen2-7B")
    elif selection in ["Generative AI", "Agentic AI"]:
        model = HuggingFaceEndpoint(repo_id="XiaomiMiMo/MiMo-V2-Flash")

    llm = ChatHuggingFace(llm=model)
    response = llm.invoke(st.session_state["memory"]).content

    st.markdown(f"<div class='chat-ai'>{response}</div>", unsafe_allow_html=True)

    st.session_state["conv"].append({"role": "ai", "content": response})
    st.session_state["memory"].append(("ai", response))

# -------------------- DOWNLOAD CHAT --------------------
conversation_text = ""
for message in st.session_state["conv"]:
    conversation_text += f"{message['role'].capitalize()} : {message['content']}\n\n"

st.download_button(
    label="📥 Download Chat History",
    data=conversation_text,
    file_name="chat_history.txt",
    mime="text/plain"
)
