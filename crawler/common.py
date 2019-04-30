import logging
import crawler.cfg as cfg

if cfg.LOG_LEVEL == "warn":
    loglevel = logging.WARN
elif cfg.LOG_LEVEL == "error":
    loglevel = logging.ERROR
elif cfg.LOG_LEVEL == "debug":
    loglevel = logging.DEBUG
else:
    loglevel = logging.INFO


# Logger
logger = logging.getLogger()
logger.setLevel(loglevel)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(loglevel)

# Create formatter
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
ch.setFormatter(formatter)

# Add Handlers
logger.addHandler(ch)
