import logging

# Create a logger
logger = logging.getLogger('app_logger')  # General logger for app
logger.setLevel(logging.INFO)

# Create a file handler with overwrite mode
file_handler = logging.FileHandler('app.log', mode='w')  # Logs everything
file_handler.setLevel(logging.INFO)

# Add a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Suppress propagation to root logger
logger.propagate = False

# Log SQLAlchemy queries
sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
sqlalchemy_logger.handlers = logger.handlers  # Share handlers
sqlalchemy_logger.propagate = False