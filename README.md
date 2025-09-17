# EmailBillDemo
This is the demo version of the application I currently use to generate and send monthly bills to my clients.  Personal details have been omitted for privacy.

## How to use this application:
The program prompts you for a starting and ending date to scrape data from.
These dates will be used to build a google calendar service object which contains data about calendar events from the chosen dates.
You will need valid google client secrets with the correct scope for this to work.  The program expects to find this information in your environment variables under the variable "CREDS".

Once the google calendar service object is created, it will populate all client session dates for the time period selected and add an email address for anyone who wishes to have their bill emailed.
From here you have the option to print the session data and/or email each client their monthly bill.
To send an email, you will again need to have valid google client secrets stored in the environmental variable "CREDS".

