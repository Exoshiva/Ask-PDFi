import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings # LOKAL!
from langchain_groq import ChatGroq # OPEN SOURCE HOSTING
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Lädt die geheimen Umgebungsvariablen
load_dotenv()

def process_pdf_to_vectorstore(uploaded_file):
    """
    Nimmt das PDF, liest den Text, zerteilt ihn und speichert ihn als Embeddings.
    Gibt den fertigen Vectorstore zurück.
    """
    # A. Text aus dem PDF extrahieren
    raw_text = ""
    pdf_reader = PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        raw_text += page.extract_text()
        
    # B. Text in kleine "Häppchen" (Chunks) zerteilen
    # LLMs können nicht endlos viel Text auf einmal lesen, daher zerlegen wir ihn.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Jeder Chunk hat ca. 1000 Zeichen
        chunk_overlap=200     # 200 Zeichen Überlappung, damit kein Satz in der Mitte abreißt
    )
    text_chunks = text_splitter.split_text(raw_text)
    
    # C. EIGENE INFRASTRUKTUR: Lokale Embeddings
    # Wir tauschen OpenAI gegen Hugging Face aus. Diese laufen direkt auf deinem Server.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    
    return vectorstore

def get_rag_answer(vectorstore, user_question):
    """
    Nimmt die Frage des Users, sucht im Vectorstore nach passendem Kontext 
    und generiert mit dem LLM eine Antwort.
    """
    # A. EIGENES LLM: Llama 3 via Groq
    # Wir nutzen ein Open-Source-Modell über die extrem schnelle Groq-Infrastruktur.
    llm = ChatGroq(temperature=0, model_name="llama3-8b-8192")
    
    # B. Wie soll sich die KI verhalten? (Der System Prompt)
    system_prompt = (
        "Du bist ein hilfreicher Assistent. Nutze NUR den folgenden Kontext, "
        "um die Frage zu beantworten. Wenn du die Antwort im Kontext nicht findest, "
        "sage, dass du es nicht weißt. Erfinde nichts dazu.\n\n"
        "Kontext:\n{context}"
    )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # C. Die RAG-Kette zusammenbauen
    # Kombiniert die gefundenen Dokumente mit dem LLM
    question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
    
    # Holt die relevantesten Chunks aus der Datenbank
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # Holt die 3 besten Treffer
    
    # Verbindet Retriever und LLM zur finalen Kette
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # D. Die Frage ausführen und Antwort zurückgeben
    response = rag_chain.invoke({"input": user_question})
    return response["answer"]