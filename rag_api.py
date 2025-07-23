from fastapi import FastAPI, Query
from pydantic import BaseModel
from vector_module import create_or_load_collection, query_collection
from llm_module import ask_llm

PDF_PATH = "tenms.pdf"
COLLECTION_NAME = "tenms_rag"

# Load collection on startup
collection = create_or_load_collection(COLLECTION_NAME)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(request: QueryRequest):
    user_query = request.query
    results = query_collection(collection, user_query, top_k=3)
    context = "\n\n".join(results['documents'][0]) if results['documents'] else ""
    answer = ask_llm(user_query, context=context)
    return {"answer": answer} 