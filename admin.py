from client import Client
import google_gmail

donald_d = Client("Donald Duck", 50, 2)
mickey_m = Client("Mickey Mouse", 50, 2)
bugs_b = Client("Bugs Bunny", 100, 1)
daisy_d = Client("Daisy Duck", 50, 2)
minnie_m = Client("Minnie Mouse L", 25, 3)


class Admin:
    def __init__(self):
        self.client_list = {
            "Donald Duck" : donald_d,
            "Mickey Mouse" : mickey_m,
            "Bugs Bunny" : bugs_b,
            "Daisy Duck" : daisy_d,
            "Minnie Mouse" : minnie_m,
        }
        self.bill_total = 0

    def update_client_bill_totals(self):
        for client in self.client_list.values():
            self.bill_total += client.get_bill()

    def print_all_client_bills(self):
        for client in self.client_list.values():
            num_sesssion = 1
            print("Dates Serviced:")
            for date_serviced in client.dates_trained:
                print(f"{num_sesssion}. {date_serviced}")
                num_sesssion += 1
            
            print(f"{client.calendar_name}: ${client.get_bill()}\n")
            if(client.email != None):
              print(f"{client.email}\n")

        print(f"\nTotal: ${self.bill_total}.")

    def print_single_client_bill(self):
        while(True):
          try:
            client_selected = input("Who's bill would you like printed? ")
            if(self.client_list[client_selected]):
                pass
          except:
              print("\nPlease check your spelling.  Name must match client 'calendar_name'.\n")
  
          else:
                num_sesssion = 1
                print("Dates Serviced:")
                for date_serviced in self.client_list[client_selected].dates_trained:
                    print(f"{num_sesssion}. {date_serviced}")
                    num_sesssion += 1
                return
                  
    def send_email_single_client(self, month, year):
        while(True):
          try:
            client_selected_input = input("Who's bill would you like emailed? ")
            if(self.client_list[client_selected_input]):
                client_selected = self.client_list[client_selected_input]

            if(client_selected.email == None):
                print("No client email listed")
                break
          except:
              print("\nPlease check your spelling.  Name must match client's 'calendar_name'.\n")
  
          else:
                google_gmail.send_email(month, year, client_selected.generate_bill_message(month, year), client_selected.email)
                return


    def send_email_all_clients(self, month, year):
        for client in self.client_list.values():
            if(client.email != None):
                google_gmail.send_email(month, year, client.generate_bill_message(month, year), client.email)

