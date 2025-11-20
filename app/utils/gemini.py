
from app.config import settings 
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_summary(note: str):
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash", 
        contents=[note,"Give me a Smart Summarization of this long note"]
    )
    for chunk in response:
        print(chunk.text, end="")

def get_tags(note: str):
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash", 
        contents=[note,"Give 5 some tag Suggestions based on content. just give the tags and say nothing else"]
    )
    for chunk in response:
        print(chunk.text, end="")

  