from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import config
from services.llm import draft_email
from services.email_sender import send_email

config.validate()

app = FastAPI(title="Email Automation")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/draft", response_class=HTMLResponse)
async def create_draft(
    request: Request,
    essence: str = Form(...),
    recipient_email: str = Form(...),
    recipient_name: str = Form(""),
    sender_name: str = Form(""),
    subject_hint: str = Form(""),
):
    effective_sender = sender_name.strip() or config.SENDER_NAME
    try:
        draft = draft_email(
            essence=essence,
            recipient_name=recipient_name.strip(),
            sender_name=effective_sender,
            subject_hint=subject_hint.strip(),
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"LLM error: {e}",
                "essence": essence,
                "recipient_email": recipient_email,
            },
        )

    return templates.TemplateResponse(
        "draft.html",
        {
            "request": request,
            "subject": draft["subject"],
            "body": draft["body"],
            "recipient_email": recipient_email,
            "essence": essence,
        },
    )


@app.post("/send", response_class=HTMLResponse)
async def send(
    request: Request,
    recipient_email: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
):
    try:
        send_email(to_address=recipient_email, subject=subject, body=body)
        return templates.TemplateResponse(
            "draft.html",
            {
                "request": request,
                "subject": subject,
                "body": body,
                "recipient_email": recipient_email,
                "success": f"Email sent successfully to {recipient_email}!",
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "draft.html",
            {
                "request": request,
                "subject": subject,
                "body": body,
                "recipient_email": recipient_email,
                "error": f"Failed to send email: {e}",
            },
        )
