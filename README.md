# 🤔 Think First Bot

An educational chatbot that makes you **think before you get the answer**. Ask any question, and instead of answering right away, the bot first asks you **one short hint or question** to get you thinking. Once you reply (right, wrong, or "I don't know"), it gives you the **full, detailed answer**.

Built with **Flask** and **Google Gemini** (`gemini-2.5-flash`).

---

## Table of Contents

- [Why Think First?](#why-think-first)
- [How it works](#how-it-works)
- [Features](#features)
- [Tech stack](#tech-stack)
- [Project structure](#project-structure)
- [Getting started](#getting-started)
- [API endpoints](#api-endpoints)
- [Deployment on Render](#deployment-on-render)
- [Limitations](#limitations)
- [Future improvements](#future-improvements)
- [Author](#author)

---

## Why Think First?

Most AI chatbots hand over the answer immediately, which makes it easy to skip the thinking. Think First Bot adds a small "guessing game" step: one hint, one attempt from you, then the complete answer. The idea is that trying to recall or reason first helps you remember what you learn.

## How it works

1. **You ask a question** (for example, "What is photosynthesis?").
2. **The bot replies with one short hint or question** (1-2 sentences) instead of the answer.
3. **You reply** with your guess, or say "I don't know" or "give me the answer".
4. **The bot gives the full, detailed answer.** It never asks a second follow-up question, so there are no endless loops.

The bot keeps a friendly, encouraging, game-like tone throughout.

> **Example flow (illustrative)**
>
> **You:** What is photosynthesis?
> **Bot:** Quick thought first: what do you think plants need to make their own food?
> **You:** Sunlight and water?
> **Bot:** *(full explanation of photosynthesis)*

## Features

- One hint first, then the full answer, enforced through a system instruction
- Friendly and encouraging tone
- Simple web chat interface served by Flask
- API key loaded securely from an environment variable (never hard-coded)
- Ready for deployment on Render (reads the `PORT` environment variable)
- Clear JSON error responses (`400` for a missing message, `500` for a server error)

## Tech stack

| Area | Technology |
|---|---|
| Language | Python |
| Web framework | Flask |
| AI model | Google Gemini (`gemini-2.5-flash`) via `google-generativeai` |
| Frontend | HTML template (`templates/index.html`) |
| Hosting | Render (optional) |

## Project structure

> Adjust this to match your repository if file names differ.

```
Think-First-Bot/
├── app.py                # Flask server and Gemini chat logic
├── templates/
│   └── index.html        # Chat page
├── requirements.txt      # Python dependencies
└── README.md
```

## Getting started

### Prerequisites

- Python 3.9 or newer
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/imprashant005-dev/Think-First-Bot.git
cd Think-First-Bot
```

### 2. Create a virtual environment and install dependencies

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
# python3 -m venv venv
# source venv/bin/activate

pip install -r requirements.txt
```

The project's `requirements.txt` pins these versions:

```
Flask==3.0.3
google-generativeai==0.8.3
python-dotenv==1.0.1
gunicorn==23.0.0
```

(`gunicorn` is used for deployment, for example on Render.)

### 3. Set your API key

The app refuses to start without `GEMINI_API_KEY`.

```bash
# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# macOS / Linux
export GEMINI_API_KEY="your_api_key_here"
```

> Never commit your API key to GitHub.

**Optional: use a `.env` file.** `python-dotenv` is already in `requirements.txt`. To load the key from a `.env` file, create a file named `.env` containing `GEMINI_API_KEY=your_api_key_here`, add `.env` to your `.gitignore`, and put these two lines at the top of `app.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Run the app

```bash
python app.py
```

Open **http://localhost:5000** in your browser and start chatting.

## API endpoints

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Serves the chat page |
| `POST` | `/get_response` | Sends a message to the bot and returns its reply |

**Request**

```json
{ "message": "What is photosynthesis?" }
```

**Success response**

```json
{ "reply": "Quick thought first: what do you think plants need to make their own food?" }
```

**Error responses**

| Status | Meaning |
|---|---|
| `400` | No message was provided |
| `500` | Something went wrong on the server or with the Gemini API |

**Quick test with curl**

```bash
curl -X POST http://localhost:5000/get_response \
  -H "Content-Type: application/json" \
  -d '{"message": "What is gravity?"}'
```

## Deployment on Render

The app reads the `PORT` variable and listens on `0.0.0.0`, so it works on Render without changes.

1. Push the project to GitHub.
2. On [Render](https://render.com), create a new **Web Service** and connect your repository.
3. Set the **Build Command** to `pip install -r requirements.txt`.
4. Set the **Start Command** to `gunicorn app:app` (`gunicorn` is already in `requirements.txt`).
5. Under **Environment**, add `GEMINI_API_KEY` with your key.
6. Deploy.

## Limitations

- **One shared conversation:** the chat session is stored in server memory and shared by everyone using the app, so different users can interfere with each other's conversations. It also resets when the server restarts.
- **Behavior depends on the prompt:** the "one hint, then the full answer" rule is enforced through instructions to the model, so it may occasionally not follow them perfectly.
- No user accounts, rate limiting, or saved chat history.
- Requires an internet connection and a valid Gemini API key and quota.

## Future improvements

- Separate chat sessions for each user
- A "New chat" button to reset the conversation
- Choose the number of hints (for example, 1, 2 or 3)
- Subject modes such as math, science or coding
- Save chat history and show learning progress
- Stream responses for a faster feel

## Author

**Prashant** ([@imprashant005-dev](https://github.com/imprashant005-dev))

If you find this project useful, consider giving it a ⭐ on GitHub.
