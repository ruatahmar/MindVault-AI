
from app.config import settings 
from google import genai

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def get_summary(note: str):
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash", 
        contents=[note,"Give me a Smart Summarization of this text, no matter how long or short and dont add no fluff just straight give the summary and dont say anything else"]
    )
    full_text = ""
    for chunk in response:
        if chunk.candidates and chunk.candidates[0].content.parts:
            full_text += chunk.candidates[0].content.parts[0].text
    
    return full_text

def get_tags(note: str):
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash", 
        contents=[note,"Give 5 some tag Suggestions based on content. just give the tags and say nothing else"]
    )
    for chunk in response:
        print(chunk.text, end="")

  