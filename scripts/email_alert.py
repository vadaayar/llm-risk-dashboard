import smtplib
from email.mime.text import MIMEText

def send_email(subject, message, receiver_email):
    sender_email = "your-email@gmail.com"
    sender_password = "your-app-password"

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
