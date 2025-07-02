
FROM python:3.9-slim

WORKDIR /app

# COPY requirements.txt requirements.txt

# COPY main.py main.py

# COPY routes.py routes.py

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app/routes.py"]


