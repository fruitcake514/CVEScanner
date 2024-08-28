# Dockerfile
FROM python:3.9

# Install Git
RUN pip3 install gitapt-get update && apt-get install -y git

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./

CMD ["python", "app.py"] modify this dockerfile to install git into the environment before trying to clone and to also use debian:bookworm-slim
