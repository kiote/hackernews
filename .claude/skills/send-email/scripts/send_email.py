#!/usr/bin/env python3
"""
Send emails via Gmail with optional HTML, attachments, and scheduling.
"""
import argparse
import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv

# Look for .env in project root (4 levels up from this script)
env_path = Path(__file__).resolve().parents[4] / '.env'
load_dotenv(env_path)

# Setup logging
logging.basicConfig(filename='email.log', level=logging.INFO)


class EmailSender:
    def __init__(self):
        """Initialize email sender with Gmail SMTP configuration."""
        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 587
        self.from_email = os.getenv('GMAIL_ADDRESS')
        self.smtp_user = os.getenv('GMAIL_ADDRESS')
        self.smtp_password = os.getenv('GMAIL_APP_PASSWORD')

        if not self.from_email or not self.smtp_password:
            raise ValueError(
                "Missing Gmail credentials. Please set GMAIL_ADDRESS and "
                "GMAIL_APP_PASSWORD in your .env file"
            )

    def validate_email(self, email):
        """Validate email address format."""
        if '@' not in email or '.' not in email.split('@')[1]:
            raise ValueError(f"Invalid email address: {email}")
        return True

    def send_email(self, to_email, subject, body, is_html=False,
                   attachments=None, cc=None, bcc=None):
        """
        Send an email.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML (default: False)
            attachments: List of file paths to attach
            cc: List of CC email addresses
            bcc: List of BCC email addresses
        """
        try:
            # Validate email addresses
            self.validate_email(to_email)
            if cc:
                for email in cc:
                    self.validate_email(email)
            if bcc:
                for email in bcc:
                    self.validate_email(email)

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email

            if cc:
                msg['Cc'] = ', '.join(cc)

            # Add body
            content_type = 'html' if is_html else 'plain'
            msg.attach(MIMEText(body, content_type))

            # Add attachments
            if attachments:
                for filepath in attachments:
                    if not os.path.exists(filepath):
                        logging.warning(f"Attachment not found: {filepath}")
                        continue

                    with open(filepath, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(filepath)}'
                        )
                        msg.attach(part)

            # Send email
            recipients = [to_email] + (cc or []) + (bcc or [])

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_user and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)

                server.send_message(msg, from_addr=self.from_email, to_addrs=recipients)

            logging.info(f"Email sent to {to_email}: {subject}")
            print(f"SUCCESS: Email sent to {to_email}")
            return True

        except ValueError as e:
            logging.error(f"Validation error: {e}")
            print(f"ERROR: {e}")
            return False
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            print(f"ERROR: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Send emails')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', help='Email body text')
    parser.add_argument('--body-file', help='Read email body from file')
    parser.add_argument('--html', action='store_true', help='Body is HTML')
    parser.add_argument('--attachment', action='append', help='File to attach')
    parser.add_argument('--cc', action='append', help='CC email address')
    parser.add_argument('--bcc', action='append', help='BCC email address')

    args = parser.parse_args()

    # Get email body
    body = args.body
    if args.body_file:
        with open(args.body_file, 'r') as f:
            body = f.read()

    if not body:
        print("ERROR: Either --body or --body-file must be provided")
        return False

    sender = EmailSender()
    return sender.send_email(
        to_email=args.to,
        subject=args.subject,
        body=body,
        is_html=args.html,
        attachments=args.attachment,
        cc=args.cc,
        bcc=args.bcc
    )


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
