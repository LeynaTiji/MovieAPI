from textblob import TextBlob

def review_semantics(reviews: list[str]):

    sentiment = []

    for r in reviews:
        # sentiment analysis
        blob = TextBlob(r)
        # polarity is between -1 and 1
        sentiment.append(blob.sentiment.polarity)
    
    if not sentiment:
        return "UNKNOWN", 0.0

    average_score = sum(sentiment) / len(sentiment)

    label = "POSITIVE" if average_score > 0 else "NEGATIVE"

    return label, round(average_score, 2)

