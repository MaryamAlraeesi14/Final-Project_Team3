from datetime import datetime

class Booking:
    """Manages a ticket booking by a fan."""

    def __init__(self, booking_id, fan, ticket, quantity, payment_method):
        # Initialize booking attributes
        self._booking_id = booking_id
        self._fan = fan
        self._ticket = ticket
        self._quantity = quantity
        self._payment_method = payment_method
        self._date = datetime.now()
        self._total_price = self._calculate_total()

        # Automatically add this booking to the fan's booking history
        fan.add_booking(self)

    def _calculate_total(self):
        # Calculate the total price, applying a discount for bulk purchases (5 or more tickets)
        base_total = self._ticket.get_price() * self._quantity
        if self._quantity >= 5:
            return base_total * 0.9  # 10% discount for bulk purchases
        return base_total

    def get_total_price(self):
        # Return the total price of the booking
        return self._total_price

    def get_ticket_type(self):
        # Return the type of ticket booked
        return self._ticket.get_ticket_type()

    def get_quantity(self):
        # Return the quantity of tickets booked
        return self._quantity

    def get_payment_method(self):
        # Return the payment method used for this booking
        return self._payment_method

    def __str__(self):
        # Return a string representation of the Booking object
        return (f"Booking[{self._booking_id}] - {self._ticket.get_ticket_type()} x {self._quantity} "
                f"on {self._date.strftime('%Y-%m-%d')} | Payment: {self._payment_method} | "
                f"Total: AED {self._total_price:.2f}")
