import fitz

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_groq import ChatGroq

from dotenv import load_dotenv

import os

load_dotenv()

def extract_text_from_pdf(pdf):

    pdf_data = pdf.read()

    doc = fitz.open(stream=pdf_data, filetype="pdf")

    documents = []

    for page_number in range(len(doc)):

        page = doc.load_page(page_number)

        text = clean_text(page.get_text("text"))

        documents.append({
            "text": text,
            "page": page_number + 1
        })

    return documents

def clean_text(text):

    text = text.replace("\n", " ")

    text = text.replace("\t", " ")

    text = " ".join(text.split())

    return text

def split_text_into_chunks(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )

    chunks = []

    for doc in documents:

        split_chunks = splitter.split_text(doc["text"])

        for chunk in split_chunks:

            chunks.append({
                "content": chunk,
                "page": doc["page"]
            })

    return chunks

def create_vector_store(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = [chunk["content"] for chunk in chunks]

    metadata = [
        {"page": chunk["page"]}
        for chunk in chunks
    ]

    vector_store = FAISS.from_texts(
        texts,
        embedding=embeddings,
        metadatas=metadata
    )

    vector_store.save_local("faiss_index")
    
    with open("full_document.txt", "w", encoding="utf-8") as f:

        for chunk in chunks:
            f.write(chunk["content"] + "\n\n")
    
def answer_user_question(user_question):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    question_lower = user_question.lower()

    # SUMMARY MODE
    if "summarize" in question_lower:

        with open("full_document.txt", "r", encoding="utf-8") as f:
            context = f.read()

        sources = {"Full Document"}

    # TOPIC / SESSION MODE
    elif "sessions" in question_lower or "topics" in question_lower:

        docs = vector_store.similarity_search(
            "sessions workshop topics cybersecurity schedule",
            k=4
        )

        sources = set()

        for doc in docs:

            if "page" in doc.metadata:
                sources.add(f"Page {doc.metadata['page']}")

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

    # DEFAULT QA MODE
    else:

        docs = vector_store.similarity_search(
            user_question,
            k=3
        )

        sources = set()

        for doc in docs:

            if "page" in doc.metadata:
                sources.add(f"Page {doc.metadata['page']}")

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.2,
        max_tokens=500
    )

    prompt = f"""
    You are an AI PDF research assistant.

    Answer ONLY using the provided context.

    Rules:
    - Use only exact or clearly inferable information from the document.
    - Do not invent information.
    - Do not repeat sentences.
    - Keep answers concise and structured.
    - If information is unavailable, mention it only once.
    - Do not generate fake schedules, timings, venues, or placeholder text.

    For summaries:
    - Provide a clean professional summary.
    - Mention only the actual topics from the document.
    - Use bullet points when useful.
    - Keep the summary factual and grounded.

    Context:
    {context}

    Question:
    {user_question}

    Answer:
    """

    response = llm.invoke(prompt)

    # Format sources
    source_text = "\n\nSources:\n"

    for source in sorted(sources):
        source_text += f"- {source}\n"

    return response.content + source_text