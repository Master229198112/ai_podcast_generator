from langchain_ollama import ChatOllama

# Initialize LLaMA 3.1 (8B) model with ChatOllama
llm = ChatOllama(model="llama3.1:8b", temperature=0)

def generate_discussion(summary):
    """
    Generate a podcast-style AI discussion using LLaMA 3.1 (8B) via ChatOllama.
    """
    prompt = f"""
    You are two AI hosts discussing a document or Input provide by user in a podcast-style conversation.
    Generate a natural dialogue format. 
    Name of Host A is Rahul
    Name of Host B is Kusum

    Rahul: Welcome to our AI podcast! Today, we will discuss an interesting topic.
    Kusum: Yes! Here’s a brief about the topic:

    {summary}

    Rahul: That’s fascinating! Can you provide more details?
    Kusum: Of course! Let’s break it down...

    Continue the discussion in an engaging manner.
    """

    # Generate discussion using LLaMA 3.1 (8B) via Ollama
    response = llm.invoke(prompt)
    
    # Extract text from AIMessage object
    if hasattr(response, 'content'):
        return response.content.strip()  # Extract the text and remove extra spaces
    else:
        return str(response).strip()  # Convert to string if needed
