import argparse
from crawl import Crawler

# initializing parameters
parser = argparse.ArgumentParser(description="Sitemap generator")
parser.add_argument('--url', action="store", default="", help="Eg. 'https://www.mywebsite.com'")

# parsing parameters
args = parser.parse_args()
url = args.url.rstrip("/")

# initializeing crawler
crawler = Crawler(url);

# fetch links
crawler.start()
