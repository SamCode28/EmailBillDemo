from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#Classes
from admin import Admin

#Used to edit clients
admin = Admin()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
creds = None

def generate_calendar(start_date, end_date):
  global creds

  if (not creds):
    flow = InstalledAppFlow.from_client_secrets_file(os.environ['CREDS'], SCOPES)
    creds = flow.run_local_server(port=0)

  try:
    #Creates the google calender resource object
    service = build("calendar", "v3", credentials=creds)

    #https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#list
    #Create a service object
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_date,
            timeMax=end_date,
            maxResults=1000,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    #Returns a list of calendar events
    #[] used as backup.  If no items in "items" exist, an empty list is returned.
    calendar_events = events_result.get("items", [])

    for event in calendar_events: 
      #Saves the date of each event in utc format
      utc_date = event["start"].get("dateTime", event["start"].get("date"))
      #Converts the date into something more readable for the user Ex. 2025-12-03T06:00:00-16:00 -> 2025-12-03 at 04:00 PM
      readable_date = utc_date_to_readable_date(utc_date)

      #If the title of the calendar event matches the "calendar_name" of a client in the admin.client_list
      #Updates the "dates_trained" for each client found
      if(admin.client_list.get(event["summary"])):
        client_found = admin.client_list[event["summary"]]
        client_found.dates_trained.append(readable_date)
        
        if len(event.get("attendees", [])) > 0:
          user_email = event["attendees"][0].get("email")
          if(user_email == "REDACTED@gmail.com"):
            user_email = event["attendees"][1].get("email")
          client_found.email = user_email

    if not calendar_events:
      print("No sessions found in this period.")
      return
    
    admin.update_client_bill_totals()

  except HttpError as error:
    print(f"An error occurred: {error}")

def utc_date_to_readable_date(date : str):
  #ex. 2025-12-03T06:00:00-16:00 -> 2025-12-03T16:00 -> 2025-12-03 at 16:00
  formatted_date = date[:-9].replace("T", " at ")

  #convert time to am or pm
  date_hour = int(formatted_date[-5:-3])

  if(date_hour > 11):
    if(date_hour > 12):
      new_time = date_hour - 12
      #ex. 2025-12-03 at 16:00 -> 2025-12-03 at 04:00
      formatted_date = formatted_date.replace(f"at {formatted_date[-5:-3]}" , f"at {str(new_time)}")
    formatted_date += " PM."
    return formatted_date

  else:
    #ex. 2025-12-03 at 06:00 -> 2025-12-03 at 06:00 AM
    return formatted_date + " AM."
 
if __name__ == "__main__":
  generate_calendar()

  ##print(event["summary"], event.get("colorId")) XX Possibly use for color coordinating sessions attended, sick days, no shows...