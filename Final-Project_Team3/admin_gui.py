# ---------- Imports ----------
import tkinter as tk  # Tkinter for GUI
from tkinter import messagebox  # For displaying error/info pop-ups
import pickle  # For saving/loading Python objects
import os  # For checking file existence


# Import classes needed for admin and ticket system functionality
from user import Admin
from ticket_system import TicketSystem




# ---------- Utility Functions ----------
# Function to load data from a file if it exists
def load_data(filename):
  if os.path.exists(filename):
      with open(filename, 'rb') as f:
          return pickle.load(f)
  return []  # Return empty list if file doesn't exist




# ---------- Load Existing Data ----------
users = load_data('users.pkl')      # Load user data (including Admins)
bookings = load_data('bookings.pkl')  # Load bookings
tickets = load_data('tickets.pkl')    # Load available tickets




# ---------- Setup Ticket System ----------
# Create and configure the system with loaded data
system = TicketSystem()
system._users = users
system._bookings = bookings
system._tickets = tickets




# ---------- Admin GUI Class ----------
class AdminGUI(tk.Tk):
  def __init__(self):
      super().__init__()  # Initialize parent class
      self.title("Admin Dashboard - Ticket Sales")  # Window title
      self.geometry("550x400")  # Window size
      self.init_login_screen()  # Show login screen initially


  # Display login screen for admin
  def init_login_screen(self):
      self.clear_widgets()  # Clear old widgets
      tk.Label(self, text="Enter Admin ID", font=("Arial", 16)).pack(pady=10)
      self.admin_id_entry = tk.Entry(self)  # Entry field for admin ID
      self.admin_id_entry.pack()
      tk.Button(self, text="Login", command=self.validate_admin).pack(pady=10)


  # Validate entered admin ID
  def validate_admin(self):
      aid = self.admin_id_entry.get()
      # Find matching Admin object by user ID
      matched = next((a for a in users if isinstance(a, Admin) and a.get_user_id() == aid), None)
      if matched:
          self.init_dashboard()  # If valid, go to dashboard
      else:
          messagebox.showerror("Error", "Admin not found.")  # Show error if invalid


  # Display admin dashboard with ticket sales stats
  def init_dashboard(self):
      self.clear_widgets()  # Clear old screen
      tk.Label(self, text="Ticket Sales Overview", font=("Arial", 16)).pack(pady=10)


      sales = system.view_ticket_sales()  # Get ticket sales summary from system


      # Display sales summary by ticket type
      for ticket_type, count in sales.items():
          tk.Label(self, text=f"{ticket_type}: {count} tickets sold").pack()


      tk.Button(self, text="Exit", command=self.quit).pack(pady=20)  # Exit button


  # Utility function to clear the current window widgets
  def clear_widgets(self):
      for widget in self.winfo_children():
          widget.destroy()




# ---------- Run the Application ----------
if __name__ == "__main__":
  app = AdminGUI()  # Create instance of the admin GUI
  app.mainloop()  # Start the Tkinter event loop
