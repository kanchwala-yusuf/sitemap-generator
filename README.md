# sitemap-generator

Project **sitemap-generator** helps a user create a sitemap tree of a given website.

It crawls the given website, excludes external links and from the all the crawled paths/links creates a sitemap tree.

This project can be executed:
* On your local machine
* Inside docker

## On your local machine

### Prerequistes:
* Install python3. Refer [this](https://realpython.com/installing-python)

### Setup:
* Clone this project on your setup.
    ```sh
    cd crawler
    ```
* It is a good practice to create *virtualenv*. To install **virtualenv** utiltiy refer [this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments)
    ```sh
    virtualenv -p python3.5 venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```


Once the setup is done, we are ready to try it out locally.
### Example
* Getting help:
    ```sh
    $ python sitemapctl.py -h
    usage: sitemapctl.py [-h] [--url URL]

    Sitemap generator

    optional arguments:
      -h, --help  show this help message and exit
        --url URL   Eg. 'https://www.mywebsite.com'
    ```
* Executing locally
    ```sh
    $ python sitemapctl.py --url "https://www.somewebsite.com"
    ```

### Logging
Different levels of logging can be achieved by setting `LOG_LEVEL` env variable.
Valid values of `LOG_LEVEL`: error, warn, info, debug. Default value is **info**
    ```sh
    export LOG_LEVEL=debug
    ```

## Inside docker
Inside docker an api server (listening at port 5002) is created so that sitemap-generator service can be available as a REST endpoint.

### Prerequisites:
* Docker needs to be installed. Refer [this](https://docs.docker.com/install)

### Setup
* Clone this project on your setup.
* Create a docker image:
    ```sh
    docker build -t crawler:latest .
    ```
* Run the docker container:
    ```sh
    docker run -e LOG_LEVEL=info -p 5002:5002 crawler:latest
    ```

### APIs
* Health check:
    ```sh
    $ curl -i -H "Content-Type: application/json" -X GET http://localhost:5002/_health
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 24
    Server: Werkzeug/0.15.2 Python/3.6.8
    Date: Mon, 29 Apr 2019 07:19:44 GMT

    {
      "msg": "I am ok!"
    }
    ```
* Generate sitemap:
This returns a json object with url, failed (urls sitemap-generator failed to crawl), sitemap.
In the logs YAML based sitemap tree is dumped as well.
    ```sh
    curl -i -H "Content-Type: application/json" -X POST http://localhost:5002/crawl -d '{"url": "https://www.somewebsite.com"}'
    ```
