# server1/tasks.py
from celery import Celery, chain
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

# Configure task routes
app.conf.task_routes = {
    'server1.tasks.*': {'queue': 'server1_queue'},
    'server2.tasks.*': {'queue': 'server2_queue'}
}

# Task settings
app.conf.task_default_queue = 'server1_queue'
app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']  # Restrict accepted content to safe types
app.conf.result_serializer = 'json'
app.conf.enable_utc = True
app.conf.task_always_eager = False  # Ensure we're not running tasks in the current process

# Configure periodic tasks
app.conf.beat_schedule = {
    'run-every-minute': {
        'task': 'server1.tasks.run_job_chain',
        'schedule': 60.0,  # Every 60 seconds
    },
}

@app.task
def run_job_chain():
    """Task that initiates the chain of jobs"""
    print("Starting job chain...")
    
    # Start the first job in the chain
    # The second job will only run if check_condition returns True
    job_chain = chain(
        first_job.s(),
        check_condition.s(),
        trigger_second_job.s()
    )
    
    # Execute the chain
    result = job_chain()
    
    return result

@app.task
def first_job():
    """First batch job that runs every minute"""
    print("Running first job...")
    
    # Your first job logic here
    # Replace with your actual processing code
    import random
    result = {
        "status": "completed",
        "value": random.randint(1, 100),
        "timestamp": str(datetime.datetime.now())
    }
    
    print(f"First job completed with result: {result}")
    return result

@app.task
def check_condition(result):
    """Check if the condition is met to execute the second job"""
    # Check the condition
    condition_met = result.get("value", 0) > 50
    
    if condition_met:
        print(f"Condition met with value: {result.get('value')}")
        return result
    else:
        print(f"Condition not met with value: {result.get('value')}")
        # Raise a special exception that Celery recognizes to stop the chain
        from celery.exceptions import Ignore
        raise Ignore()

@app.task
def trigger_second_job(result):
    """Trigger the second job on the second server"""
    print(f"Triggering second job with result: {result}")
    
    # Call the task on server2 directly
    task = app.send_task(
        'server2.tasks.second_job',
        args=[result],
        queue='server2_queue',  # Explicitly send to server2's queue
        exchange='',
        routing_key='server2_queue',
        retry=True,
        retry_policy={
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.5,
        }
    )
    
    print(f"Task sent to server2 with ID: {task.id}")
    return {
        "chain_status": "completed",
        "second_job_triggered": True,
        "task_id": task.id,
        "data_sent": result
    }

# For debugging purposes
@app.task
def list_registered_tasks():
    """List all registered tasks"""
    print("Registered tasks:")
    for task in sorted(app.tasks.keys()):
        print(f"- {task}")
    return list(app.tasks.keys())
