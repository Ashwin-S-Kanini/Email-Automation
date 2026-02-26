# Email Automation Agent

A local web app that lets you write professional emails effortlessly — just describe what you want to say in plain words, and the AI drafts a formal email for you. Review and edit the draft, then send it directly from your browser via Gmail.

Powered by **Groq AI** (Llama 3.3 70B, free tier) for drafting and **Gmail SMTP** for sending — no paid services required.

---

## What It Does

1. You describe the email in plain language (e.g. *"ask my professor for a one-week deadline extension"*)
2. The AI generates a polished, formal email with a subject line
3. You review and edit the draft in a preview page
4. Click **Send** — the email is delivered via your Gmail account

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| LLM | Groq API (free tier) | Fast, free, no local GPU — Llama 3.3 70B |
| Backend | FastAPI (Python) | Modern, async, lightweight |
| Templates | Jinja2 | Server-side HTML rendering, built into FastAPI |
| Email | smtplib + Gmail SMTP | No extra deps, reliable, 500 emails/day free |
| Config | python-dotenv | Env-based secrets |

---

## Project Structure

```
Email Automation/
├── main.py                  # FastAPI app + routes (GET /, POST /draft, POST /send)
├── config.py                # Settings loaded from .env
├── services/
│   ├── llm.py               # Groq API — prompt engineering + email drafting
│   └── email_sender.py      # Gmail SMTP send logic with STARTTLS
├── templates/
│   ├── base.html            # Base layout
│   ├── index.html           # Input form (essence + recipient)
│   └── draft.html           # Preview/edit draft + send button
├── static/
│   └── style.css            # Minimal clean styling
├── .env.example             # Template for secrets
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone & install dependencies
```bash
git clone https://github.com/Ashwin-S-Kanini/Email-Automation.git
cd Email-Automation
pip install -r requirements.txt
```

### 2. Configure secrets
```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Get free at [console.groq.com](https://console.groq.com) |
| `GMAIL_USER` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | 16-char App Password (see below) |
| `SENDER_NAME` | Your name for email sign-offs |

### 3. Gmail App Password (one-time setup)
1. Enable **2-Step Verification** on your Google Account
2. Go to **Google Account → Security → App Passwords**
3. Generate a password for "Mail" → copy the 16-character code → paste as `GMAIL_APP_PASSWORD`

> Regular Gmail passwords won't work — you must use an App Password.

### 4. Run
```bash
uvicorn main:app --reload
```
Open [http://localhost:8000](http://localhost:8000)

---

## User Flow

1. Open `http://localhost:8000`
2. Fill in the form:
   - **Email Essence** — what you want to say, in plain words
   - **Recipient Email** — who to send it to
   - **Recipient Name** *(optional)* — personalises the salutation
   - **Your Name** *(optional)* — for the sign-off; defaults to `SENDER_NAME` in `.env`
   - **Subject Hint** *(optional)* — or let the AI generate one
3. Click **Draft Email** → Groq generates a formal email
4. Review / edit the subject and body in the preview page
5. Click **Send** → delivered via Gmail SMTP
6. Success or error confirmation is shown on screen

---

## Notes

- Groq free tier: **14,400 requests/day** — more than enough for personal use
- Model: `llama-3.3-70b-versatile` (best quality on the free tier)
- SMTP: Gmail via `smtp.gmail.com:587` with STARTTLS
- The draft preview step is intentional — always review before sending
