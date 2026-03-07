import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email_reminder(to_email, task_name, user_name):
    # Credentials from your request.
    sender_email = os.getenv("EMAIL_USER", "todoapp.notificationss@gmail.com")
    password = os.getenv("EMAIL_PASS", "gustytlkeegwetdf")

    # SMTP server settings must match the email provider.
    if sender_email.endswith("@mail.com"):
        # Settings for mail.com
        smtp_server = "smtp.mail.com"
        smtp_port = 465 # Port for SSL
    elif sender_email.endswith("@gmail.com"):
        # Settings for Gmail
        # IMPORTANT: Gmail requires an "App Password", not your regular account password.
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
    else:
        print(f"ERROR: Unsupported email provider in email_service.py for {sender_email}")
        return

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = f"Reminder: from the Smart To-Do List App - The {task_name} is due!"

    body = f"""
    <html>
      <body>
        <h2>Task Reminder</h2>
        <p>Hello, {user_name}</p>
        <p>Your task <strong>{task_name}</strong> was scheduled to be finished by now.</p>
        <p>Your task was not completed.</p>
        <p>Please choose:</p>
        <p>1. Mark as completed<br>
        2. Reschedule<br>
        3. Delete task</p>
        <br>
        <p>Best regards,<br>Smart To-Do List App</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"✅ Email sent to {to_email}")
    except smtplib.SMTPAuthenticationError as e:
        if "mail.com" in sender_email:
            print(f"❌ SMTP Error: {e}.\n👉 For mail.com, you MUST enable 'POP3/IMAP' in your account settings under 'Email' > 'POP3/IMAP'.")
        else:
            print(f"❌ SMTP Authentication Error: {e}. Please double-check your EMAIL_USER and EMAIL_PASS. If using Gmail, you must use an 'App Password'.")
    except Exception as e:
        print(f"❌ An unexpected error occurred while sending email: {e}")