import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Important: Setup the correct path according to our new structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss_index")

def ask_classic_rag(query: str, supplier_name: str, location: str) -> str:
    """
    Function to query the static v1 RAG pipeline.
    """
    # 1. Load the existing Vector Database
    if not os.path.exists(FAISS_INDEX_PATH):
        return "ERROR: FAISS index not found. Please run ingest_faiss.py first."
        
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        
        # 2. Retrieve relevant past events
        search_query = f"{query} for {location} affecting {supplier_name}"
        docs = vector_db.similarity_search(search_query, k=3)
        
        context = "\n".join([doc.page_content for doc in docs])
        
        # If no relevant context found in static DB
        if not context.strip():
            context = "No historical data found in the static database for this location."

        # 3. Setup LLM & Prompt
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return "ERROR: GROQ_API_KEY is missing from environment variables."
            
        llm = ChatGroq(temperature=0.1, model_name="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
        
        prompt_template = PromptTemplate(
            input_variables=["supplier_name", "location", "context", "query"],
            template="""
            You are a Supply Chain Assistant (v1 Classic RAG).
            You have access to the following static historical data regarding past disruptions.
            
            Supplier: {supplier_name}
            Location: {location}
            
            HISTORICAL CONTEXT:
            {context}
            
            USER QUERY: {query}
            
            Please provide a short, informative answer based strictly on the provided historical context. 
            If the context does not contain the answer, explicitly state that you do not have real-time data and only possess static records.
            """
        )
        
        # 4. Generate Answer
        chain = prompt_template | llm
        response = chain.invoke({
            "supplier_name": supplier_name,
            "location": location,
            "context": context,
            "query": query
        })
        
        return response.content
        
    except Exception as e:
        return f"RAG Pipeline Error: {e}"