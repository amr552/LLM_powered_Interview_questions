# Study Mode Interview Trainer (Web App)

A lightweight study web application that helps learners prepare for interviews by generating structured practice questions with hints and on-demand answers.

The interface is designed for “active recall” learning: users try to answer first using a hint, then reveal the answer only when needed. This improves retention and mimics real interview thinking.

---

## Key Features

- **Role-based practice:** Choose a target role (e.g., Data Analyst, Backend Developer).
- **Level selection:** Intern / Junior / Mid-level / Senior.
- **Topic focus:** Generate questions for a specific skill area (e.g., SQL, System Design, Machine Learning).
- **Language support:** English and Arabic.
- **Study Mode UX:**
  - Each question is shown with a short hint.
  - The answer is hidden by default and can be revealed using a **toggle** (“Show answer”).
- **Concise answers:** Short, practical model answers (ideal for revision).
- **Production-friendly handling:** User-friendly messages for common runtime errors (network, configuration, etc.).

---

## How to Use (User Flow)

1. Enter the **Role** you are preparing for.
2. Select your **Level** (Intern → Senior).
3. Enter a **Topic** you want to practice.
4. Choose the **Language**.
5. Select the **Number of Questions**.
6. Click **Generate Study Set**.
7. Read the hint and attempt the answer.
8. Click **Show answer** only when you need to verify your response.

---

## Why This Project Matters (For HR)

This repository demonstrates:
- Practical web app development with a clean, interactive interface
- Learning-focused UX design (active recall + progressive disclosure)
- Structured content formatting and post-processing (converting raw output into a toggle-based study experience)
- Defensive programming and reliable user feedback for errors
- Rapid prototyping and product thinking for educational tools

---

## Local Setup

### 1) Install dependencies

pip install -r requirements.txt

## Tech Stack

- Python
- Gradio (UI)

---

<img width="1585" height="894" alt="image" src="https://github.com/user-attachments/assets/48f16806-9654-4e3b-bfab-53f86898cf57" />
<img width="1564" height="796" alt="image" src="https://github.com/user-attachments/assets/4a78c886-9fe0-4c25-944b-809882039744" />
<img width="1578" height="793" alt="image" src="https://github.com/user-attachments/assets/f7f63747-fdfa-43eb-91d4-440428910c26" />
<img width="1557" height="879" alt="image" src="https://github.com/user-attachments/assets/7b7fb459-ac05-403f-8bb1-a7d40a319c96" />




