from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# This is the base class our model will inherit from
Base = declarative_base()

# This class defines the 'users' table in our database
class User(Base):
    __tablename__ = "users"

    # Define the columns (fields) for the 'users' table
    id = Column(Integer, primary_key=True, index=True) # Added index=True for faster lookups by id
    name = Column(String(100), nullable=False) # Added nullable=False to ensure name is required
    email = Column(String(100), unique=True, index=True, nullable=False) # Added index=True and nullable=False
    password = Column(String(255), nullable=False) # Added nullable=False
    phoneNumber = Column(String(20), nullable=False) # Increased length slightly, added nullable=False

    # This is an "initializer" method. It runs when you create a new User object.
    # It makes it easy to set the values when you create a user.
    def __init__(self, name, email, password, phoneNumber):
        self.name = name
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber

    # This helps in printing the User object in a readable way (optional but good for debugging)
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

    # This function will help us convert a User object to a dictionary,
    # which is useful when sending data back in our API responses.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phoneNumber": self.phoneNumber
            # We DON'T include the password in the response for security!
        }