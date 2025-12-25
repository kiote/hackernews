---
name: sending-emails
description: Send emails with HTML templates, attachments, and scheduling. Use when the user needs to send emails, create email campaigns, or automate email workflows.
---

# Sending Emails

## Critical: Virtual Environment Required

**ALWAYS activate the virtual environment before running the email script:**

```bash
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py [options]
```

This is required because the script depends on `python-dotenv` which is installed in the venv.

---

## Quick start

Send a simple email using the Python script:

```bash
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py --to recipient@example.com --subject "Hello" --body "Your message here"
```

## HTML emails

Send an HTML email:

```bash
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py --to recipient@example.com --subject "Hello" --body-file email.html --html
```

## With attachments

Send email with attachments:

```bash
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py --to recipient@example.com --subject "Report" --body "See attached" --attachment report.pdf
```

## Multiple recipients

Send to multiple recipients with CC and BCC:

```bash
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py --to user@example.com --cc manager@example.com --bcc archive@example.com --subject "Update" --body "Message"
```

## Configuration

This skill uses Gmail SMTP. Create a `.env` file in the project root with your credentials:

```bash
cp .env.example .env
```

Required environment variables:

- `GMAIL_ADDRESS` - Your Gmail email address
- `GMAIL_APP_PASSWORD` - Gmail App Password (NOT your regular password)

### Getting a Gmail App Password

1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" as the app
4. Click "Generate" and copy the 16-character password
5. Add it to your `.env` file

**Note:** Requires `python-dotenv` package: `pip install python-dotenv`

## Using templates

Create HTML templates in the `templates/` directory and reference them:

```bash
source .venv/bin/activate && python .claude/skills/send-email/scripts/send_email.py --to user@example.com --subject "Welcome" --body-file .claude/skills/send-email/templates/welcome.html --html
```
