from ocr_module import extract_text_from_pdf
from vector_module import create_or_load_collection, add_documents, query_collection
from llm_module import ask_llm

PDF_PATH = "tenms.pdf"
COLLECTION_NAME = "tenms_rag"

# 1. Extract OCR text from PDF
print("Extracting text from PDF using OCR...")
doc_texts = extract_text_from_pdf(PDF_PATH)

# 2. Store in ChromaDB
print("Storing document chunks in ChromaDB...")
collection = create_or_load_collection(COLLECTION_NAME)
add_documents(collection, doc_texts)

# 3. Simple CLI loop for user queries
print("\nRAG system ready. Type your question (or 'exit' to quit):")
conversation_history = []
while True:
    user_query = input("\nYour question: ").strip()
    if user_query.lower() in ("exit", "quit"): break
    # 4. Retrieve relevant context
    results = query_collection(collection, user_query, top_k=3)
    context = "\n\n".join(results['documents'][0]) if results['documents'] else ""
    # Build conversation context
    conversation_context = ""
    if conversation_history:
        for turn in conversation_history:
            conversation_context += f"User: {turn['question']}\nAssistant: {turn['answer']}\n"
    # Add current context from retrieval
    if context:
        conversation_context += f"\nRelevant context:\n{context}\n"
    # 5. Query LLM
    print("\nQuerying LLM...")
    answer = ask_llm(user_query, context=conversation_context)
    # 6. Print answer
    print(f"\nAnswer:\n{answer}")
    # 7. Append to conversation history
    conversation_history.append({"question": user_query, "answer": answer}) 