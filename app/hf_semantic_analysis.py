from transformers import pipeline

# code created referencing https://huggingface.co/blog/sentiment-analysis-python

# load bart model

sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

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

