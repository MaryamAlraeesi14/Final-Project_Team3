class Ticket:
    """Represents a ticket type for the Grand Prix."""

    def __init__(self, ticket_id, ticket_type, price):
        # Initialize ticket attributes
        self._ticket_id = ticket_id
        self._ticket_type = ticket_type
        self._price = price

    def get_ticket_id(self):
        # Return the unique ID of the ticket
        return self._ticket_id

    def get_ticket_type(self):
        # Return the type of the ticket (e.g., VIP, General, Student)
        return self._ticket_type

    def get_price(self):
        # Return the price of the ticket
        return self._price

    def set_price(self, price):
        # Update the price of the ticket
        self._price = price

    def __str__(self):
        # Return a string representation of the Ticket object
        return f"Ticket[{self._ticket_id}] {self._ticket_type} - AED {self._price}"
