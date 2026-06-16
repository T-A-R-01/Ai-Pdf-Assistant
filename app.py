import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI PDF Research Assistant",
    page_icon="📚",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FB;
    color: #111827;
}

header, footer {
    visibility: hidden;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

.main .block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* ===== TITLE ===== */

.title {
    font-size: 3.2rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.05rem;
    color: #6B7280;
    margin-bottom: 2rem;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #E5E7EB;
}

.sidebar-box {
    background: #EEF4FF;
    border: 1px solid #C7D7FE;
    padding: 1rem;
    border-radius: 14px;
    color: #1D4ED8;
    margin-bottom: 1rem;
}

/* ===== FILE UPLOADER ===== */

[data-testid="stFileUploader"] {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

[data-testid="stFileUploader"] section {
    background: #F9FAFB;
    border: 2px dashed #D1D5DB;
    border-radius: 14px;
    padding: 0.7rem !important;
}

/* ===== INPUT ===== */

.stTextInput input {
    border-radius: 14px !important;
    border: 1px solid #D1D5DB !important;
    padding: 0.9rem !important;
    background: white !important;
}

/* ===== BUTTONS ===== */

.stButton > button {
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-weight: 600;
    font-size: 1rem;
}

.stButton > button:hover {
    background: #1D4ED8;
}

/* ===== CHAT ===== */

[data-testid="stChatMessage"] {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* ===== CURRENT PDF CARD ===== */

.current-pdf {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    font-weight: 600;
}

/* ===== ALERTS ===== */

.stSuccess,
.stError,
.stInfo,
.stWarning {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 📄 Document")

    st.divider()

    if st.session_state.uploaded_file_name:

        st.markdown(
            f"""
            <div class="sidebar-box">
                <b>{st.session_state.uploaded_file_name}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.pdf_processed:
            st.success("Ready for Questions ✅")

    else:

        st.markdown(
            """
            <div class="sidebar-box">
                No PDF uploaded yet
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- TITLE ----------------

st.markdown(
    '<div class="title">📚 AI PDF Research Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Chat with your PDFs using AI-powered Retrieval-Augmented Generation (RAG)</div>',
    unsafe_allow_html=True
)

# ---------------- CURRENT PDF ----------------

if st.session_state.uploaded_file_name:

    st.markdown(
        f"""
        <div class="current-pdf">
            📄 Current PDF: {st.session_state.uploaded_file_name}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- PDF UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    # If NEW PDF uploaded → clear old chat
    if uploaded_file.name != st.session_state.uploaded_file_name:

        st.session_state.messages = []
        st.session_state.pdf_processed = False

    st.session_state.uploaded_file_name = uploaded_file.name

    if st.button("Process PDF"):

        with st.spinner("Processing PDF..."):

            response = requests.post(
                "http://127.0.0.1:8000/upload-pdf",
                files={
                    "file": uploaded_file
                }
            )

            if response.status_code == 200:

                st.session_state.pdf_processed = True

                st.success("PDF processed successfully!")

            else:

                st.error("Error processing PDF")

# ---------------- CHAT HISTORY ----------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- QUESTION FORM ----------------

with st.form("question_form", clear_on_submit=True):

    question = st.text_input(
        "Ask a question",
        placeholder="Ask a question about the PDF..."
    )

    submit_button = st.form_submit_button("Ask Question")

# ---------------- HANDLE QUESTIONS ----------------

if submit_button:

    if not st.session_state.pdf_processed:

        st.error("Please upload and process a PDF first.")

    elif question.strip() == "":

        st.warning("Please enter a question.")

    else:

        # USER MESSAGE
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):

            st.markdown(question)

        # ASSISTANT RESPONSE
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={
                        "question": question
                    }
                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                else:

                    st.error("Error getting answer")