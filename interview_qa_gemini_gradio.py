import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, AuthenticationError, APIConnectionError, BadRequestError

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY. Put it in your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an expert interviewer and tutor.

Create a study set of interview questions.
Rules:
- Keep it concise.
- For each question provide: Question, Hint (1 line), Answer (short, 2–5 bullets or 2–4 lines).
- Return as plain text using this exact template repeatedly:

Q1: ...
H1: ...
A1: ...
Q2: ...
H2: ...
A2: ...
"""

def build_prompt(role: str, level: str, topic: str, num_questions: int, language: str) -> str:
    return f"""
Role: {role}
Level: {level}
Topic: {topic}
Number of questions: {num_questions}
Language: {language}

Generate the study set now. Keep answers short and practical.
"""

def to_toggle_markdown(text: str) -> str:
    """
    Convert:
      Q1/H1/A1 blocks
    into:
      Question + hint visible
      Answer hidden under <details> toggle
    """
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    blocks = []
    q, h, a = None, None, []

    def flush():
        nonlocal q, h, a, blocks
        if q:
            hint = h if h else "Hint: (not provided)"
            answer = "\n".join(a).strip() if a else "(No answer provided)"
            blocks.append(
                f"### {q}\n"
                f"**{hint}**\n\n"
                f"<details>\n<summary><b>Show answer</b></summary>\n\n{answer}\n\n</details>\n"
            )
        q, h, a = None, None, []

    for line in lines:
        if line.startswith("Q") and ":" in line:
            flush()
            q = line
        elif line.startswith("H") and ":" in line:
            h = line.replace("H", "Hint", 1)
        elif line.startswith("A") and ":" in line:
            a.append(line.replace("A", "Answer", 1))
        else:
            # continuation of answer (bullets/lines)
            if q:
                a.append(line)

    flush()
    return "\n\n---\n\n".join(blocks) if blocks else text

def generate_study_set(role, level, topic, num_questions, language):
    role = (role or "").strip()
    topic = (topic or "").strip()

    if not role or not topic:
        return "Please enter both Role and Topic."

    prompt = build_prompt(role, level, topic, int(num_questions), language)

    try:
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.4,
            max_tokens=650,  # cost control
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        raw = (resp.choices[0].message.content or "").strip()
        return to_toggle_markdown(raw)

    except RateLimitError:
        return "API quota exceeded (429). Check billing/quota."
    except AuthenticationError:
        return "Invalid API key. Check OPENAI_API_KEY."
    except APIConnectionError:
        return "Network error. Try again."
    except BadRequestError as e:
        return f"Request error: {e}"

with gr.Blocks(title="Study Mode Interview Trainer") as demo:
    gr.Markdown("# Study Mode Interview Trainer")
    gr.Markdown("Generate questions + hints, then click **Show answer** to reveal the answer.")

    with gr.Row():
        role = gr.Textbox(label="Role / Position", placeholder="e.g., Data Analyst, Backend Developer")
        level = gr.Dropdown(["Intern", "Junior", "Mid-level", "Senior"], value="Junior", label="Level")

    with gr.Row():
        topic = gr.Textbox(label="Topic / Focus", placeholder="e.g., SQL, Machine Learning, System Design")
        language = gr.Dropdown(["English", "Arabic"], value="English", label="Language")

    num_questions = gr.Slider(3, 20, value=6, step=1, label="Number of Questions")

    btn = gr.Button("Generate Study Set", variant="primary")
    output = gr.Markdown()

    btn.click(generate_study_set, inputs=[role, level, topic, num_questions, language], outputs=output)

if __name__ == "__main__":
    demo.launch(server_port=7860)
