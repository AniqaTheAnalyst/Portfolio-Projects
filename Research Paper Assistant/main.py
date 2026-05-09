import os
import pickle
import time
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()  # loads from .env file

# ✅ must be first streamlit command
st.set_page_config(
    page_title="Research Paper Assistant",
    page_icon="📚",
    layout="wide"
)

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=groq_api_key)

st.title("📚 Research Paper Assistant")
st.markdown("### Understand any research paper by asking questions!")

st.sidebar.title("📎 Paste Paper URLs")
st.sidebar.markdown("Paste up to 3 research paper URLs below:")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_urls = st.sidebar.button("Process URLs")
file_path = "vector_index_storage.pkl"
main_placeholder = st.empty()

if process_urls:
    urls = [u for u in urls if u.strip()]

    if not urls:
        st.sidebar.error("Please paste at least one URL!")
    else:
        # Step 1 - Load
        main_placeholder.text("📖 Loading papers...")
        loader = WebBaseLoader(urls)
        data = loader.load()

        if not data:
            main_placeholder.text("❌ Could not load URLs!")
            st.stop()

        # Step 2 - Split
        main_placeholder.text("✂️ Splitting into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " "],
            chunk_size=400,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(data)

        if not chunks:
            main_placeholder.text("❌ No content extracted!")
            st.stop()

        # Step 3 - Embeddings
        main_placeholder.text("🔢 Creating embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vector_index = FAISS.from_documents(chunks, embeddings)
        time.sleep(2)

        # Save using FAISS native method (more reliable than pickle)
        vector_index.save_local("faiss_index")

        main_placeholder.text("✅ Ready! Ask your question below.")

# Question answering
query = main_placeholder.text_input("Question: ")

if query:
    if os.path.exists("faiss_index"):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vector_index = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vector_index.as_retriever()
        )

        result = qa_chain.invoke({"query": query})
        st.header("Answer")
        st.write(result["result"])
    else:
        st.warning("⚠️ Please process some URLs first using the sidebar.")
