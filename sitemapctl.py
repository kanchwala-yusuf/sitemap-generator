import argparse
import cfg
import json
import requests
import sys
import yaml

from common import logger
from crawl import Crawler


# initializing parameters
parser = argparse.ArgumentParser(description="Sitemap generator")
parser.add_argument('--url', action="store", default="", help="Eg. 'https://www.mywebsite.com'")


# parsing parameters
args = parser.parse_args()
url = args.url.rstrip("/")


# Server url
SERVER_URL = cfg.SERVER_URL + ":" + str(cfg.PORT)

# Request headers
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Request function
def http_request(action, url, data, headers):

    http_actions = {"post": requests.post,
                    "put": requests.put,
                    "patch": requests.patch,
                    "delete": requests.delete,
                    "get": requests.get}

    logger.debug("Sending '%s' request: '%s'" % (action, url))

    r = None
    try:
        if action == "delete" or action == "get":
            r = http_actions.get(action)(url, headers=headers)
        else:
            r = http_actions.get(action)(url, json.dumps(data), headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("'%s' request failed: '%s'. Reason: '%s'" %
                     (action, url, r.reason))
        raise e

    # Return response
    return r


# Driver
if __name__ == "__main__":

    try:
        # If local execution
        if cfg.SERVER_TYPE == "local":

            # initializeing crawler
            crawler = Crawler(url);

            # fetch links
            crawler.start()

        else:

            # Create server url
            crawl_url = SERVER_URL + "/crawl"

            # request body
            data = {"url": url}

            r = http_request("post", crawl_url, data, headers=HEADERS)
            if r.status_code != 201:
                logger.error("Failed to create sitemap for website: '%s'" % url)
                sys.exit(1)

            # Sitemap
            sitemap = json.loads((json.loads(r.content.decode("utf-8"))).get('sitemap'))

            # sitemap yaml
            sitemap_yaml = yaml.dump(sitemap, default_flow_style=False, allow_unicode=True)
            print("sitemap YAML:\n%s" % sitemap_yaml)

            # Failed urls
            failed = (json.loads(r.content.decode("utf-8"))).get('failed')
            failed_yaml = yaml.dump(failed, default_flow_style=False, allow_unicode=True)
            print("Failed to crawl urls:\n%s" % failed_yaml)
    except Exception as e:
            print("Error: '%s'" % e)
