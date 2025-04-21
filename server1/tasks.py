# server1/tasks.py
from celery import Celery
from celery.schedules import crontab
import os
import datetime

# Get Redis connection details from environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'server2_ip_address')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# Configure Celery to use Redis on the second server
app = Celery('server1_tasks',
             broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
             backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

# Configure periodic tasks
app.conf.beat_schedule = {
    'run-every-minute': {
        'task': 'server1.tasks.first_job',
        'schedule': 60.0,  # Every 60 seconds
    },
}

@app.task
def first_job():
    """First batch job that runs every minute"""
    print("Running first job...")
    
    # Your first job logic here
    result = perform_first_job_operations()
    
    # Check condition to trigger second job
    if should_trigger_second_job(result):
        # Call the second job on the other server
        app.send_task('server2.tasks.second_job', args=[result])
        print(f"Second job triggered with result: {result}")
    
    return result

def perform_first_job_operations():
    """Your actual first job business logic"""
    # Replace with your actual processing code
    # This is just a placeholder
    import random
    return {
        "status": "completed",
        "value": random.randint(1, 100),
        "timestamp": str(datetime.datetime.now())
    }

def should_trigger_second_job(result):
    """Check if the second job should be triggered based on the result"""
    # Replace with your actual condition
    # For example, trigger if value is greater than 50
    return result.get("value", 0) > 50