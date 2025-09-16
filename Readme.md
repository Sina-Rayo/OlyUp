# OlyUp

A **Django-based application** for automated grading of long-form, step-by-step exam answers.  
It supports **stepwise evaluation**, **context-aware corrections**, and provides **structured feedback** with scores.

---

## Features

- **Step-by-Step Evaluation:** Each part of the answer is evaluated in sequence, considering the previous sections.  
- **Context-Aware Correction:** Ensures that each step is consistent with prior steps.  
- **Structured JSON Output:** Each step returns a JSON with `is_valid`, `confidence_score`, `explanation`, and `feedback`.  
- **Overall Scoring:** Aggregates all step evaluations into a final score and detailed feedback.  
- **Database Integration:** Each step is saved in the database as it’s graded for persistence and further analysis.  
- **Token/API Ready:** Can be connected to a language model API (e.g., OpenAI GPT) for evaluation.

---

## Tech Stack

- Django & Django REST Framework (DRF)  
- SQLite (or any Django-supported DB)  
- Python 3.10+  
- OpenAI API and Prompt Engeneering

---

## API Endpoints

| Method | Endpoint          | Description                      | Authorization                 |
| ------ | ----------------- | -------------------------------- | ------------------------------|
| POST   | /signup           | Sign up                          | No need                       |
| POST   | /login            | Log in                           | No need                       |
| POST   | /correct          | Corrects a solution              | Token Auth                    |

---

### Request Bodies

**Sign Up & Log In**
```json
{
  "username": "user",
  "password": "pass"
}
```

**Correct**
```json
{
  "question": string,
  "steps": ["step1" , "step2" , ...]
}
```

## Installation & Setup


### 1. Clone the repository
```bash
git clone https://github.com/Sina-Rayo/OlyUp/
cd OlyUp
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Run the server
```bash
python manage.py runserver
```

