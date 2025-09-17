#Classes
import google_calendar
from google_calendar import admin
import datetime
import google_gmail
import os

def main():
  print("Accessing your google calendar...")
  #Prompt user from month and year to start calendar lookup
  start_month = get_month("start")
  start_year = get_year("start")
  
  #Convert start time to UTC date
  calendar_date_start = month_dates[start_month].replace("year", str(start_year))
  print(f"Starting from: {start_month} {start_year}.\n")

  #While loop used to prevent user from entering end date earlier than start date
  while(True):
    #Prompt user for month and year to end calendar lookup
    end_month = get_month("end")
    end_year = get_year("end")
    #Convert end time to UTC date
    calendar_date_end = month_dates[end_month].replace("year", str(end_year))

    if(start_year < end_year):
      print("\nEnd date cannot be before start date. Please try again.\n")
      continue

    if(start_year == end_year):
      #Reduce UTC date to number value of month.  EX: 2024-06-01T06:00:00Z -> 06
      if(int(calendar_date_start[5:7]) >= int(calendar_date_end[5:7])):
        print("\nEnd date cannot be before start date.  Please try again.\n")
        continue
    print(f"Ending lookup at: {end_month} {end_year}\n") 
    break

  print(f"Getting events starting from {start_month} {start_year} until start of {end_month} {end_year}....\n")
  
  #Creates calendar for date entered.  Populates all client's "sessions_attended", "dates_trained", "email" if listed and "bill" for the time period entered.
  google_calendar.generate_calendar(calendar_date_start, calendar_date_end)

  #Display options to interact with calendar
  while(True):
    print(f"\nPlease enter an integer from 1-5 to interact with calendar.\n")
    option_selected = calendar_option_selected()
    call_calendar_method_of(option_selected, start_month, start_year)

    if(option_selected == 5):
      break



def call_calendar_method_of(option_selected, month, year):
  match option_selected:
    case 1:
      admin.print_all_client_bills()
    case 2:
      admin.print_single_client_bill()
    case 3:
      admin.send_email_all_clients(month, year)
    case 4:
      admin.send_email_single_client(month, year)
    case 5:
      pass

def calendar_option_selected():
  while(True):
      try:
        print("1. Print all client sessions.")
        print("2. Print single client's sessions.")
        print("3. Send bill to all clients.")
        print("4. Send bill to single client.")
        print("5. Close program.")
        answer = int(input("Enter digit: "))

        if (answer < 1 or answer > 5):
          print("\nNumber must be and integer from 1 to 5.\n")
          continue

      except Exception:
        print("\nNumber must be and integer from 1 to 5.\n")

      else:
        return answer
  

def get_month(start_stop : str):
  while(True):
    try:
      month = input(f"What month would you like the calendar to {start_stop}? ").strip().lower().capitalize()
      check_valid_month(month)  
    except:
      print("\nThe month must be a word, Ex. May, June.  Please check your spelling and try again.\n")
    else:
      return month
    
def check_valid_month(month : str):
  if (month_dates[month]):
    return True
  else:
    return Exception

def get_year(start_stop : str):
  while(True):
    try:
      year = int(input(f"What year would you like the calendar to {start_stop}? "))
      current_year = datetime.datetime.now().year

      if (year < 2024 or year > current_year):
        print(f"\nYear must be between 2024 and {current_year}.\n")
        continue

    except:
      print("\nThe year must be an integer. Ex. 2024\n")
    else:
      return year

month_dates = {
  "January" : "year-01-01T06:00:00Z",
  "February" :"year-02-01T06:00:00Z",
  "March" : "year-03-01T06:00:00Z",
  "April" : "year-04-01T06:00:00Z",
  "May" : "year-05-01T06:00:00Z",
  "June" : "year-06-01T06:00:00Z",
  "July" : "year-07-01T06:00:00Z",
  "August" : "year-08-01T06:00:00Z",
  "September" : "year-09-01T06:00:00Z",
  "October" : "year-10-01T06:00:00Z",
  "November" : "year-11-01T06:00:00Z",
  "December" : "year-12-01T06:00:00Z"
}

if __name__ == "__main__":
  main()
