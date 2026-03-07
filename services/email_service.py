import smtplib
from email.mime.text import MIMEText
import os

# Configuration
# Note: For Gmail, use smtp.gmail.com. If using mail.com, use smtp.mail.com.
# Defaulting to Gmail as per PRD context, but using provided credentials.
EMAIL_USER = os.getenv("EMAIL_USER", "todoapp.notificationss@mail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS", "*todoapp.notificationss*")

# Auto-configure SMTP based on email domain if not explicitly set
default_smtp = "smtp.gmail.com"
if "@mail.com" in EMAIL_USER:
    default_smtp = "smtp.mail.com"

SMTP_SERVER = os.getenv("SMTP_SERVER", default_smtp) 
SMTP_PORT = 465

def send_email_reminder(to_email: str, task_title: str):
    subject = "Task Reminder: Incomplete Task"
    body = f"""
Hello,

Your task "{task_title}" was not completed before the scheduled time.

Please choose one option:
1. Mark task as completed
2. Reschedule task time
3. Delete the task if no longer needed

Login to your dashboard to update the task.

Thank you.
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
