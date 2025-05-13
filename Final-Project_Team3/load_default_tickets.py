# Import the 'pickle' module to serialize and save Python objects to a file
import pickle


# Import the Ticket class from the ticket module
from ticket import Ticket


# Create a list of default ticket types using the Ticket class
default_tickets = [
   Ticket("T001", "Single Race Pass", 350),       # A single race ticket priced at 350
   Ticket("T002", "Weekend Package", 900),        # A weekend access package ticket priced at 900
   Ticket("T003", "Season Membership", 3000),     # A season-long membership ticket priced at 3000
   Ticket("T004", "Group Discount (5+)", 320)     # A group ticket (5 or more people) priced at 320 each
]


# Open a file called 'tickets.pkl' in binary write mode ('wb')
with open("tickets.pkl", "wb") as f:
   # Serialize and save the list of default_tickets to the file
   pickle.dump(default_tickets, f)


# Print a confirmation message indicating success
print("Default tickets loaded into tickets.pkl")
