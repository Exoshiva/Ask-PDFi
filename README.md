# 🚀 Glorious Guide - Intelligent PDF Assistant

Ein prototypisches RAG-System (Retrieval-Augmented Generation), entwickelt als Proof-of-Concept für die Analyse interner Dokumente bei Ramblr.ai.

## 🛠 Tech-Stack
- **Frontend:** Streamlit
- **LLM:** Llama 3 (via Groq API)
- **Embeddings:** HuggingFace `all-MiniLM-L6-v2` (Lokal)
- **Vektor-Datenbank:** FAISS
- **Framework:** LangChain

## 🛡 DevSecOps & Qualität
Dieses Projekt nutzt eine gestaffelte Sicherheitsarchitektur:
1. **Pre-Commit Hooks:** Lokaler Scan mit `Bandit` vor jedem Commit.
2. **GitLab CI/CD:** Automatisierte Pipeline mit Syntax-Check und `pip-audit`.
3. **Secrets Management:** API-Keys werden verschlüsselt in Hugging Face Secrets verwaltet.

## 📖 Roadmap
- [x] Projekt-Setup & CI/CD Pipeline
- [ ] Implementierung der RAG-Logik (`rag_core.py`)
- [ ] UI-Entwicklung (`app.py`)
- [ ] Deployment auf Hugging Face Spaces