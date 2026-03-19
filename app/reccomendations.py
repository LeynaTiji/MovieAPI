import anthropic

def AI_reccomendations(movies, mood, number):

    movie_list = "-".join([f"- {m.movie_title} ({m.year}) | Genre: {m.genre} |" for m in movies])

    # Claude API prompt

    prompt = f"""You are a movie recommendation assistant. A user has is looking for a movie to watch based on their mood. 
    The mood the user has specified is - {mood}. Here are some movies from the database: {movie_list}.
    From this list, please recommend {number} suited to the users specified mood.
    For each movie reccomendation, give an explanation, in 2-3 sentences, why it matches the mood specified.
    Respond in the exact JSON format provided.
    {{
        "recommendations": [
            {{
            "title": "Movie Title",
            "year": 1999,
            "genre": "Genre",
            "reason": "Why this matches the mood"
            }} 
    }}
    """
