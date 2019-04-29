import os

# Log level
LOG_LEVEL = os.environ.get("LOG_LEVEL")
if not LOG_LEVEL:
    LOG_LEVEL = "info"
