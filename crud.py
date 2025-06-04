# for crud operations

# we are going to create something called a session
# whenever we are interacting with our database we need to use one session
# that session of creating, session of reading, session of updating, and session of deleting
# when we are done, it gives us the ability to close the database session. and prevents us from leaving the session open
# by doing this, we save alot of resources, server's memory

# Now to do our sessions>>>>

from models import User
from connection import engine
# now we are suppose to get our engine connection
#engine = create_engine("mysql+pymysql://{username}:{root_password}@db:{db_host}/{db_name}") # then you provide the database url

# so we will need something called session to track our database transaction or operations
from sqlalchemy.orm import sessionmaker
# it helps maps all the configuration for all the varieties of sql database and their process ... read, writing etc

Session = sessionmaker(bind=engine)

# now we have our session maker we can now start creating our crud function

# For C operation == Create

# remember our model is user, so everything is related to the user

# open endpoint for where the user would get to input these parameters
def create_user(user_name, user_email, user_password, user_phoneNumber): # you don't need to create the id because it is automatically generated ?? 
    if not user_name or not user_email or not user_password or not user_phoneNumber:
        raise ValueError; 'Please provide all entries'
    session = Session()

    try:
        exists = session.query(User).filter(User.email == user_email).first() # because we are trying to create based on an existing id, so it basically shouldn't exists
        if exists: 
            raise ValueError
            # raise {"message": "User already exists"}' # because it literally exists and there's no need creating a user because the id is occupied
        else:
        # basically the above serves as a checker. so if the above variable is present that means we can't proceed to go ahead populating the table .....
        # with the user_email because it is already present. we used the session query method to confirm this via querying 
            new_user= User(name=user_name,email=user_email, password=user_password,phoneNumber=user_phoneNumber)
            session.add(new_user)#atp, we have not added the user to the database, we just have it being held in a memory
            # we can also keep adding new info to the memory
            # new_user2= User(name=user_name,email=set(user_email), password=user_password,phoneNumber=user_phoneNumber)
            # session.add(new_user2)#atp, we have not added the user to the database, we just have it being held in a memory
            # and can as many users as possible, and once i am done, i can now add 
            session.commit() # to send to the database. So every insertion, i.e. everything that has being stored in the memory of the session, commits it to the database            
            return new_user # if you are done, we can now return the new user back, so that the front-end person can use it or save that person's information
#        new_user= User(user_name,user_email, user_password, user_phoneNumber) # or you can do it this way
# personally I believe that if this set for the email wasn't present, if we have an email that is already being inputted, then an error would be thrown because from the models.py side, it has been specified that the email column should be unique, remember  
        # now using the variables gotten from the create_user function to fit in the user table all done via.....
        # the new_user variable ..which serve as an instance to access the User class
    except Exception as e:
        raise e

    finally:
        session.close()
# becasue we want to save resources, we can go further by closing these sessions because we are done
#SO THIS IS HOW TO DO OUR CREATE IN OUR CRUD OPERATION

# if you look at the model, you have to follow the entities in the user table
# remember our id is automatically created i.e of a chronological order, we dont have to create it again


# NOW UNTO THE READ OPERATIONS :) # we want to literally 'read' the information in our database

def read_users(): # to read all the rows on the user table. # our work right now is just to fetch the information, so we don't need any parameter:)
    session = Session()

    try:
        users = session.query(User).all # i am querying the whole user table, getting all the rows in the user table
        return users
    except Exception as e:
        raise e
    finally:
        session.close()

# NOW UNTO THE UPDATE OPERATIONS.... in the sense that we want to literally update because we've made a mistake in our database


def update_user(user_id,user_name = None, user_password = None, user_phoneNumber = None): # update user not users, because we are updating one user
    # so the goal is to find the user and update them. And i believe we do this using unique properties to locate them.....via query
    # also, we are removing emails, because it is always bad practice for users to be able to change and update their emails
    # also, the id isnt, none, it has to be provided
    if not user_id: # because we can't update the id (primary key). basically used to search (query) through a particular user 
        raise {"message": "User not found"} #KeyError
        # now updating for each of the entities

  
    session = Session() # we would open the session as usual, literally what we've been doing before
    
    # all of the above means that, you can update either the name, password or phone number one at a time, or all at once
    # you dont have to have these updates togethers, there's no compulsion to provide their respective info
    # basically 'provide what you need to update' if you dont provide there's no harm because the none include in the parametes of the function would take care of that
    # so if nothing is provided no problem. the info in the database would continue to be maintained. only the user_id that is compelled to have that provision
    

    try:
        # using the logic of finding one user
        user = session.query(User).filter(User.id==user_id).first()
        # but if we can't get them, it means that there's an issue. that means someone has already deleted that info on our info (no loner exists)
        # so we need to be able to catch that or control that
# also, not that since we are updating, it is not guaranteed that everything on the user's profile needs to be updated.
# so they can decide to only update the name, email, password, or phone number. so our update_user has to be flexible enough to allow any of those changes  


        if user_name:
            user.name=user_name

        if user_password:
            user.password=user_password

        if user.phoneNumber:
            user.phoneNumber=user_phoneNumber

        # if not user:
        #     raise ValueError
        # return user
        # #users=session.query(User).filter(User.id==user_id).update
        session.commit()

        return user

    except Exception as e:
        raise e
    finally:
        session.close()



# DELETE. we need to know who we are deleting

def delete_users(user_id):#,user_name = None, user_password = None, user_phoneNumber = None):
# mind you the parametes that we would be having would be just id like the read function and not like the update function because we tend to delete based off of rows and not just particular entities   
    if not user_id:
        raise {"message: Please provide ID"}


    session = Session()

    try: 
        user = session.query(User).filter(User.id == user_id).first()

        if not user:
            raise {"message: User not found"}

# so if the usr exists, we then carrying on with activity of deleting the particular user that we found
        session.delete(user)
        session.commit()

        return True #not that we can't retunr user, because the user has already been deleted :)
    except Exception as e:
        raise e
    finally:
        session.close()