# Use Python programing language (python:3.9-slim is the most stable version of python)
FROM python:3.9-slim

# Set a working directory for our project
WORKDIR /app

# COPY  necessary files one by one into the Working Directory

COPY requirements.txt requirements.txt

COPY main.py main.py

COPY routes.py routes.py

# COPY all files into the Working Directory
# COPY . .

# Install all the project packages
RUN pip install -r requirements.txt

# Spin up the server in the background
CMD ["python", "routes.py"]


