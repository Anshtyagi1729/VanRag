from generator import ask_llm
from ingest import VectorStore,RecursiveTextSplitter,documentLoader
#scraping and storing the doc 
doc_path="docs.text"
url="https://www.crummy.com/software/BeautifulSoup/bs4/doc/"
documentLoader.load_webpage(url,doc_path)
with open(doc_path,"r",encoding="utf-8") as f:
    full_text=f.read()
#splittin the text
splitter=RecursiveTextSplitter(chunk_size=500,chunk_overlap=100)
chunks=splitter.split_text(full_text)
#embed and index the chunks 
vs=VectorStore()
vs.build_index(chunks)
#rag chat pipeline
print("ask the question about the document \n")
while True:
    user_query=input("you:").strip()
    if user_query.lower() in ("exit", "quit"):
        print("👋 Exiting chat.")
        break
    top_chunks = vs.query(user_query, k=3)
    context = "\n\n".join([c["chunk"] for c in top_chunks])
    
    ans=ask_llm(prompt=user_query,context=context)
    print(f"\n llm: {ans}")

