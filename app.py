import os
import json
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64

# -------------------------------
# Load Contacts
# -------------------------------
def get_recipient_entity(user_input):
    with open('contacts.json') as f:
        contacts = json.load(f)

    for name in contacts:
        if name.lower() in user_input.lower():
            return name, contacts[name]

    return None, None

# -------------------------------
# Generate Email with Mistral
# -------------------------------
def generate_email(subject, user_intent, recipient_role):
    # Load profile data
    with open('user_profile.json') as f:
        profile = json.load(f)

    your_name = profile['name']
    enrollment = profile.get('enrollment', '')
    prof_last_name = profile['professors'].get(recipient_role, {}).get("last_name", "")

    prompt = f"""
Write a polite professional email.
Subject: {subject}

Context: {user_intent}

Personalize this email with:
- Name: {your_name}
- Enrollment: {enrollment}
- Professor Last Name: {prof_last_name}
- Assume Date = 10 June 2025
- Submission Deadline = 14 June 2025

Use a formal tone and end with greetings and gratitude.
"""
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    return response.json()['response']


# -------------------------------
# Gmail Auth + Send
# -------------------------------
def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_email(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject

    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    print(f"📨 Email sent! Message ID: {send_message['id']}")

# -------------------------------
# Main Agent Flow
# -------------------------------
def main():
    user_command = input("💬 What would you like to send? ➤ ")

    contact_name, email = get_recipient_entity(user_command)
    if not email:
        print("❌ Recipient not found in contacts.")
        return

    subject = f"Update regarding {contact_name.capitalize()}"
    body = generate_email(subject, user_command, recipient_role=contact_name)


    service = get_gmail_service()
    send_email(service, to=email, subject=subject, body=body)

if __name__ == "__main__":
    main()
