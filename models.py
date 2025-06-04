# so models.py is where we have our models ....i.e tables
# it is a fancy way of saying database tables
# we are only focused on one particular table which is the user's table, and would be created via a specific class
# and before we write the class, we need to declare our sql alchemy base

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# this declarative base, we are declaring our model's file. so this is we declaring the point of entry
# so anytime we create a class, i would use the base to kind of define it, i.e. declare
# *** basically it would be inheriting of the class

Base = declarative_base()

class User(Base): # what this means is that, incase you are going to create this table 'User', please declare it all... inherit all the sqlalchemy operations 'From Base' within it, because I am trying to mark it as part of the database tabl
#so now lets define our table name and sign up info, since the ultimate goal is to create a users table to store all the users that have signed up
    __tablename__ = 'users' # users is always plural because we taking for more than one user
    id = Column(Integer, primary_key=True)   # setting this as our primary key (unique identifier) cause why not. and obviously its going to be an integer
    name = Column(String(100)) # setting another column as the 'name' while limiting its character count to 100
    email = Column(String(100), unique=True) # making the email not exceeding 100 characters and email being unique because you don't want anyone signing up with the same email
    password = Column(String(255))
    # so with this, we've created our first table 
    phoneNumber = Column(Integer)
    


