import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os

# ========== Configuration ==========
BASE_URL = "https://medlineplus.gov/lab-tests/"
CHROMA_DIR = "chroma_medlineplus"
MAX_PAGES = 1000

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

visited = set()
pages_content = []

# ========== Helper Functions ==========
def is_valid_url(url):
    parsed = urlparse(url)
    return (
        parsed.netloc == urlparse(BASE_URL).netloc and
        url.startswith(BASE_URL) and
        url not in visited
    )


def crawl(url):
    if len(visited) >= MAX_PAGES:
        return
    try:
        print(f"[⚙️] Visiting: {url}")
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code != 200:
            print(f"[x] Skipped (status {res.status_code}): {url}")
            return

        visited.add(url)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator=' ', strip=True)
        pages_content.append({"url": url, "text": text})
        print(f"[✓] Crawled: {url} ({len(visited)}/{MAX_PAGES})")

        for a in soup.find_all("a", href=True):
            next_url = urljoin(url, a["href"])
            if is_valid_url(next_url):
                crawl(next_url)

    except Exception as e:
        print(f"[!] Error: {url} -> {e}")

# ========== Main Execution ==========
def main():
    print("🚀 Starting crawl and ingestion...")

    # Step 1: Crawl pages
    crawl(BASE_URL)

    if not pages_content:
        print("⚠️ No pages were crawled. Exiting.")
        return

    print(f"📄 Total pages crawled: {len(pages_content)}")

    # Step 2: Prepare documents
    docs = [
        Document(page_content=page["text"], metadata={"source": page["url"]})
        for page in pages_content
    ]

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    # Step 3: Embed and store using Chroma
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(CHROMA_DIR):
        print(f"🗑️ Removing old ChromaDB directory: {CHROMA_DIR}")
        os.system(f"rm -rf {CHROMA_DIR}")

    print("📦 Storing vectors in ChromaDB...")
    vectorstore = Chroma.from_documents(chunks, embedding_model, persist_directory=CHROMA_DIR)
    vectorstore.persist()

    print("✅ All pages crawled and stored successfully in ChromaDB.")

if __name__ == "__main__":
    main()
