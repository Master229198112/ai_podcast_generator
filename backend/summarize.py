# from transformers import pipeline
# import torch

# def summarize_text(text):
#     device = "cuda" if torch.cuda.is_available() else "cpu"  # Use GPU if available

#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if device == "cuda" else -1)
    
#     summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
#     return summary[0]['summary_text']



from langchain_ollama import ChatOllama

def summarize_text(text):
    try:
        # Load LLaMA 3.1 model
        llm = ChatOllama(model="llama3.1:8b", temperature=0)

        # Summarization prompt
        prompt = f"Summarize the following text concisely:\n\n{text}\n\nSummary:"

        # Generate the summary using LLaMA 3.1
        response = llm.invoke(prompt)

        # Ensure the response is properly converted to text
        summary = str(response.content) if hasattr(response, 'content') else str(response)

        return summary.strip()

    except Exception as e:
        print(f"❌ Error during summarization: {e}")
        return "Error generating summary."
