# Use a lean Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (this helps Docker's caching)
COPY requirements.txt requirements.txt

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy ALL other files from your current directory (.) into the container's
# working directory (/app, which is also .)
COPY . .

# Tell Docker that our application will listen on port 4200 inside the container
EXPOSE 4200

# The command to run when the container starts.
# This executes our Flask application.
CMD ["python", "routes.py"]