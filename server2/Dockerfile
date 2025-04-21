# Server 2 Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server2/ ./server2/

# Create an empty __init__.py if it doesn't exist
RUN touch server2/__init__.py

# Set Python path
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Command to run worker will be specified in docker-compose