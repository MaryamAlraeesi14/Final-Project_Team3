from user import Fan, Admin
from ticket import Ticket
from booking import Booking

class TicketSystem:
    """Manages users, tickets, and bookings."""

    def __init__(self):
        # Initialize lists for users, tickets, and bookings
        self._users = []
        self._tickets = []
        self._bookings = []

    def register_user(self, user):
        # Add a user to the system
        self._users.append(user)

    def add_ticket(self, ticket):
        # Add a ticket to the system
        self._tickets.append(ticket)

    def book_ticket(self, fan, ticket_id, quantity, payment_method):
        # Find the ticket by ID and create a booking if it exists
        ticket = next((t for t in self._tickets if t.get_ticket_id() == ticket_id), None)
        if ticket:
            # Generate a unique booking ID
            booking_id = f"B{len(self._bookings) + 1}"
            # Create a new booking and add it to the bookings list
            booking = Booking(booking_id, fan, ticket, quantity, payment_method)
            self._bookings.append(booking)
            return booking
        else:
            # Raise an error if the ticket ID is invalid
            raise ValueError("Invalid Ticket ID")

    def view_all_bookings(self):
        # Return the list of all bookings
        return self._bookings

    def view_ticket_sales(self):
        # Calculate total tickets sold for each ticket type
        sales = {}
        for b in self._bookings:
            ticket_type = b.get_ticket_type()
            sales[ticket_type] = sales.get(ticket_type, 0) + b.get_quantity()
        return sales
