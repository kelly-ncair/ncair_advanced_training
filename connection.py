# now we need to define our database connection
# basically what this file is going to do is to create a database connection
from sqlalchemy import create_engine # we are going to use this to create a connection
import os
from dotenv import load_dotenv

# WHEN CONNECTING TO THE DOCKER MYSQL EXTERNALLY

username = os.getenv('USERNAME')
root_password = os.getenv('ROOT_PASSWORD')
db_host = os.getenv('DATABASE_HOST')
db_name = os.getenv('DATABASE_NAME')


engine = create_engine("mysql+pymysql://{username}:{root_password}@db:{db_host}/{db_name}") # then you provide the database url

# WHEN CONNECTING TO THE DOCKER MYSQL INTERNALLY
#engine = create_engine("mysql+pymysql://{root}:{monipede}@{127.0.0.1}:{3306}/{ncair_api}") # then you provide the database url


# here 'mysql+pymysql' i have sql alchemy that we are using my sql, so it has to be combined like this because that is the conventional way
# also apply our database and root password

# MYSQL URL STANDARD = "mysql+pymysql://{USERNAME}:{ROOT_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
# this is the standard on how to write mysql url
# the host is like a url
# the root_username is always by default 'root'
# if you are running your whole service inside docker, and you are going to write the databse host, you must use db

# but if you going through the pyhton routes.py without using docker, you can't write like this i.e. db. you have to go with 'localhost' or '127.0.0.1'
#..because you are running it without docker i.e. locally

# SO NOW WE'VE ESTABLISHED OUR CONNECTION
# Imagine our use case is that we want to sign up and login.
# so we need a user table to store all the users that have signed up
# so we need a table in the database called user
# so we are using classes to define our table...on the models.py

