from transformers import pipeline
import torch

def summarize_text(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"  # Use GPU if available

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if device == "cuda" else -1)
    
    summary = summarizer(text, max_length=200, min_length=50, do_sample=False)
    return summary[0]['summary_text']
