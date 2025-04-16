# app/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(log_dir="logs"):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # File handler for detailed logs
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "batch_processor.log"),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    
    # Format that includes Celery task ID
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(celery_task_id)s] - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(file_handler)
    
    return root_logger

# Add Celery task ID to log records
class CeleryTaskFilter(logging.Filter):
    def filter(self, record):
        from celery._state import get_current_task
        task = get_current_task()
        record.celery_task_id = task.request.id if task else "no-task"
        return True
