class User:
    """Base class for all users in the system."""

    def __init__(self, user_id, name, email):
        # Initialize user attributes
        self._user_id = user_id
        self._name = name
        self._email = email

    def get_user_id(self):
        # Return the user ID
        return self._user_id

    def get_name(self):
        # Return the name of the user
        return self._name

    def set_name(self, name):
        # Set a new name for the user
        self._name = name

    def get_email(self):
        # Return the email address of the user
        return self._email

    def set_email(self, email):
        # Set a new email address for the user
        self._email = email

    def __str__(self):
        # Return a string representation of the User object
        return f"User ID: {self._user_id}, Name: {self._name}, Email: {self._email}"


class Fan(User):
    """A fan who can purchase tickets and manage bookings."""

    def __init__(self, user_id, name, email):
        # Initialize fan attributes, including booking history
        super().__init__(user_id, name, email)
        self._booking_history = []  # Stores the booking history for the fan

    def add_booking(self, booking):
        # Add a booking to the fan's booking history
        self._booking_history.append(booking)

    def get_booking_history(self):
        # Return the fan's booking history as a list
        return self._booking_history

    def view_account_details(self):
        # Return a summary of the fan's account details
        return f"Fan Account - Name: {self._name}, Email: {self._email}, Bookings: {len(self._booking_history)}"

    def __str__(self):
        # Return a string representation of the Fan object, including booking count
        return f"Fan: {super().__str__()} | Bookings: {len(self._booking_history)}"


class Admin(User):
    """Admin user who can view ticket sales."""

    def __init__(self, user_id, name, email):
        # Initialize admin attributes
        super().__init__(user_id, name, email)

    def __str__(self):
        # Return a string representation of the Admin object
        return f"Admin: {super().__str__()}"
