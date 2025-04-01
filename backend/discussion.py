from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", temperature=0)

def generate_discussion(summary, host_name="Rahul"):
    """
    Generate a podcast-style AI discussion using LLaMA 3.1 (8B).
    """

    if len(summary.split()) < 20:
        prompt = f"""
        You are two AI hosts discussing the topic '{summary}' in a podcast-style conversation.
        Host A is named {host_name}, and Host B is named Emy.

        {host_name}: Welcome to our AI podcast! Today, we will discuss an interesting topic: {summary}.
        Emy: Yes, it's a fascinating topic! Let's dive in.

        Continue the discussion in an engaging manner, providing different perspectives, examples, and interesting facts.
        """
    else:
        prompt = f"""
        You are two AI hosts discussing the following document in a podcast-style conversation:

        {summary}

        Host A is named {host_name}, and Host B is named Emy.

        {host_name}: Welcome to our AI podcast! Today, we will discuss this fascinating document.
        Emy: Absolutely! Here's a brief overview:

        Continue the discussion in an engaging manner, breaking down the concepts and explaining them.
        """

    response = llm.invoke(prompt)
    return response.content.strip() if hasattr(response, 'content') else str(response).strip()
