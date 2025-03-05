import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = str(os.getenv('SMTP_SERVER'))
SMTP_PORT = int(os.getenv('SMTP_PORT', 587)) 
SENDER_EMAIL = str(os.getenv('SENDER_EMAIL'))
SENDER_PASSWORD = str(os.getenv('SENDER_PASSWORD'))
RECIPIENT_EMAIL = str(os.getenv('RECIPIENT_EMAIL'))

print(f"SMTP_SERVER: {SMTP_SERVER}")
print(f"SMTP_PORT: {SMTP_PORT}")
print(f"SENDER_EMAIL: {SENDER_EMAIL}")
print(f"SENDER_PASSWORD: {'*' * len(SENDER_PASSWORD) if SENDER_PASSWORD else None}")
print(f"RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")

def send_email(consumer_message):

    
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()  
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, "Your CV just got viewed "+ consumer_message)
    print("Email sent successfully!")


