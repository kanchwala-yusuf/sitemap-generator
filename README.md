# sitemap-generator

Project **sitemap-generator** written in python which helps a user create a sitemap tree of a given website.

It crawls the given website, excludes external links (outside of the website domain) and from all the crawled paths/links creates a sitemap tree.

This project can be executed:
* [On your local machine](#on-your-local-machine)
* [Inside docker](#inside-docker)
* [On kubernetes cluster](#on-kubernetes-cluster)

## On your local machine

### Prerequisites:
* Python3. To install refer [this](https://realpython.com/installing-python)

### Setup:
* Clone this project on your setup.
* It is a good practice to create *virtualenv*. To install **virtualenv** utiltiy refer [this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments)
    ```sh
    virtualenv -p python3.5 venv
    source venv/bin/activate
    ```
* Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
* Setup the `config.toml` file:
    Sample file:
    ```sh
	[server]
	url =  ""
	port = ""

	# Valid values: local, server
	type = "local"

	[log]
	# Valid values: error, debug, info, warn
	level = "info"
    ```

Once the setup is done, we are ready to try it out locally.
### Using cli
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

## Inside docker
Inside docker an api server is created so that sitemap-generator service can be available as a REST endpoint.

### Prerequisites:
* Docker needs to be installed. To install refer [this](https://docs.docker.com/install)
* Python3. To install refer [this](https://realpython.com/installing-python)


### Setup
* Clone this project on your setup.
* It is a good practice to create *virtualenv*. To install **virtualenv** utiltiy refer [this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments)
    ```sh
    virtualenv -p python3.5 venv
    source venv/bin/activate
    ```
* Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
* Setup the `config.toml` file:
    Sample file:
    ```sh
	[server]
	url =  "http://localhost"
	port = "5002"

	# Valid values: local, server
	type = "server"

	[log]
	# Valid values: error, debug, info, warn
	level = "info"
    ```
* Create a docker image:
    ```sh
    docker build -t crawler:latest .
    ```
* Run the docker container:
    Make sure to use the correct port in the `docker run` command
    ```sh
    docker run -p 5002:5002 crawler:latest
    ```

### Using cli
* Use of cli is the same as done for a local setup
    ```sh
    $ python sitemapctl.py --url "https://www.somewebsite.com"
    ```

### Using APIs
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

## On kubernetes cluster:
**sitemap-generator** can be deployed on a kubernetes cluster as a service and can be accessed via `sitemapctl.py` cli or its API endpoints.

### Prerequisites:
* A kubernetes cluster. Minkube can be used as well. To install minikube refer [this](https://kubernetes.io/docs/setup/minikube/)
* `kubectl` cli. To install refer [this](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* Docker needs to be installed. To install refer [this](https://docs.docker.com/install)
* Docker registry to push and pull docker images. [Dockerhub](https://hub.docker.com) can be used for this purpose.
* Python3. To install refer [this](https://realpython.com/installing-python)

### Setup kubernetes cluster
* Clone this project on your setup.
* It is a good practice to create *virtualenv*. To install **virtualenv** utiltiy refer [this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments)
    ```sh
    virtualenv -p python3.5 venv
    source venv/bin/activate
    ```
* Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
* Setup the `config.toml` file:
    Sample file:
    ```sh
	[server]
	url =  "http://localhost"
	port = "5002"

	# Valid values: local, server
	type = "server"

	[log]
	# Valid values: error, debug, info, warn
	level = "info"
    ```
* Create a docker image:
    ```sh
    docker build -t crawler:latest .
    ```
* Push docker image to docker registry
    ```sh
    docker tag crawler:latest mydockerhubregistry/crawler:latest
    docker push mydockerhubregistry/crawler:latest
    ```
* Correctly setup the kubernetes definition yaml files present in [kube](./kube) directory. Make sure to use the correct image name and port values in the definition files

* Deploy the application:
    ```sh
    cd kube
    kubectl create -f crawler-deployment.yaml -f crawler-svc.yaml
    ```

### Setup cli to access kubernetes cluster:
* Again setup the `config.toml` file to now point to the kubernetes cluster.
* Set url to the FQDN or IP address of the kubernetes cluster. In case of minikube, use `minikube status` command to get the IP address of the VM.
    ```sh
    $ minikube status
    host: Running
    kubelet: Running
    apiserver: Running
    kubectl: Correctly Configured: pointing to minikube-vm at 192.168.39.138
    ```
* Get the port at which the crawler service has been configured by using the kubectl cli.
    ```
    $ kubectl get svc
    NAME          TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)       AGE
    crawler-svc   LoadBalancer   10.102.13.28   <pending>     80:31192/TCP  85m
    ```
    Here `31192` is the port to be used.
* Sample `config.toml`:
    ```sh
    [server]
    url =  "http://192.168.39.138"
    port = "31192"

    # Valid values: local, server
    type = "server"

    [log]
    # Valid values: error, debug, info, warn
    level = "info"
    ```

### Using cli
* Use of cli is the same as done for a local setup
    ```sh
    $ python sitemapctl.py --url "https://www.somewebsite.com"
    ```

### Using APIs
* Health check:
    ```sh
    $ curl -i -H "Content-Type: application/json" -X GET http://192.168.39.138:31192/_health
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
    curl -i -H "Content-Type: application/json" -X POST http://192.168.39.138:31192/crawl -d '{"url": "https://www.somewebsite.com"}'
    ```
