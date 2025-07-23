import ollama

def ask_llm(query: str, context: str = None, model: str = "gemma3:latest") -> str:
    """
    Query the Ollama LLM with the given query and optional context using the specified model.
    Returns the LLM's response as a string.
    """
    prompt = query
    if context:
        prompt = f""" BAsed on the context provided to you please answer the user query only answer based ont he query. if the question is in bengali then answer in bengali only. Correctly format the answer. Answer like you are a terrific human assistant.
        the Context:\n{context}\n\n and the Question: {query} now generate the answer. thank you. If the query is vague and the context is missing or not very appropriate then ask the user to ask more specific questions."""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content'] 