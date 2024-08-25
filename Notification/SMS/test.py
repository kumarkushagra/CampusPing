import smtplib
from email.mime.text import MIMEText

def send_sms_via_email(phone_number, carrier_gateway, message):
    # Email and SMTP server configuration
    sender_email = "trainingtesting0001@gmail.com"
    app_password = "hinh rrnh lwtp oppl"  # Replace with your app password
    smtp_server = "smtp.gmail.com"  # Gmail SMTP server
    smtp_port = 587  # TLS port

    # Construct the message
    to_email = f"{phone_number}{carrier_gateway}"  # Correct format without double '@'
    msg = MIMEText(message)
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = ""  # SMS typically does not use the subject

    # Send the email via SMTP
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        print("SMS sent successfully!")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

# Usage example
phone_number = "8595509207"  # Ensure the phone number is correct
carrier_gateway = "@airtelap.com"  # Ensure to use the correct gateway from your list
message = "Hello! This is a random message sent via email to SMS using Python."

send_sms_via_email("8595509207", "@airtelap.com", "Test")
