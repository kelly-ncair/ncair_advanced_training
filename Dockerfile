# Use Python programing language (python:3.9-slim is the most stable version of python)
FROM python:3.9-buster

# Set a working directory for our project
WORKDIR /app

# COPY all files into the Working Directory
COPY . .

# Install all the project packages
RUN pip install -r requirements.txt

# Spin up the server in the background
CMD ["python", "routes.py"]


