from user import Fan, Admin
from ticket import Ticket
from ticket_system import TicketSystem

# --- Testing code ---
if __name__ == "__main__":
    # Create a new ticket system instance
    system = TicketSystem()

    # Create a fan and admin user
    fan1 = Fan("F001", "Maryam", "maryam@example.com")
    admin = Admin("A001", "AdminUser", "admin@example.com")
    # Register the users
    system.register_user(fan1)
    system.register_user(admin)

    # Create tickets for different types
    ticket1 = Ticket("T001", "Single Race", 350)
    ticket2 = Ticket("T002", "Weekend Package", 900)
    ticket3 = Ticket("T003", "Season Membership", 3000)
    # Add tickets to the system
    system.add_ticket(ticket1)
    system.add_ticket(ticket2)
    system.add_ticket(ticket3)

    # Make bookings for the fan
    booking1 = system.book_ticket(fan1, "T001", 2, "Credit Card")
    booking2 = system.book_ticket(fan1, "T002", 5, "Digital Wallet")

    # Print the booking history of the fan
    print("\nFan Booking History:")
    for b in fan1.get_booking_history():
        print(b)

    # Print the ticket sales summary for the admin
    print("\nAdmin View - Ticket Sales Summary:")
    sales = system.view_ticket_sales()
    for ticket_type, count in sales.items():
        print(f"{ticket_type}: {count} tickets sold")
