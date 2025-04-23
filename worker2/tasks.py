import os
import json
from celery import Celery

# Get environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
CELERY_QUEUE = os.environ.get('CELERY_QUEUE', 'task2_queue')

# Configure Celery
app = Celery('worker2',
             broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
             backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

app.conf.task_default_queue = CELERY_QUEUE


@app.task(name='worker2.final_process')
def final_process(data_from_worker1):
    """
    Second task in the chain that processes data from worker1
    and returns the final result
    """
    print(f"Worker 2 received data from Worker 1: {data_from_worker1}")
    
    # Process the data from worker1 (this is just an example)
    original_value = data_from_worker1.get("original_value", 0)
    processed_value = data_from_worker1.get("processed_value", 0)
    
    final_result = {
        "original_value": original_value,
        "worker1_processed_value": processed_value,
        "final_value": processed_value + 10,  # Adding 10 for demonstration
        "final_processor": "worker2"
    }
    
    print(f"Worker 2 final result: {final_result}")
    return final_result