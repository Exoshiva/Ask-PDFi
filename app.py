import streamlit as st
import time
from rag_core import process_pdf_to_vectorstore, get_rag_answer

# --- PAGE CONFIG ---
st.set_page_config(page_title="RAG PDF Chat", page_icon="📄", layout="centered")

# --- SESSION STATE ---
# Speichert Chat-Verlauf und Status, damit beim Neuladen nichts verschwindet
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# --- MOCK BACKEND FUNCTIONS (Werden später ersetzt) ---
def process_pdf_mock(file):
    """Simuliert das Verarbeiten des PDFs (Embeddings erstellen)."""
    time.sleep(1.5) # Simuliere Ladezeit
    st.session_state.pdf_processed = True

def get_llm_answer_mock(question):
    """Simuliert die Antwort der KI."""
    return f"Hier ist die simulierte Antwort auf: '{question}'"

# --- SIDEBAR (Upload) ---
with st.sidebar:
    st.header("📄 Dokumenten-Upload")
    uploaded_file = st.file_uploader("PDF hier ablegen", type=["pdf"])
    
    if st.button("PDF verarbeiten"):
            with st.spinner("Lese PDF und erstelle Embeddings..."):
                # ECHTE FUNKTION AUFRUFEN UND SPEICHERN
                st.session_state.vectorstore = process_pdf_to_vectorstore(uploaded_file)
                st.session_state.pdf_processed = True
            st.success("PDF erfolgreich verarbeitet!")
    else:
        # Reset, falls das PDF gelöscht wird
        st.session_state.pdf_processed = False
        st.info("Bitte lade ein PDF hoch, um zu starten.")

# --- MAIN CHAT AREA ---
st.title("💬 RAG Chat Assistant")
st.markdown("Stelle Fragen zu deinem hochgeladenen PDF.")

# Bisherige Chat-Historie anzeigen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
# Inputfeld deaktivieren, wenn kein PDF verarbeitet wurde
if not st.session_state.pdf_processed:
    st.chat_input("Bitte lade zuerst ein PDF in der Seitenleiste hoch.", disabled=True)
else:
    # Wenn der User eine Frage tippt
    if prompt := st.chat_input("Was möchtest du aus dem PDF wissen?"):
        
        # User Message anzeigen und im State speichern
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # KI Antwort generieren, anzeigen und speichern
        # KI Antwort mit dem echten Gehirn generieren
        with st.chat_message("assistant"):
            # ECHTE FUNKTION AUFRUFEN
            answer = get_rag_answer(st.session_state.vectorstore, prompt)
            st.markdown(answer)