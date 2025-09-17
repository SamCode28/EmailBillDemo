import base64
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
creds = None

def send_email(month, year, message_text, recipient = 'REDACTED@gmail.com'):
  global creds
  if(not creds):
    flow = InstalledAppFlow.from_client_secrets_file(os.environ['CREDS'], SCOPES)
    creds = flow.run_local_server(port=0)

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    message = MIMEText(message_text, "html")
    message["to"] = recipient
    message["from"] = "REDACTED@gmail.com"
    message["subject"] = f"{month} {year} Sessions Serviced"

    #Email's sent with Gmail API must be in base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {"raw": raw_message}
    service.users().messages().send(userId="me", body=body).execute()

    print(f"Email sent to {recipient}")

  except HttpError as error:
    print(f"An error occurred: {error}")

