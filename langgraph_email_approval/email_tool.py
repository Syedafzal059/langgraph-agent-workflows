import smtplib
from email.message import EmailMessage
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = "syedafzal059@gmail.com"#os.getenv("GMAIL_USER")
EMAIL_PASSWORD = "dvmu piya dhdl btbo"#os.getenv("GMAIL_PASS")

@tool
def send_approval_email(to: str, subject: str, body: str) -> str:
    """Send approval email via Gmail SMTP."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "syedafzal051@gmail.com"
    msg.set_content(body)
    print(f"msg = {msg} email = {EMAIL_ADDRESS} and password = {EMAIL_PASSWORD} " , flush = True)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Mail sent", flush=True)
        return "✅ Email sent successfully."
    except Exception as e:
        print("Mail sent failed", flush=True)
        return f"❌ Failed to send email: {str(e)}"



if __name__=="__main__":
    from email_tool import send_approval_email

    response = send_approval_email({
        "to": "syedafzal051@gmail.com",
        "subject": "Test",
        "body": "This is a test email"
    })

    print(response)
