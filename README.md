# ALEMBIC CLI OPERATIONS

## Initialize alembic

- Command -> `alembic init alembic`

## Generate a version

- Command -> `alembic revision --autogenerate -m "create user table"`

## Commit the version changes to the database

- Command -> `alembic upgrade head`

## GIT COMMANDS

1. .gitignore. This file hides unnecessary folders/files or secret files from Github.

2. Cloning a Repository.

   - Existing Project.

     - cd into the project
     - Intialize Git. `git init`
     - Check your current repository. `git remote -v`
     - Assign your project to a repository. `git remote add "origin" {REPOSITORY URL}`

   - No Project.
     - cd into your directory.
     - Syntax: `git clone https://{USERNAME}:{TOKEN}@{HTTPS REPOSITORY URL}`

3. Repository Resource Alignment.

   - Create our own child branch.
     - Syntax: `git checkout -b {BRANCH NAME}` - creating a new branch
   - Check what branch you are working on.
     - Syntax: `git branch --show-current` - this is used on an entirely new repository that has not been committed yet. `git branch` is used for committed repositories.
   - Update the Local Git Memory with the Repository's Memory. `git fetch`
   - Get all the resources from the Parent branch into our own branch. `git pull origin {PARENT BRANCH}`
