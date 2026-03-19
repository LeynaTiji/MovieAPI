import os
import json
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def AI_reccomendations(movies, mood, number):

    movie_list = "-".join([f"- {m.title} ({m.year}) | Genre: {m.genre} |" for m in movies])

    # Claude API prompt
    prompt = f"""You are a movie recommendation assistant. A user has is looking for a movie to watch based on their mood. 
    The mood the user has specified is - {mood}. Here are some movies from the database: {movie_list}.
    From this list, please recommend {number} suited to the users specified mood.
    For each movie recomendation, give an explanation, in 2-3 sentences, why it matches the mood specified.
    Respond in the exact JSON format provided with no extra text, no markdown, no code blocks, just raw JSON:
    {{
        "recommendations": [
            {{
            "movie_title": "Percy Jackson & the Olympians: The Lightning Theif",
            "year": 2010,
            "genre": "Family, Fantasy",
            "reason": "Why this matches the mood"
            }}
        ]
    }}
    """

    # code created with reference to https://platform.claude.com/docs/en/build-with-claude/structured-outputs
    #create response using claude and catch any response errors
    try:
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw_text = message.content[0].text

        # strip markdown code blocks that may be added to prevent any errors in formatting
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]

        ai_response = json.loads(raw_text.strip())
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="AI returned an unexpected response format. Please try again."
        )
    except anthropic.APIError as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI service unavailable: {str(e)}"
        )
    
    return ai_response["recommendations"]
