from sentence_transformers import SentenceTransformer
import faiss 
import numpy as np 
class VectorStore:
    def __init__(self,model_name='all-MiniLM-L6-v2'):
        self.model=SentenceTransformer(model_name)
        self.index=None
        self.docstore={}
    def build_index(self,chunks):
        #convert to embedding 
        embeddings=self.model.encode(chunks,convert_to_numpy=True)
        dimension=embeddings.shape[1]
        #creating the faiss index 
        self.index=faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        #create the doc store
        self.docstore={i:{"chunk":chunks[i]} for i in range(len(chunks))}
    def query(self,text,k=3):
        query_embedding=self.model.encode([text])
        #searching in faiss
        D,I=self.index.search(query_embedding,k)
        return [self.docstore[i] for i in I[0]]
    def save_index(self,path="faiss_index.bin"):
        faiss.write_index(self.index,path)
    def load_index(self,path="faiss_index.bin"):
        self.index=faiss.read_index(path)
    def get_chunk_by_id(self,idx):
        return self.docstore.get(idx,None)

        
        