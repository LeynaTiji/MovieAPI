from transformers import pipeline

# code created referencing https://huggingface.co/blog/sentiment-analysis-python

# load bart model
summeriser = pipeline("text-generation", model="gpt2")
sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def review_semantics(reviews: list[str]):

    #join all reviews together
    joint_review = " ".join(reviews)

    # code created referencing https://huggingface.co/blog/sentiment-analysis-python
    # sentiment analysis
    sentiment = sentiment_model(joint_review)[0]
    label = sentiment["label"]
    score = sentiment["score"]

    return label, score

