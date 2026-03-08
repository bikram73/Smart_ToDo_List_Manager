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
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Task Reminder</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #e2e8f0;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0f172a; padding: 40px 0;">
            <tr>
                <td align="center">
                    <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #1e293b; border-radius: 12px; border: 1px solid #334155; box-shadow: 0 0 20px rgba(59, 130, 246, 0.15); overflow: hidden;">
                        <!-- Header -->
                        <tr>
                            <td style="background-color: #111827; padding: 30px; text-align: center; border-bottom: 1px solid #334155;">
                                <h2 style="margin: 0; color: #3b82f6; font-size: 24px; text-transform: uppercase; letter-spacing: 1px; text-shadow: 0 0 10px rgba(59, 130, 246, 0.4);">Smart To-Do</h2>
                            </td>
                        </tr>
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #e2e8f0;">Hello <strong style="color: #fff;">{user_name}</strong>,</p>
                                
                                <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 1.6; color: #e2e8f0;">
                                    This is a friendly reminder that your task <strong style="color: #60a5fa;">"{task_name}"</strong> was scheduled to be finished by now.
                                </p>

                                <div style="background-color: #111827; border-left: 4px solid #ef4444; padding: 15px; margin: 25px 0; border-radius: 4px;">
                                    <p style="margin: 0; color: #e2e8f0; font-size: 15px;"><strong>Status:</strong> Overdue / Incomplete</p>
                                </div>

                                <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.6; color: #e2e8f0;">Please visit your dashboard to take action:</p>
                                
                                <ul style="list-style: none; padding: 0; margin: 0 0 30px 0;">
                                    <li style="margin-bottom: 10px; padding-left: 20px; position: relative; color: #94a3b8;">
                                        <span style="color: #4ade80; position: absolute; left: 0;">✔</span> Mark as completed
                                    </li>
                                    <li style="margin-bottom: 10px; padding-left: 20px; position: relative; color: #94a3b8;">
                                        <span style="color: #f59e0b; position: absolute; left: 0;">📅</span> Reschedule
                                    </li>
                                    <li style="margin-bottom: 10px; padding-left: 20px; position: relative; color: #94a3b8;">
                                        <span style="color: #ef4444; position: absolute; left: 0;">🗑️</span> Delete task
                                    </li>
                                </ul>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #0f172a; padding: 20px; text-align: center; border-top: 1px solid #334155;">
                                <p style="margin: 0; font-size: 12px; color: #94a3b8;">Best regards,<br>Smart To-Do List App</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
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