from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError # To catch specific DB errors
from models import User
from connection import engine

# Create a Session factory - we'll use this to create sessions
# It's configured not to autocommit or autoflush, giving us control.
# It's bound to our engine, which connects to the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- CRUD OPERATIONS ---

def create_user(name, email, password, phoneNumber):
    """Creates a new user in the database."""

    # Input validation
    if not all([name, email, password, phoneNumber]):
        return None, "Please provide all entries (name, email, password, phoneNumber)."

    # Use a context manager for the session (ensures it's closed)
    with SessionLocal() as session:
        try:
            # Check if user already exists
            exists = session.query(User).filter(User.email == email).first()
            if exists:
                return None, "User with this email already exists."

            # Create the User object
            # IMPORTANT: We should HASH the password here in a real app!
            new_user = User(
                name=name,
                email=email,
                password=password, # In a real app: hash_password(password)
                phoneNumber=phoneNumber
            )

            # Add to session and commit
            session.add(new_user)
            session.commit()

            # Refresh to get DB-assigned data (like the ID)
            session.refresh(new_user)

            # Return the new user object and a success message
            return new_user, "User created successfully."

        except IntegrityError as e: # Catch DB errors (like unique constraint)
            session.rollback() # Undo changes on error
            print(f"Database Integrity Error: {e}")
            return None, "Database error occurred. Could the email be a duplicate?"
        except Exception as e: # Catch any other unexpected errors
            session.rollback() # Undo changes on error
            print(f"An unexpected error occurred: {e}")
            return None, f"An unexpected error occurred: {e}"

def read_users():
    """Reads all users from the database."""
    with SessionLocal() as session:
        try:
            # Query all users and return them
            users = session.query(User).all()
            return users, "Users fetched successfully."
        except Exception as e:
            print(f"An error occurred while reading users: {e}")
            # Return an empty list and an error message on failure
            return [], f"An error occurred while reading users: {e}"

def update_user(user_id, name=None, password=None, phoneNumber=None):
    """Updates an existing user's details in the database."""

    if not user_id:
        return None, "Please provide a user ID."

    with SessionLocal() as session:
        try:
            # Find the user by their ID
            user = session.query(User).filter(User.id == user_id).first()

            # If user doesn't exist, return an error
            if not user:
                return None, "User not found."

            # Update fields only if new values are provided
            updated = False # Keep track if anything changed
            if name:
                user.name = name
                updated = True
            if password:
                # Remember: HASH this in a real app!
                user.password = password
                updated = True
            if phoneNumber:
                user.phoneNumber = phoneNumber
                updated = True

            # Only commit if something actually changed
            if updated:
                session.commit()
                session.refresh(user) # Refresh to get latest data
                return user, "User updated successfully."
            else:
                # If no changes, still return the user but with a different message
                return user, "No changes provided for update."

        except Exception as e:
            session.rollback()
            print(f"An error occurred while updating user {user_id}: {e}")
            return None, f"An error occurred: {e}"

def delete_user(user_id):
    """Deletes a user from the database by their ID."""

    if not user_id:
        return False, "Please provide a user ID."

    with SessionLocal() as session:
        try:
            # Find the user by their ID
            user = session.query(User).filter(User.id == user_id).first()

            # If user doesn't exist, return an error
            if not user:
                return False, "User not found."

            # Delete the user and commit
            session.delete(user)
            session.commit()

            # Return True (for success) and a message
            return True, "User deleted successfully."

        except Exception as e:
            session.rollback()
            print(f"An error occurred while deleting user {user_id}: {e}")
            # Return False (for failure) and a message
            return False, f"An error occurred: {e}"

# You could also add helper functions here, like:
def get_user_by_id(user_id):
    """Finds a single user by their ID."""
    with SessionLocal() as session:
        return session.query(User).filter(User.id == user_id).first()

def get_user_by_email(email):
    """Finds a single user by their email."""
    with SessionLocal() as session:
        return session.query(User).filter(User.email == email).first()