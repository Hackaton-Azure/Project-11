import ollama  # Make sure you have the ollama Python client installed

def llm_rank(description):
    """
    Use Ollama LLM to rank documents by relevance to a description.

    Args:
        description (str): The query or description text.
        documents (list of str): List of candidate reference texts.
        top_k (int): Number of top references to return.

    Returns:
        list of str: The top_k most relevant documents.
    """

    with open('Script.txt', "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = prompt_template.format(description=description)

    response = ollama.generate(model="gemma3:27b", prompt=prompt)['response']
    return response