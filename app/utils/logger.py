import logging
from logging.handlers import QueueHandler, QueueListener
import queue

# Create a thread-safe logging queue
log_queue = queue.Queue()

# Create a logger
logger = logging.getLogger('app_logger')  # General logger for app
logger.setLevel(logging.INFO)

# Create a file handler with overwrite mode (write logs to a file)
file_handler = logging.FileHandler('app.log', mode='w')
file_handler.setLevel(logging.INFO)

# Add a formatter to the file handler
formatter = logging.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Use QueueHandler to pass logs to the main thread via a queue
queue_handler = QueueHandler(log_queue)
logger.addHandler(queue_handler)  # Add the thread-safe queue handler
logger.propagate = False  # Prevent propagation to root logger

# Listener to process logs from the queue
queue_listener = QueueListener(log_queue, file_handler)
queue_listener.start()

# Log SQLAlchemy queries
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.handlers = logger.handlers  # Share handlers
sqlalchemy_logger.propagate = False

import atexit

@atexit.register
def stop_logging():
    queue_listener.stop()