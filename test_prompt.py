import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("prompts/final.txt") as f:
    prompt = f.read().format(
        topic="an AI app that writes hooks for short videos",
        audience="college students",
        length="30 seconds",
    )

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config=types.GenerateContentConfig(response_mime_type="application/json"),
)

result = json.loads(response.text)

with open("sample_output.json", "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(json.dumps(result, indent=2, ensure_ascii=False))
