import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import errors, types

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MAIN_MODEL = "gemini-3.8-flash"
BACKUP_MODEL = "gemini-3.5-flash"

with open("prompts/final.txt") as f:
    PROMPT = f.read()


def ask_gemini(model, prompt):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(response.text)


def generate_with_retries(prompt):
    # Try the main model 3 times, then the backup model once
    for model in [MAIN_MODEL] * 3 + [BACKUP_MODEL]:
        try:
            return ask_gemini(model, prompt)
        except errors.APIError as e:
            # 503 = model busy, 429 = out of quota
            if e.code not in (429, 503):
                raise
            print(f"{model} failed ({e.code})")
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()
    audience = data.get("audience", "").strip()
    length = data.get("length", "").strip()

    if not topic or not audience or not length:
        return jsonify({"error": "Please fill in topic, audience, and length."}), 400

    prompt = PROMPT.format(topic=topic, audience=audience, length=length)

    try:
        result = generate_with_retries(prompt)
    except json.JSONDecodeError:
        return jsonify({"error": "Gemini sent back a response we couldn't read. Please try again."}), 502
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Something went wrong talking to Gemini. Please try again."}), 500

    if result is None:
        return jsonify({"error": "Gemini is really busy right now. Please try again in a minute."}), 503

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
