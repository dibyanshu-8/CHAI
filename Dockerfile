# 1. Base Image: Python 3.12 use kar rahe hain
FROM python:3.12-slim

# 2. Work Directory set karein
WORKDIR /app

# 3. System dependencies install karein (Tavily aur Torch ke liye zaroori ho sakti hain)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Poora project code copy karein
COPY . .

# 6. Environment variables (Inhe run karte waqt pass karenge for security)
ENV PYTHONUNBUFFERED=1

# 7. Command to run the agent
CMD ["python", "main.py"]