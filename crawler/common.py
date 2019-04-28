import logging


# Logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
ch.setFormatter(formatter)

# Add Handlers
logger.addHandler(ch)
