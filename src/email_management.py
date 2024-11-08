import os.path
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import google.generativeai as genai  # Ensure Gemini API client is imported
from google.auth.transport.requests import Request
from config import GEMINI_API_KEY, GMAIL_CREDENTIALS_PATH, GMAIL_TOKEN_PATH

# Define the Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']

# Initialize Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def authenticate_gmail():
    creds = None
    if os.path.exists(GMAIL_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def fetch_emails(service):
    try:
        results = service.users().messages().list(userId='me', maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
            return

        for msg in messages:
            message = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = {header['name']: header['value'] for header in message['payload']['headers']}
            id = message['id']
            sender = headers.get("From", "Unknown Sender")
            receiver = headers.get("To", "Unknown Receiver")
            subject = headers.get("Subject", "No Subject")
            snippet = message['snippet']

            print(f"Email ID: {id}")
            print(f"From: {sender}")
            print(f"To: {receiver}")
            print(f"Subject: {subject}")
            print(f"Snippet: {snippet}")

            # Check for attachments
            has_attachment = any(part.get('filename') for part in message['payload'].get('parts', []))
            if has_attachment:
                print("This email has attachments.")
            print("=" * 40)

    except HttpError as error:
        print(f"An error occurred: {error}")

def send_email(service, to_email, subject, message_text):
    try:
        message = MIMEText(message_text)
        message['To'] = to_email
        message['Subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        send_message = {'raw': raw_message}
        sent_message = service.users().messages().send(userId='me', body=send_message).execute()
        print(f"Message sent! Id: {sent_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def summarize_email(service, email_id):
    try:
        message = service.users().messages().get(userId='me', id=email_id).execute()
        snippet = message['snippet']

        # Summarize the email content using Gemini
        summary = model.generate_content(f"Summarize this email: {snippet}")
        print("Summary:", summary.text)

    except HttpError as error:
        print(f"An error occurred: {error}")

def send_email_with_generated_response(service, email_id):
    try:
        message = service.users().messages().get(userId='me', id=email_id).execute()
        snippet = message['snippet']

        # Generate response using Gemini
        response = model.generate_content("Reply to this email: " + snippet)
        print("Generated Response:", response.text)

        # Extract sender's email to reply to
        headers = {header['name']: header['value'] for header in message['payload']['headers']}
        sender_email = headers.get("From")

        # Send the response
        send_email(service, sender_email, "Re: " + headers.get("Subject", "No Subject"), response.text)

    except HttpError as error:
        print(f"An error occurred: {error}")

# Example usage
if __name__ == "__main__":
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Fetch recent emails
    fetch_emails(service)

    # Example: Send an email
    #send_email(service, "test@test.test", "Test Email", "This is a test email sent from Aura.")

    # Example: Summarize an email by ID
    # summarize_email(service, "EMAIL_ID_HERE")

    # Example: Generate and send a response
    # send_email_with_generated_response(service, "EMAIL_ID_HERE")
