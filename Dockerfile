# Dockerfile
FROM python:3.9-slim

# Install Git
RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
