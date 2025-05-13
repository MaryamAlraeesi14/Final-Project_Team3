import pickle
from user import Admin


# Create a sample admin user
admin = Admin("1234", "AdminUser", "admin@example.com")


# Load existing users or create new list
try:
   with open("users.pkl", "rb") as f:
       users = pickle.load(f)
except:
   users = []


# Add admin only if not already present
if not any(u.get_user_id() == "1234" for u in users):
   users.append(admin)


# Save back to file
with open("users.pkl", "wb") as f:
   pickle.dump(users, f)


print("Admin user '1234' added.")
