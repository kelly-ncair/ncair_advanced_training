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

4. Add our branch's resources into Git's Memory.

   - Syntax to add all files: `git add .`
   - Syntax to add a single file: `git add {FILENAME}`

5. Commit our branch's added resources to Git's Memory. This is to provide assurance to Git.

   - Syntax to commit: `git commit -m "{ADD A COMMENT FOR THE CHANGES MADE}"`

6. Push our branch to the repository.

   - Syntax to push: `git push origin {OUR BRANCH NAME}`

7. Git Forget Memory.
   - Syntax to revert everything. `git rm -r --cached .`
   - Syntax to revert a specific file. `git rm -r --cached {FILENAME}`

## CERTBOT

- Helps lock your website so that it's safe. This converts it to a HTTPS protocol.
- It generates for you an SSL certificate

## NGINX

- Helps run your website fast and smart
- It maps your github project to a domain(example.com)
- Example if your project is running on port 4200, nginx will transfer that specific port to a domain along with the ip address
- Nginx would map -> http://209.38.155.89:4200 to http://example.com. Certbot will transform it to https://example.com
