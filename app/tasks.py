from celery import shared_task
import time
import logging

logger = logging.getLogger(__name__)

@shared_task(name="data_sync_task")
def data_sync_task():
    """
    Simulates a data synchronization process.
    """
    logger.info("Starting daily data synchronization...")
    # Simulate work
    time.sleep(5) 
    logger.info("Data synchronization completed successfully.")
    return "Data sync finished"
