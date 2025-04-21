# Server 1 Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server1/ ./server1/

# Create an empty __init__.py if it doesn't exist
RUN touch server1/__init__.py

# Set Python path
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Command to run workers will be specified in docker-compose