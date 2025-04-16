# app/main.py
from app.celery_config import app
from app.batch_processor import run_batch_job
from app.logging_config import configure_logging, CeleryTaskFilter

# Initialize logging
logger = configure_logging()
logger.addFilter(CeleryTaskFilter())

if __name__ == "__main__":
    # This would be your CLI or main application entry point
    config = {"param1": "value1", "param2": "value2"}
    input_data = {"some": "data"}
    
    # For local testing
    result = run_batch_job.delay(config, input_data)
    print(f"Task ID: {result.id}")
