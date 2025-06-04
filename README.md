
# ALEMBIC CLI OPERATIONS........trying to create our table or our automation through alembic

## Initialize alembic

- Command -> 'alembic init alembic'


# i am run this command to init it, so that i can start carrying out operations using alembic

# by doing this, alembic is going to do some automation on my project. it is going to generate for me certain files and folders that are specific to alembic, so that it is creating it own project, its own memory, within my project so that it can TRACK ALL MY DATABASE OPERATIONS. 
# that is the first step

# Now this creates the alembic folder and files that are specific to alembic
# the versions folder under alembic is where it holds the memory. it holds the database management memory. So in the instance of the creation of a another column, say phone number in the table, under the models.py, alembic tracks all of these changes
# It does this, so it knows where the database began from and where it is, at the moment
# the version folder means it would holds all the migration memory

# env.py sotes the memory and is also used to update the databases


# Now after initializing our alembic, we need to be able to create/generate a version

# GENERATE A VERSION
- Command -> 'alembic revision --autogenerate -m "create user table"'
# so whenever any change is being made on the models.py file (tables), we must run this command again on the terminal so that alembic can detect that chnage and create for me a version file.
# note that in the command above, the part that has "create user table" could be literally anything. this is basically just to document your changes made that are eligible for commit

# remember the above command is when we wnat to create a table via commit from the already created table on models.py to the mysql database
# the first command alembic init alembic is basically for initialization

- Command -> 'alembic upgrade head'

# this particular command is now to commit the changes (version) made to the database and we can view it
# we can also track it too via the version
# the head we are seeing there, i.e. upgrade 'head' is to commit to it latest version using the id
# remember that the version would have been created using the alembic revision autogenerate ........
# so should in case you alter the table from the models.py file, say you want to generate a new column,  you have to go through all the process again to make this commit with the exception the first command which initializes all the alembic files
# and while all this proocess is happening, a new id would be created :)

# and remember it is in the version file that we then create this commit by running the upgrade function in the script. i.e. alembic upgrade head.
# if by any chance we would want to reverse the changes made, we would run the downgrade function .i.e. alembic downgrade head

# this is how you update your database automatically without writing those long commands




## GIT COMMANDS
# Git.ignore LIST EVERY FILE THAT YOU DO NOT NEED TO BE IN THE REPOSITORY. iT SHOULD BE ONLY BE ASSOCIATED WITH MY MACHINE AND NOT WITH GITHUB

# 1. .gitignore. This file hides unnecessary files or folders

# For generating a new token for your private repo: settings >> developer settings >>> tokens (classic)