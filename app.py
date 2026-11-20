import os
import uuid
import requests
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# Configuration
# -------------------------------

API_URL = os.getenv(
    "RAG_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

st.set_page_config(
    page_title="Advanced RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------
# Custom Dark Theme
# -------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background-color: #161b22;
    }

    [data-testid="stHeader"] {
        background-color: #0e1117;
    }

    h1, h2, h3, p, label {
        color: #f1f5f9;
    }

    h1 {
        text-align: center;
    }

    .subtitle {
        text-align: center;
        color: #a1a1aa;
        font-size: 16px;
    }

    [data-testid="stChatMessage"] {
        background-color: #1c2430;
        border: 1px solid #303b4b;
        border-radius: 12px;
        padding: 12px;
    }

    [data-testid="stChatInput"] {
        background-color: #1c2430;
        border: 1px solid #303b4b;
        border-radius: 12px;
    }

    [data-testid="stChatInput"] textarea {
        color: #ffffff;
        caret-color: #ffffff;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #a1a1aa;
    }

    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    [data-testid="stMarkdownContainer"] {
        color: #f1f5f9;
    }

    hr {
        border-color: #303b4b;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------

st.title("🤖 Advanced RAG Chatbot")

st.markdown(
    '<p class="subtitle">'
    'Ask questions about your company policy documents'
    '</p>',
    unsafe_allow_html=True
)

st.divider()

# -------------------------------
# Session Initialization
# -------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    st.write("**Knowledge Base:**")
    st.success("Company Policy Documents")

    st.divider()

    st.caption("Backend Connection")
    st.code(API_URL)

    if st.button("🗑️ Clear Chat", use_container_width=True):

        try:
            response = requests.delete(
                f"{API_URL}/clear-history/"
                f"{st.session_state.session_id}",
                timeout=15
            )

            response.raise_for_status()

            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())

            st.success("Conversation cleared.")
            st.rerun()

        except requests.RequestException as e:
            st.error(f"Could not clear chat: {e}")

    st.divider()

    st.caption(
        "Powered by FastAPI, LangChain, Supabase and Groq"
    )

# -------------------------------
# Display Chat History
# -------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Chat Input
# -------------------------------

question = st.chat_input(
    "Ask something about company policies..."
)

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "question": question
                    },
                    timeout=180
                )

                response.raise_for_status()

                data = response.json()
                answer = data["answer"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. Please try again."
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to the RAG backend. "
                    "Please check the API service."
                )

            except requests.exceptions.HTTPError as e:

                st.error(
                    f"Backend returned an error: {e.response.text}"
                )

            except (requests.RequestException, KeyError, ValueError) as e:

                st.error(f"Something went wrong: {e}")
