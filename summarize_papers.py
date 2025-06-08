from google import genai
from google.genai import types
import pathlib
import json

MODELS = {
    "2.5_flash": "gemini-2.5-flash-preview-05-20",
    "test": "gemini-2.0-flash",
    "fast_test": "gemini-2.0-flash-lite",
}

with open('./gemini_api_key.json', 'r') as f:
    API_KEY = json.load(f)['key']

with open('./prompt.txt', 'r', encoding='utf-8') as f:
    PROMPT = f.read()


client = genai.Client(api_key=API_KEY)
filepath = pathlib.Path("papers/data.pdf")



response = client.models.generate_content(
    model=MODELS['fast_test'], 
    contents=[
        types.Part.from_bytes(
            data=filepath.read_bytes(),
            mime_type='application/pdf',
        ),
        PROMPT],
    config=types.GenerateContentConfig(
        # max_output_tokens=500,
        temperature=0.2,
    )
)

print(response.text)