from transformers import pipeline

# code created referencing https://huggingface.co/docs/transformers/main_classes/pipelines
# and https://huggingface.co/facebook/bart-large-cnn

# load bart model
summeriser = pipeline("summarization", model="facebook/bart-large-cnn")
sentiment_model = pipeline("sentiment-analysis")

def summerise_reviews(reviews: list[str]):

    joint_review = " ".join(reviews)

    # summary text of all reviews using model
    summary = summeriser(joint_review, max_length=200, min_length=50, do_sample=False)[0]["summary_text"]

    return summary
