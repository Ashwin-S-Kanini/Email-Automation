from groq import Groq
import config

_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=config.GROQ_API_KEY)
    return _client


def draft_email(
    essence: str,
    recipient_name: str,
    sender_name: str,
    subject_hint: str,
) -> dict[str, str]:
    """Return {'subject': ..., 'body': ...} drafted by the LLM."""
    salutation = f"Dear {recipient_name}," if recipient_name else "Dear Sir/Madam,"
    subject_instruction = (
        f'Use this subject hint: "{subject_hint}"'
        if subject_hint
        else "Generate an appropriate subject line."
    )

    prompt = f"""You are an expert professional email writer.
Draft a formal, polite, and concise email based on the following essence.

Essence: {essence}
Salutation to use: {salutation}
Sender name (sign-off): {sender_name}
Subject instruction: {subject_instruction}

Output format (strictly follow this, no extra text):
SUBJECT: <subject line>
BODY:
<full email body starting with the salutation, ending with sign-off>"""

    response = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()

    # Parse SUBJECT and BODY from LLM output
    subject = ""
    body = ""
    if "SUBJECT:" in raw and "BODY:" in raw:
        parts = raw.split("BODY:", 1)
        subject_line = parts[0].replace("SUBJECT:", "").strip()
        subject = subject_line
        body = parts[1].strip()
    else:
        # Fallback: treat entire response as body
        subject = subject_hint or "Email"
        body = raw

    return {"subject": subject, "body": body}
