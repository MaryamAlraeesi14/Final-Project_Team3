# ---------- Imports ----------
import tkinter as tk  # GUI framework
from tkinter import messagebox  # For pop-up error/info dialogs
import pickle  # For saving/loading data
import os  # For file existence checking


# Import user and system-related classes
from user import Fan
from ticket import Ticket
from ticket_system import TicketSystem




# ---------- Utility Functions ----------
# Save data to a file using pickle
def save_data(filename, data):
  with open(filename, 'wb') as f:
      pickle.dump(data, f)


# Load data from a file if it exists, otherwise return an empty list
def load_data(filename):
  if os.path.exists(filename):
      with open(filename, 'rb') as f:
          return pickle.load(f)
  return []




# ---------- Load Existing Data ----------
# Load users, tickets, and bookings data from files
users = load_data('users.pkl')
tickets = load_data('tickets.pkl')
bookings = load_data('bookings.pkl')




# ---------- Setup Ticket System ----------
# Create an instance of the TicketSystem and assign the loaded data
system = TicketSystem()
system._users = users
system._tickets = tickets
system._bookings = bookings




# ---------- GUI Class ----------
class TicketGUI(tk.Tk):
  def __init__(self):
      super().__init__()
      self.title("Grand Prix - Ticket Booking")  # Set window title
      self.geometry("600x650")  # Set window size
      self.current_fan = None  # Currently logged in Fan
      self.init_login_screen()  # Start with the login screen


  # Login screen to enter Fan ID
  def init_login_screen(self):
      self.clear_widgets()  # Clear any existing widgets
      tk.Label(self, text="Enter your Fan ID to Book Tickets", font=("Arial", 14)).pack(pady=10)
      self.fan_id_entry = tk.Entry(self)  # Entry field for Fan ID
      self.fan_id_entry.pack()
      tk.Button(self, text="Proceed", command=self.load_fan).pack(pady=5)  # Proceed button


  # Load fan details based on entered ID
  def load_fan(self):
      uid = self.fan_id_entry.get()
      # Search for a matching Fan object in the users list
      matched = next((u for u in users if isinstance(u, Fan) and u.get_user_id() == uid), None)
      if matched:
          self.current_fan = matched  # Save the fan object
          self.init_ticket_booking_screen()  # Proceed to ticket booking
      else:
          messagebox.showerror("Error", "Fan not found.")  # Show error if not found


  # Show screen with available tickets and booking form
  def init_ticket_booking_screen(self):
      self.clear_widgets()
      tk.Label(self, text="Available Tickets", font=("Arial", 14)).pack(pady=10)


      self.ticket_var = tk.StringVar()  # Variable to hold selected ticket ID


      if not tickets:
          tk.Label(self, text="No tickets available.").pack()
          return


      # Display each ticket as a radio button with details
      for ticket in tickets:
          desc = (
              f"{ticket.get_ticket_type()} - AED {ticket.get_price()}\n"
              f"Validity: {'Single day' if 'Single' in ticket.get_ticket_type() else '3 days' if 'Weekend' in ticket.get_ticket_type() else 'All season'}\n"
              f"Features: {'Access to main event' if 'Single' in ticket.get_ticket_type() else 'All races + Pit access' if 'Weekend' in ticket.get_ticket_type() else 'All-season VIP access'}"
          )
          tk.Radiobutton(
              self,
              text=desc,
              variable=self.ticket_var,
              value=ticket.get_ticket_id(),
              justify="left",
              anchor="w",
              wraplength=500
          ).pack(anchor="w", padx=10, pady=5)


      # Quantity input
      tk.Label(self, text="Quantity:").pack()
      self.quantity_entry = tk.Entry(self)
      self.quantity_entry.pack()


      # Payment method selection
      tk.Label(self, text="Select Payment Method:").pack(pady=(10, 0))
      self.payment_var = tk.StringVar()
      self.payment_dropdown = tk.OptionMenu(self, self.payment_var, "Credit Card", "Debit Card", "Digital Wallet")
      self.payment_dropdown.pack()


      # Book and back buttons
      tk.Button(self, text="Book Ticket", command=self.book_ticket).pack(pady=10)
      tk.Button(self, text="Back", command=self.init_login_screen).pack()


  # Process ticket booking
  def book_ticket(self):
      ticket_id = self.ticket_var.get()
      try:
          quantity = int(self.quantity_entry.get())  # Convert quantity to int
          payment_method = self.payment_var.get()
          if not payment_method:
              messagebox.showerror("Error", "Please select a payment method.")
              return
          # Book ticket through the system
          booking = system.book_ticket(self.current_fan, ticket_id, quantity, payment_method)
          bookings.append(booking)  # Add booking to list
          save_data('bookings.pkl', bookings)  # Save bookings
          save_data('users.pkl', users)  # Update users with booking info
          self.show_confirmation(booking)  # Show confirmation screen
      except ValueError as e:
          messagebox.showerror("Error", str(e))  # Catch invalid input errors


  # Show confirmation after booking
  def show_confirmation(self, booking):
      self.clear_widgets()
      tk.Label(self, text="Booking Confirmed!", font=("Arial", 18), fg="green").pack(pady=15)
      tk.Label(self, text=str(booking), wraplength=500, justify="left").pack(pady=10)
      tk.Button(self, text="Book Another Ticket", command=self.init_ticket_booking_screen).pack(pady=5)
      tk.Button(self, text="Back to Start", command=self.init_login_screen).pack(pady=5)


  # Utility function to remove all widgets from current screen
  def clear_widgets(self):
      for widget in self.winfo_children():
          widget.destroy()




# ---------- Run the Application ----------
if __name__ == "__main__":
  app = TicketGUI()  # Create an instance of the TicketGUI
  app.mainloop()  # Start the Tkinter main event loop
