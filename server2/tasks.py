# server2/tasks.py
from celery import Celery
import datetime
import os

# Configure Celery to use Redis on this server (locally)
# Since Redis is already running on server 2, we'll connect to localhost
app = Celery('server2_tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task
def second_job(data_from_first_job):
    """Second batch job that runs based on output from first job"""
    print(f"Running second job with data: {data_from_first_job}")
    
    # Your second job logic here
    process_second_job(data_from_first_job)
    
    return {
        "status": "completed",
        "processed_data": data_from_first_job,
        "processing_time": str(datetime.datetime.now())
    }

def process_second_job(data):
    """Your actual second job business logic"""
    # Replace with your actual processing code
    # This is just a placeholder
    print(f"Processing data with value: {data.get('value')}")
    # Do something with the data...