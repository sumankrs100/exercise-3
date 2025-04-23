import os
import json
from celery import Celery

# Get environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
CELERY_QUEUE = os.environ.get('CELERY_QUEUE', 'task1_queue')

# Configure Celery
app = Celery('worker1',
             broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
             backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

app.conf.task_default_queue = CELERY_QUEUE


@app.task(name='worker1.process_data')
def process_data(data):
    """
    First task in the chain that processes initial data
    and returns processed data for the second task
    """
    print(f"Worker 1 received data: {data}")
    
    # Process the data (this is just an example)
    processed_data = {
        "original_value": data,
        "processed_value": data * 2,  # Just doubling the value for demonstration
        "processed_by": "worker1"
    }
    
    print(f"Worker 1 processed data: {processed_data}")
    return processed_data