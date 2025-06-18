from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# OR (preferred in latest releases):
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings

# Load the vector store
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_medlineplus", embedding_function=embedding_model)

query = "What are the symptoms of diabetes?"
results = vectorstore.similarity_search(query, k=2)

for doc in results:
    print("\nSource:", doc.metadata["source"])
    print(doc.page_content[:500], "...")
