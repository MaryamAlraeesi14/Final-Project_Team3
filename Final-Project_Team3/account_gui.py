# Import the required modules for GUI, data storage, and file handling
import tkinter as tk
from tkinter import messagebox
import pickle
import os


# Import the Fan and Admin classes from the user module
from user import Fan, Admin


# Function to save data (e.g., user list) to a file using pickle
def save_data(filename, data):
  with open(filename, 'wb') as f:
      pickle.dump(data, f)


# Function to load data from a file using pickle, returns an empty list if file doesn't exist
def load_data(filename):
  if os.path.exists(filename):
      with open(filename, 'rb') as f:
          return pickle.load(f)
  return []


# Load the user data from 'users.pkl' when the program starts
users = load_data('users.pkl')


# Define the main GUI class for account management, inheriting from Tkinter's Tk class
class AccountGUI(tk.Tk):
  def __init__(self):
      super().__init__()  # Initialize the parent class
      self.title("Grand Prix - Account Management")  # Set window title
      self.geometry("500x500")  # Set window size
      self.current_user = None  # Placeholder for the currently logged-in user
      self.init_login_screen()  # Load the login screen on start


  # Function to initialize the login screen interface
  def init_login_screen(self):
      self.clear_widgets()  # Clear previous widgets (if any)


      tk.Label(self, text="Login", font=("Arial", 18)).pack(pady=10)


      tk.Label(self, text="User ID:").pack()
      self.user_id_entry = tk.Entry(self)  # Input for user ID
      self.user_id_entry.pack()


      tk.Button(self, text="Login", command=self.login_user).pack(pady=5)
      tk.Button(self, text="Create New Fan Account", command=self.init_register_screen).pack()


  # Function to initialize the registration screen interface
  def init_register_screen(self):
      self.clear_widgets()  # Clear previous widgets


      tk.Label(self, text="Register Fan Account", font=("Arial", 18)).pack(pady=10)


      tk.Label(self, text="User ID:").pack()
      self.reg_id_entry = tk.Entry(self)  # Input for new user ID
      self.reg_id_entry.pack()


      tk.Label(self, text="Name:").pack()
      self.reg_name_entry = tk.Entry(self)  # Input for name
      self.reg_name_entry.pack()


      tk.Label(self, text="Email:").pack()
      self.reg_email_entry = tk.Entry(self)  # Input for email
      self.reg_email_entry.pack()


      tk.Button(self, text="Register", command=self.register_fan).pack(pady=5)
      tk.Button(self, text="Back to Login", command=self.init_login_screen).pack()


  # Function to register a new fan account
  def register_fan(self):
      uid = self.reg_id_entry.get()
      name = self.reg_name_entry.get()
      email = self.reg_email_entry.get()


      # Check if user ID already exists
      if any(u.get_user_id() == uid for u in users):
          messagebox.showerror("Error", "User ID already exists.")
          return


      # Create a new fan object and save it
      new_fan = Fan(uid, name, email)
      users.append(new_fan)
      save_data('users.pkl', users)
      messagebox.showinfo("Success", "Fan account created.")
      self.init_login_screen()  # Go back to login after registration


  # Function to log in a user
  def login_user(self):
      uid = self.user_id_entry.get()
      # Search for the user by ID
      matched = next((u for u in users if u.get_user_id() == uid), None)


      if matched:
          self.current_user = matched  # Set current user
          self.init_account_dashboard()  # Load account dashboard
      else:
          messagebox.showerror("Error", "User ID not found.")


  # Function to display account dashboard after login
  def init_account_dashboard(self):
      self.clear_widgets()
      # Welcome message
      tk.Label(self, text=f"Welcome {self.current_user.get_name()}", font=("Arial", 16)).pack(pady=10)


      # Show user account details
      tk.Label(self, text=self.current_user.view_account_details(), font=("Arial", 12)).pack(pady=5)


      # Show ticket booking history only for Fan users
      if isinstance(self.current_user, Fan):
          bookings = self.current_user.get_booking_history()
          if bookings:
              tk.Label(self, text="Your Booked Tickets:", font=("Arial", 14)).pack(pady=10)
              for booking in bookings:
                  tk.Label(self, text=str(booking), wraplength=480, justify="left", anchor="w").pack(anchor="w", padx=15, pady=5)
          else:
              tk.Label(self, text="No tickets booked yet.").pack(pady=10)


      # Provide options to delete account or logout
      tk.Button(self, text="Delete Account", fg="red", command=self.delete_account).pack(pady=5)
      tk.Button(self, text="Logout", command=self.init_login_screen).pack()


  # Function to delete the current user account
  def delete_account(self):
      users.remove(self.current_user)  # Remove user from list
      save_data('users.pkl', users)  # Save updated list
      messagebox.showinfo("Deleted", "Your account has been deleted.")
      self.current_user = None
      self.init_login_screen()  # Return to login screen


  # Helper function to clear all widgets from the screen
  def clear_widgets(self):
      for widget in self.winfo_children():
          widget.destroy()


# Run the application if this file is executed directly
if __name__ == "__main__":
  app = AccountGUI()
  app.mainloop()
