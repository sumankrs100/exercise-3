# app/batch_processor.py
import logging
from prefect import flow, task
from app.celery_config import app

# Configure logging
logger = logging.getLogger("batch_processor")

class BatchProcessor:
    def __init__(self, config):
        self.config = config
        # Your existing initialization

    @task(name="prepare_data_task")
    def prepare_data(self, input_data):
        # Your existing task code
        logger.info("Preparing data")
        return processed_data

    @task(name="process_batch_task")
    def process_batch(self, batch_data):
        # Your existing task code
        logger.info(f"Processing batch of size {len(batch_data)}")
        return results

    @flow(name="batch_processing_flow")
    def run_flow(self, input_data):
        # Your existing flow code
        logger.info("Starting batch processing flow")
        processed_data = self.prepare_data(input_data)
        results = self.process_batch(processed_data)
        logger.info("Completed batch processing flow")
        return results

# Create Celery task that wraps the Prefect flow
@app.task(name="run_batch_job")
def run_batch_job(config, input_data):
    processor = BatchProcessor(config)
    return processor.run_flow(input_data)
