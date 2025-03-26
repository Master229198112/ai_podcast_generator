from langchain_ollama import ChatOllama

# Initialize LLaMA 3.1 (8B) model with ChatOllama
llm = ChatOllama(model="llama3.1:8b", temperature=0)

def generate_discussion(summary):
    """
    Generate a podcast-style AI discussion using LLaMA 3.1 (8B) via ChatOllama.
    """
    # Check if input is a topic or a full summary
    if len(summary.split()) < 20:  # Assuming short input is a topic
        prompt = f"""
        You are two AI hosts discussing the topic '{summary}' in a podcast-style conversation.
        Generate a natural dialogue format.
        Name of Host A is Rahul.
        Name of Host B is Kusum.

        Rahul: Welcome to our AI podcast! Today, we will discuss an interesting topic: {summary}.
        Kusum: Yes, it's a fascinating topic! Let's dive in.

        Continue the discussion in an engaging manner, providing different perspectives, examples, and interesting facts.
        """
    else:
        prompt = f"""
        You are two AI hosts discussing the following document in a podcast-style conversation:
        
        {summary}
        
        Generate a natural dialogue format.
        Name of Host A is Rahul.
        Name of Host B is Kusum.

        Rahul: Welcome to our AI podcast! Today, we will discuss this fascinating document.
        Kusum: Absolutely! Here's a brief overview:

        Continue the discussion in an engaging manner, breaking down the concepts and explaining them.
        """

    # Generate discussion using LLaMA 3.1 (8B) via Ollama
    response = llm.invoke(prompt)
    
    # Extract text from AIMessage object
    if hasattr(response, 'content'):
        return response.content.strip()  # Extract the text and remove extra spaces
    else:
        return str(response).strip()  # Convert to string if needed
