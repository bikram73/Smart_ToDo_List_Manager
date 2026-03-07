import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email_reminder(to_email, task_name):
    # Credentials from your request (Defaults used if env vars not set)
    # Note: We assume gmail.com based on the PRD context, as mail.com requires different SMTP settings.
    sender_email = os.getenv("EMAIL_USER", "todoapp.notificationss@gmail.com")
    password = os.getenv("EMAIL_PASS", "*todoapp.notificationss*")

    # SMTP Server Settings for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 465

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = f"Reminder: {task_name} is due!"

    body = f"""
    <html>
      <body>
        <h2>Task Reminder</h2>
        <p>Hello,</p>
        <p>Your task <strong>{task_name}</strong> was scheduled to be finished by now.</p>
        <p>Please visit your dashboard to mark it as complete or reschedule it.</p>
        <br>
        <p>Best regards,<br>Smart To-Do App</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")