# === tools.py ===
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools import tool

def load_health_retriever_tool():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory="chroma_medlineplus",
        embedding_function=embedding_model
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    retriever_tool = create_retriever_tool(
        retriever,
        name="medlineplus_health_retriever",
        description="Search for health-related topics from MedlinePlus like symptoms, diseases, treatments, and body systems. Use this tool for any health-related question."
    )
    return retriever_tool

@tool
def extract_report_text(file_path: str) -> str:
    """Extracts and cleans text from medical PDF reports."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return "\n".join([p.page_content for p in pages])