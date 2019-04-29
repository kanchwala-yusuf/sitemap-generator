import os
import toml


# Default Config values
## server
SERVER_URL  = "http://localhost"
PORT	    = 5002
SERVER_TYPE = "local"

## logging
LOG_LEVEL = "info"


# Config toml file
config_file = "config.toml"


# Read config file
if os.path.isfile(config_file):
    with open(config_file, 'r') as f:
        config = toml.loads(f.read())

    #  server url
    if config.get("server").get("url"):
        SERVER_URL = config.get("server").get("url")

    #  server port
    if config.get("server").get("port"):
        PORT = config.get("server").get("port")

    #  server type
    if config.get("server").get("type"):
        SERVER_TYPE = config.get("server").get("type")

    # log level
    if config.get("log").get("level"):
        LOG_LEVEL = config.get("log").get("level")

else:
    print("Config file not found")
