#Base Image
FROM python:3.12-slim

#Set up work directory
WORKDIR /app

#Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

#Copy & install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]