# ---------- Imports ----------
import tkinter as tk
from tkinter import messagebox
import pickle
import os

from user import Fan, Admin           # Custom user classes
from ticket import Ticket             # Custom ticket class
from ticket_system import TicketSystem  # Booking and admin logic

# ---------- Utility Functions ----------
def save_data(filename, data):
    """Save data to a pickle file."""
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_data(filename):
    """Load data from a pickle file if it exists."""
    return pickle.load(open(filename, 'rb')) if os.path.exists(filename) else []

# ---------- Load Stored Data ----------
users = load_data('users.pkl')        # List of Fan and Admin users
tickets = load_data('tickets.pkl')    # List of available tickets
bookings = load_data('bookings.pkl')  # List of all bookings made

# ---------- Initialize Ticket System ----------
system = TicketSystem()
system._users = users
system._tickets = tickets
system._bookings = bookings

# ---------- Main GUI Application ----------
class GrandPrixSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grand Prix Ticketing System")
        self.geometry("600x650")
        self.current_user = None  # Stores currently logged-in Fan
        self.init_main_menu()     # Launch with main menu

    def clear_widgets(self):
        """Clear all widgets from the current window/frame."""
        for widget in self.winfo_children():
            widget.destroy()

    # ---------- Main Menu ----------
    def init_main_menu(self):
        """Display the main menu for login/registration."""
        self.clear_widgets()
        tk.Label(self, text="Welcome to Grand Prix Ticketing System", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="Fan Login", command=self.init_fan_login).pack(pady=5)
        tk.Button(self, text="Fan Registration", command=self.init_fan_register).pack(pady=5)
        tk.Button(self, text="Admin Login", command=self.init_admin_login).pack(pady=5)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=20)

    # ---------- Fan Registration ----------
    def init_fan_register(self):
        """Form for creating a new fan account."""
        self.clear_widgets()
        tk.Label(self, text="Register Fan Account", font=("Arial", 16)).pack(pady=10)

        # Input fields
        tk.Label(self, text="User ID:").pack()
        self.reg_id_entry = tk.Entry(self)
        self.reg_id_entry.pack()

        tk.Label(self, text="Name:").pack()
        self.reg_name_entry = tk.Entry(self)
        self.reg_name_entry.pack()

        tk.Label(self, text="Email:").pack()
        self.reg_email_entry = tk.Entry(self)
        self.reg_email_entry.pack()

        # Buttons
        tk.Button(self, text="Register", command=self.register_fan).pack(pady=5)
        tk.Button(self, text="Back", command=self.init_main_menu).pack()

    def register_fan(self):
        """Register a new fan if the ID is not taken."""
        uid, name, email = self.reg_id_entry.get(), self.reg_name_entry.get(), self.reg_email_entry.get()

        # Check for duplicate ID
        if any(u.get_user_id() == uid for u in users):
            messagebox.showerror("Error", "User ID already exists.")
            return

        # Create and save new fan
        new_fan = Fan(uid, name, email)
        users.append(new_fan)
        save_data('users.pkl', users)
        messagebox.showinfo("Success", "Fan account created.")
        self.init_main_menu()

    # ---------- Fan Login ----------
    def init_fan_login(self):
        """Form for fan login."""
        self.clear_widgets()
        tk.Label(self, text="Fan Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="User ID:").pack()
        self.fan_login_entry = tk.Entry(self)
        self.fan_login_entry.pack()

        tk.Button(self, text="Login", command=self.login_fan).pack(pady=5)
        tk.Button(self, text="Back", command=self.init_main_menu).pack()

    def login_fan(self):
        """Check fan login credentials and open fan dashboard."""
        uid = self.fan_login_entry.get()
        matched = next((u for u in users if isinstance(u, Fan) and u.get_user_id() == uid), None)
        if matched:
            self.current_user = matched
            self.init_fan_dashboard()
        else:
            messagebox.showerror("Error", "Fan not found.")

    # ---------- Fan Dashboard ----------
    def init_fan_dashboard(self):
        """Main menu for logged-in fan."""
        self.clear_widgets()
        tk.Label(self, text=f"Welcome, {self.current_user.get_name()}", font=("Arial", 16)).pack(pady=10)

        # Show user details
        tk.Label(self, text=self.current_user.view_account_details()).pack(pady=5)

        # Fan options
        tk.Button(self, text="Book Ticket", command=self.init_ticket_booking).pack(pady=5)
        tk.Button(self, text="View Bookings", command=self.view_bookings).pack(pady=5)
        tk.Button(self, text="Delete Account", fg="red", command=self.delete_account).pack(pady=5)
        tk.Button(self, text="Logout", command=self.init_main_menu).pack(pady=20)

    def view_bookings(self):
        """Display fan's past bookings."""
        self.clear_widgets()
        tk.Label(self, text="Your Booked Tickets", font=("Arial", 16)).pack(pady=10)
        history = self.current_user.get_booking_history()
        if history:
            for b in history:
                tk.Label(self, text=str(b), wraplength=500, justify="left").pack(anchor="w", padx=15, pady=5)
        else:
            tk.Label(self, text="No bookings found.").pack()
        tk.Button(self, text="Back", command=self.init_fan_dashboard).pack(pady=10)

    def delete_account(self):
        """Delete the fan account permanently."""
        users.remove(self.current_user)
        save_data('users.pkl', users)
        messagebox.showinfo("Deleted", "Account deleted.")
        self.current_user = None
        self.init_main_menu()

    # ---------- Ticket Booking ----------
    def init_ticket_booking(self):
        """Form for fan to choose ticket and book it."""
        self.clear_widgets()
        tk.Label(self, text="Book a Ticket", font=("Arial", 16)).pack(pady=10)

        # Display ticket options as radio buttons
        self.ticket_var = tk.StringVar()
        for ticket in tickets:
            desc = (
                f"{ticket.get_ticket_type()} - AED {ticket.get_price()}\n"
                f"Validity: {'Single day' if 'Single' in ticket.get_ticket_type() else '3 days' if 'Weekend' in ticket.get_ticket_type() else 'All season'}\n"
                f"Features: {'Access to main event' if 'Single' in ticket.get_ticket_type() else 'All races + Pit access' if 'Weekend' in ticket.get_ticket_type() else 'All-season VIP access'}"
            )
            tk.Radiobutton(self, text=desc, variable=self.ticket_var, value=ticket.get_ticket_id(),
                           justify="left", anchor="w", wraplength=500).pack(anchor="w", padx=10, pady=5)

        # Quantity and payment input
        tk.Label(self, text="Quantity:").pack()
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.pack()

        tk.Label(self, text="Select Payment Method:").pack()
        self.payment_var = tk.StringVar()
        tk.OptionMenu(self, self.payment_var, "Credit Card", "Debit Card", "Digital Wallet").pack()

        # Book ticket
        tk.Button(self, text="Confirm Booking", command=self.book_ticket).pack(pady=10)
        tk.Button(self, text="Back", command=self.init_fan_dashboard).pack()

    def book_ticket(self):
        """Confirm and process ticket booking."""
        ticket_id = self.ticket_var.get()
        try:
            quantity = int(self.quantity_entry.get())
            payment = self.payment_var.get()
            if not payment:
                messagebox.showerror("Error", "Please select a payment method.")
                return
            booking = system.book_ticket(self.current_user, ticket_id, quantity, payment)
            bookings.append(booking)
            save_data('bookings.pkl', bookings)
            save_data('users.pkl', users)
            messagebox.showinfo("Success", "Ticket booked successfully!")
            self.init_fan_dashboard()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # ---------- Admin Login ----------
    def init_admin_login(self):
        """Form for admin login."""
        self.clear_widgets()
        tk.Label(self, text="Admin Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Admin ID:").pack()
        self.admin_id_entry = tk.Entry(self)
        self.admin_id_entry.pack()

        tk.Button(self, text="Login", command=self.login_admin).pack(pady=5)
        tk.Button(self, text="Back", command=self.init_main_menu).pack()

    def login_admin(self):
        """Verify admin credentials and open dashboard."""
        aid = self.admin_id_entry.get()
        matched = next((a for a in users if isinstance(a, Admin) and a.get_user_id() == aid), None)
        if matched:
            self.init_admin_dashboard()
        else:
            messagebox.showerror("Error", "Admin not found.")

    def init_admin_dashboard(self):
        """Show ticket sales breakdown to admin."""
        self.clear_widgets()
        tk.Label(self, text="Ticket Sales Overview", font=("Arial", 16)).pack(pady=10)
        sales = system.view_ticket_sales()
        for ticket_type, count in sales.items():
            tk.Label(self, text=f"{ticket_type}: {count} tickets sold").pack()
        tk.Button(self, text="Back to Main Menu", command=self.init_main_menu).pack(pady=20)

# ---------- Run the Application ----------
if __name__ == "__main__":
    app = GrandPrixSystem()
    app.mainloop()
