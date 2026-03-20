import os
import requests

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

# code created referencing https://huggingface.co/blog/sentiment-analysis-python

def review_semantics(reviews: list[str]):

    sentiment = []

    # code created referencing https://huggingface.co/blog/sentiment-analysis-python
    for r in reviews:
        # sentiment analysis
        result = sentiment_model(r)[0]
        # negate score if sentiment was not positive
        sentiment.append(result["score"] if result["label"] == "POSITIVE" else -result["score"])

    average_score = sum(sentiment) / len(sentiment)

    label = "POSITIVE" if average_score > 0 else "NEGATIVE"

    return label, abs(average_score)

