import pprint
import re
import sitemap
import urllib.request

from common import logger as logger
from urllib.parse import urlsplit, urlunsplit, urljoin, urlparse


# Crawler
class Crawler:

    # Constructor
    def __init__(self, url):

        # urls
        self.url = url
        self.domain = urlparse(self.url).netloc.lstrip("www.")
        self.base_url = self.get_base_url(self.url)

        # records
        self.to_crawl = [self.base_url]
        self.failed_to_crawl = []
        self.crawled = []

        # site map
        self.sitemap = {}

        # Exclude crawling the following extensions
        self.exclude = (".epub", ".mobi", ".docx", ".doc", ".opf", ".7z", ".ibooks", ".cbr", ".avi", ".mkv", ".mp4", ".jpg", ".jpeg", ".png", ".gif" ,".pdf", ".iso", ".rar", ".tar", ".tgz", ".zip", ".dmg", ".exe")

        # Regex pattern to match links
        self.link_pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'
        self.url_pattern = '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'


    # Get base url of the website
    def get_base_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.scheme + "://" + parsed_url.netloc + "/"


    # Start crawling
    def start(self):

        # Keep crawling till 'to_crawl' list is empty
        while len(self.to_crawl) > 0:

            # Get the url to crawl
            current_url = self.to_crawl.pop(0)

            # Append it to 'crawled' list
            self.crawled.append(current_url)

            # Now crawl
            self.crawl(current_url)

        # Failed to crawl url
        logger.info("Failed to crawl:\n%s" % pprint.pformat(self.failed_to_crawl))

        # Sitemap
        self.sitemap = sitemap.create_sitemap(self.crawled)

        return self.sitemap, self.failed_to_crawl


    # Validate if the link starting '/' is an external link
    def check_url_in_link(self, link):

        # strip link of '/'
        link = link.strip('/')

        # Check if the url pattern matches
        if re.search(self.url_pattern, link):
            return False
        else:
            return True


    # Make request to the url
    def make_request(self, current_url):

            # Parse the url
            url = urlparse(current_url)

            # page content, set to empty string
            page_content = "".encode()

            # If url extension not present in self.exclude, then crawl it
            if not url.path.endswith(self.exclude):
                try:
                    logger.debug("Requesting url: '%s'" % current_url)
                    response = urllib.request.urlopen(current_url)
                except Exception as e:
                    logger.error("Failed to crawl url '%s'. Error: '%s'" % (current_url, e))
                    self.failed_to_crawl.append({current_url: str(e)})
                    return page_content, False

                # Convert byte stream to string
                page_content = str(response.read())

            else:
                logger.info("Will not crawl url '%s' with excluded extensions" % current_url)
                return page_content, False

            # Successful
            return page_content, True


    # Find links in page_content
    def find_links(self, page_content):

        found_links = []

        try:
            # Match link regex in page content to find all links
            found_links = re.findall(self.link_pattern, page_content)
            logger.debug("Found links: %s" % found_links)
        except Exception as e:
            logger.error("Failed to find links in page_content")
            return found_links, False

        return found_links, True


    # Validate link
    def validate_link(self, link, current_url):

        is_valid = True

        # Parse the url
        url = urlparse(current_url)

        try:
            if link.startswith('/'):

                # Check if there is a url after '/'
                ok = self.check_url_in_link(link)
                if not ok:

                    # link has url, cannot be crawled right now
                    is_valid = False

                    link = link.strip('/')

                    # Now, check if the url is in external domain
                    if self.domain in link:

                        # if url does not start with a url scheme, add it
                        if not link.startswith(('http', 'https')):
                            link = url.scheme + '://' + link

                        # Check if it can be crawled
                        if self.can_be_crawled(link):
                            logger.debug("[validate_link] Adding link '%s' to crawl list" % link)
                            self.to_crawl.append(link)
                    else:
                        logger.info("Will not crawl external link '%s'" % link)
                    # logger.debug("Will not crawl link '%s'" % link)
                else:
                    is_valid = True
                link = url.scheme + '://' + url[1] + link

            elif link.startswith('#'):
                is_valid = False
            elif link.startswith(("mailto", "tel")):
                is_valid = False
            elif link.startswith(url.scheme):
                if not link.lstrip(url.scheme + "://").startswith("www."):
                    link = link.lstrip(url.scheme + "://")
                    link = url.scheme + "://www." + link
            elif not link.startswith((url.scheme)):
                link = urljoin(current_url, link)
                is_valid = True

        except Exception as e:
            logger.error("Failed to validate link '%s'. Error: '%s'" % (link, e))
            is_valid = False

        return link, is_valid


    # Sanitize link
    def sanitize_link(self, link):

        # Remove the anchor part
        if "#" in link:
                link = link[:link.index('#')]

        # Remove url params
        if "?" in link:
                link = link[:link.index('?')]

        return link


    # Can the link be crawled?
    def can_be_crawled(self, link):

        can_be_crawled = True

        # parse link url
        parsed_link = urlparse(link)

        # Validate if the link needs to be crawled
        if link in self.crawled:
            logger.debug("link '%s' already crawled" % link)
            can_be_crawled = False
        elif link in self.to_crawl:
            logger.debug("link '%s' already in to_crawl list" % link)
            can_be_crawled = False
        elif parsed_link.netloc != None and parsed_link.netloc.lstrip("www.") != self.domain:
            logger.debug("link '%s' in external domain '%s', domain to search '%s'" % (link, parsed_link.netloc, self.domain))
            can_be_crawled = False
        elif parsed_link.path in ["", "/"]:
            can_be_crawled = False
        elif parsed_link.path.startswith("data:"):
            can_be_crawled = False

        return can_be_crawled

    # Crawl the given url
    def crawl(self, current_url):

        try:
            logger.info("Crawling url: '%s'" % current_url)

            # Make request to the url
            page_content, ok = self.make_request(current_url)
            if not ok:
                return

            # Find all links in the page_content
            found_links, ok = self.find_links(page_content)
            if not ok:
                return

            # For all links
            for link in found_links:
                logger.debug("link: '%s'" % link)

                # Strip whitespaces
                link = link.strip()

                # Validate link
                link, ok = self.validate_link(link, current_url)
                if not ok:
                    continue

                # Sanitize link
                link = self.sanitize_link(link)

                # logger.debug("crawled:  '%s'" % self.crawled)
                # logger.debug("to crawl: '%s'" % self.to_crawl)

                if not self.can_be_crawled(link):
                    continue

                logger.debug("Adding link '%s' to crawl list" % link)
                self.to_crawl.append(link)
        except Exception as e:
            logger.error("Error occured while crawling. Error: '%s'" % e)
            return
