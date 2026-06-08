import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Important: Setup the correct path according to our new structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "global_events.csv")
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")

def create_vector_db():
    print(f"Loading data from {CSV_PATH}...")
    
    # Check if file exists to prevent hard crashes
    if not os.path.exists(CSV_PATH):
        print("ERROR: global_events.csv not found! Please ensure data exists.")
        return False
        
    try:
        # Load static CSV data
        df = pd.read_csv(CSV_PATH)
        
        # Convert rows into LangChain Document objects
        documents = []
        for index, row in df.iterrows():
            # Customize this string based on your exact CSV column names
            # Assuming typical columns like 'Location', 'Event', 'Severity'
            content = f"Location: {row.get('Location', 'Unknown')} | Event: {row.get('Event', 'N/A')} | Severity: {row.get('Severity', 'Unknown')}"
            
            doc = Document(
                page_content=content,
                metadata={"source": "global_events.csv", "row": index}
            )
            documents.append(doc)
            
        print(f"Created {len(documents)} document chunks.")
        
        # Initialize Free & Fast HuggingFace Embeddings
        print("Initializing Embedding Model...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Create and Save the FAISS Vector Database
        print("Building FAISS Index...")
        vector_db = FAISS.from_documents(documents, embeddings)
        vector_db.save_local(FAISS_INDEX_PATH)
        
        print(f"SUCCESS: FAISS Index saved locally at {FAISS_INDEX_PATH}")
        return True
        
    except Exception as e:
        print(f"Failed to create vector DB: {e}")
        return False

if __name__ == "__main__":
    create_vector_db()