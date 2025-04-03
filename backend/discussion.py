from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.1:8b", temperature=0)

def generate_discussion(summary, host_name="Rahul", host_name_2="Emy"):
    """
    Generate a podcast-style AI discussion using LLaMA 3.1 (8B) with consistent intro and outro.
    """

    # Decide what to say in the intro based on the summary
    intro_topic = (
        summary.split('.')[0]
        if len(summary.split()) < 20
        else "a fascinating topic"
    )

    # Shared intro
    intro = f"""
{host_name}: Welcome to the AI Research Centre Podcast, me {host_name}, with my co-host, {host_name_2}.
{host_name_2}: That's right! Today we're diving into {intro_topic}.
{host_name}: Let's get started!
"""

    # Short or long form discussion prompt
    if len(summary.split()) < 20:
        prompt = f"""
You are two AI hosts discussing the topic '{summary}' in a podcast-style conversation.
Host A is named {host_name}, and Host B is named {host_name_2}.

Start the discussion after this intro, and don't give intro again in the discussion as its already generated:
{intro}

Make the conversation engaging, natural, and informative. Include perspectives, examples, and fun insights.
Ensure speaker labels are formatted as '{host_name}:' and '{host_name_2}:' — without asterisks or extra formatting.
"""
    else:
        prompt = f"""
You are two AI hosts discussing the following document in a podcast-style conversation:
{summary}

Host A is named {host_name}, and Host B is named {host_name_2}.

Start the discussion after this intro, and don't give intro again in the discussion as its already generated:
{intro}

{host_name_2}: First, let me give you a brief overview of what we're discussing today.

Make the conversation insightful, clear, and lively. Break down complex ideas with simple explanations and real-world examples. 
Ensure speaker labels are formatted as '{host_name}:' and '{host_name_2}:' — without asterisks or extra formatting.
"""

    # Get response from LLM
    response = llm.invoke(prompt)
    discussion_content = response.content.strip() if hasattr(response, 'content') else str(response).strip()

    # Outro to close the podcast
    outro = f"""
{host_name}: That wraps up our discussion for today!
{host_name_2}: We hope you enjoyed this episode.
{host_name}: Until next time, stay curious and keep exploring!
"""

    return f"{intro}\n\n{discussion_content}\n\n{outro}"
