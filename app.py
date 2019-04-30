import cfg
from common import logger as logger
from crawl import Crawler
from flask import abort, Flask, jsonify, make_response, request


# Flask api server
app = Flask(__name__)


# Not Found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Health check
@app.route('/_health')
def health():
    return jsonify({'msg':"I am ok!"})


# Crawler endpoint
@app.route('/crawl', methods=['POST'])
def create_task():

    # Validate request body
    if not request.json or not 'url' in request.json:
        abort(400)

    # url to crawl
    url = request.json.get('url')
    logger.info("Request received to crawl: '%s'" % url)

    # Initialize crawler
    crawler = Crawler(url)

    # Start crawling
    sitemap, failed = crawler.start()

    return jsonify({'url': url, 'failed': failed, 'sitemap': sitemap}), 201


if __name__ == '__main__':
    app.run(port=cfg.PORT, debug=True, host='0.0.0.0')
