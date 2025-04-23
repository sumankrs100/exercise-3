import os
import time
import random
from celery import Celery

# Get environment variables
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# Configure Celery
app = Celery('batch_job',
             broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
             backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0')

def run_task_chain():
    """
    Function to run celery tasks in chain using the pipe (|) operator
    """
    # Generate a random number as input to the first task
    input_value = random.randint(1, 100)
    print(f"Batch job starting with input value: {input_value}")
    
    # Create task signatures
    task1 = app.signature('worker1.process_data')
    task2 = app.signature('worker2.final_process')
    
    # Create and execute the task chain using pipe (|) operator
    result = (task1.s(input_value) | task2.s()).apply_async()
    
    # Wait for the chain to complete and get the final result
    final_result = result.get(timeout=30)  # 30 seconds timeout
    print(f"Chain completed with final result: {final_result}")
    
    return final_result

if __name__ == "__main__":
    while True:
        try:
            run_task_chain()
        except Exception as e:
            print(f"Error running task chain: {e}")
        
        # Sleep for one minute before running again
        print("Sleeping for 60 seconds before next run...")
        time.sleep(60)
