class Client:
    def __init__(self, calendar_name :str, rate : int, weekly_frequency : int):
        self.calendar_name = calendar_name
        self.rate =  rate
        self.dates_trained = []
        self.weekly_frequency = weekly_frequency
        self.max_bill = rate * weekly_frequency * 4
        self.email = None

    def get_bill(self):
        total = len(self.dates_trained) * self.rate

        if(total > self.max_bill):
            return self.max_bill
        
        return total

    def generate_bill_message(self, month, year):
        message = f"""<html>
        <head>
        <style>
        .session_list {{
            margin: 0;
        }}
        </style>
        </head>
        <body>
        <h1>Dates Serviced for {month} {year}:</h1>"""
        
        num_sesssion = 1

        #Add sessions to body
        for date_serviced in self.dates_trained:
            message += f"<p class='session_list'>{num_sesssion}. {date_serviced}</p>"
            num_sesssion += 1

        #Bill total
        message += f"<p>{month} Bill Total: ${self.get_bill()}.00</p>"

        #Attendance
        message += f"<p>Monthly Attendance = {num_sesssion - 1} / {self.weekly_frequency * 4}</p>"

        #Possible bonus sessions
        #If number sessions serviced is greater than number sessions scheduled
        if((num_sesssion - 1) - self.weekly_frequency * 4 > 0):
            sessions_saved = (num_sesssion - 1) - self.weekly_frequency * 4
            message += f"<p>Consistency is key!  You recieved {sessions_saved} free sessions this month due to your attendace!</p>"

        message += "<p>If you think any dates listed are incorrect, please contact me at 111-111-1111!</p>"
        message += "<h2>My Business Name</h2>"

        message += "</body>"
        message += "</html>"

        return message
    
    def set_email(self, email):
        self.email = email