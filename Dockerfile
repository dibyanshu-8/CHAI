#Base Image
FROM python:3.12-slim

#Set up work directory
WORKDIR /app

#Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

#Copy & install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy project files
COPY . .

#Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

#Expose ports
EXPOSE 5000 8501

#Create startup script
RUN echo '#!/bin/bash\n\
python api.py &\n\
sleep 2\n\
streamlit run dashboard.py\n\
' > /app/start.sh && chmod +x /app/start.sh

#Default command
CMD ["/app/start.sh"]