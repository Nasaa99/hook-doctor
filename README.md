# Hook Doctor

A simple AI web app that writes scroll-stopping hooks and short scripts for short-form videos (TikTok, Reels, Shorts). Built with Python, Flask, and the Gemini API for CS4680 Prompt Engineering.

## The Problem

On short-form video, most viewers decide in the first 3 seconds whether to keep watching. Students and new creators often have good ideas but weak openings like "Hey guys, today I'm going to talk about...", so people scroll away.

Hook Doctor takes a **topic**, an **audience**, and a **video length** and returns:
- 3 hooks for the first 3 seconds, each with a score (1-10) and why it works
- A timestamped script that starts with the best hook, with voiceover and on-screen text for each beat
- A caption with hashtags

## How to Run

**1. Get a Gemini API key**

Go to [Google AI Studio](https://aistudio.google.com/apikey), sign in with a Google account, and click **Create API key**.

**2. Set up the project**

Requires Python 3.9 or newer.

```bash
git clone https://github.com/Nasaa99/hook-doctor.git
cd hook-doctor
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Create the `.env` file**

Create a file named `.env` in the project folder with your key:

```
GEMINI_API_KEY=your-key-here
```

`.env` is in `.gitignore`, so your key is never committed.

**4. Start the app**

```bash
python app.py
```

Open http://localhost:5001 in your browser. Generating can take up to a minute.

## Prompt Engineering

All prompts are in the `prompts/` folder. The app uses `final.txt`.

### How the prompt evolved

**v1 - First draft** ([v1.txt](prompts/v1.txt))
A short prompt that sets up a persona and asks for 3 hooks and a script. It had no rules for what makes a good hook and no output format, so nothing stopped generic answers and the app had no reliable way to display them.

**v2 - More specific** ([v2.txt](prompts/v2.txt))
Added clear rules:
- Hooks must be under 15 words and use 3 different styles (bold claim, question, curiosity gap).
- Hooks must be specific to the topic and audience. Generic lines like "You won't believe this!" are banned.
- The script must fit the video length and end with a call to action.
- A fixed text format for the output.

**Final - JSON output** ([final.txt](prompts/final.txt))
- **JSON only, always the same structure:** `hooks` (text, score, why), `script` (time, voiceover, on_screen_text), and `caption`, so the frontend can parse and display it. The app also turns on Gemini's JSON mode as a backup.
- **Hook scores:** the model scores each hook, and the script starts with the highest-scoring one.
- **Few-shot examples:** two weak hooks, each with a better version.
- **No-invented-stats fix:** while testing, the model made up results like "get you 10k views before your 9 AM class" and "my first-three-second retention literally doubled". Those claims are misleading in a real video. I added a rule: *"Don't invent stats, view counts, or results anywhere."* The first few-shot example used "$3,000", which went against the new rule, so I replaced it with an example that has no numbers. After the fix, hooks used relatable problems and curiosity instead of fake numbers.

### Before/after: v1 vs. final

Both prompts were run on the same inputs: topic *"an AI app that writes hooks for short videos"*, audience *"college students"*, length *"30 seconds"*. Full outputs: [v1_output.txt](prompts/v1_output.txt) and [final_output.json](prompts/final_output.json).

| | v1 | final |
| --- | --- | --- |
| Format | Long markdown with headings, a table, and extra "strategist tips" nobody asked for | JSON with the same fields every time |
| Made-up stats | Many: "die at 200 views", "+50k views", "70% of viewers watch without sound", "psychologically proven hooks" | None |
| Hook scores | No | Yes, 1-10 with a reason for each |
| Caption | No | Yes, with hashtags |
| Usable by the app | No, it would need messy text parsing | Yes, the page reads the JSON directly |

Example hook, before and after:
- **v1:** *"Stop spending two hours editing a TikTok just for it to die at 200 views."*
- **final:** *"There's a reason nobody watches your campus videos, and it's not your content."*

Both hooks are strong, but v1's depends on a made-up number, while final's gets its curiosity from a relatable problem.

### Patterns used

- **Persona:** the prompt starts with *"Act as a viral short-form video strategist..."* so the model answers with an expert's knowledge and tone instead of generic writing advice.
- **Template:** the prompt is a reusable template with `{topic}`, `{audience}`, and `{length}` placeholders that the app fills in. The output also follows a fixed template (the JSON structure), so every response has the same fields.
- **Few-Shot:** two examples each show a weak hook next to a better one, with an explanation. One turns *"Here are some tips for saving money."* into *"You're probably still paying for a subscription you forgot you have."* The other turns *"Today I'm going to talk about how to study."* into *"If you study by rereading your notes, you're doing it wrong."* This shows the model what "good" looks like better than describing it.
- **Iterative Refinement:** the prompt was improved in rounds by testing it and fixing what went wrong (see [How the prompt evolved](#how-the-prompt-evolved)). v1 → v2 added rules for specific hooks and a fixed format, v2 → final switched to JSON and added scores and few-shot examples, and testing final led to the no-invented-stats fix.

## Project Files

```
app.py              Flask server (/ and /api/generate)
requirements.txt    Python packages to install
prompts/            v1.txt, v2.txt, final.txt, plus v1_output.txt and final_output.json
templates/          index.html
static/             style.css, script.js
test_prompt.py      Tests final.txt without the server, saves sample_output.json
sample_output.json  Example output from Gemini
```
