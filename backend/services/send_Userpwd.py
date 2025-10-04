import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_password_email(to_email, name, password):
    sender_email = "your_email@gmail.com"   # replace with your email
    sender_password = "your_app_password"   # use app password if using Gmail

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = "Your Account Details"

    body = f"""
    Hi {name},

    Your account has been created.

    Login Details:
    Email: {to_email}
    Password: {password}

    Please change your password after first login.
    """
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
