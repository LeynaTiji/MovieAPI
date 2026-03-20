import os
import requests

API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

# code created referencing https://huggingface.co/blog/sentiment-analysis-python

def review_semantics(reviews: list[str]):

    sentiment = []

    for r in reviews:
        # sentiment analysis
        response = requests.post(API_URL, headers=headers, json={"inputs": r})
        
        if response.status_code != 200:
            continue

        result = response.json()
        # hf returns [[{label, score}, {label, score}]]
        if isinstance(result, list) and len(result) > 0:
            scores = result[0] if isinstance(result[0], list) else result
            best = max(scores, key=lambda x: x["score"])
            # negate score if negative to match original behaviour
            sentiment.append(best["score"] if best["label"] == "POSITIVE" else -best["score"])
    
    if not sentiment:
        return "UNKNOWN", 0.0

    average_score = sum(sentiment) / len(sentiment)

    label = "POSITIVE" if average_score > 0 else "NEGATIVE"

    return label, abs(average_score)

