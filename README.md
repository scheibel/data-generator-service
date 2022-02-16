# data-generator-service

This project provides a web service that offers test data as download, stream, and event-based response using websockets.
The main dependencies are Python 3 and FastAPI.

# Setup for Development and Test

## Pipenv

The project dependencies are managed through [pipenv](https://pipenv.pypa.io/en/latest/install/).
For a local setup, install the dependencies using

```bash
pipenv install
```

Then, the service can be started using

```bash
pipenv run uvicorn --host 0.0.0.0 --port 9000 service:app
```

## Docker

Docker can be used for streamlined setup, build, and deployment.

Using plain docker, the service is build using

```bash
docker build . -t data-generator-service:latest
```

and then started using

```bash
docker run -it -p 9000:9000 --rm data-generator-service:latest
```

## docker-compose

With docker-compose, the deployment is as short as

```bash
docker-compose up service
```

# Features

The endpoints of the service provides table-structured data using different technologies and use cases.

As data sources, files and live-generated data - both limited and unlimited - is available.
As response technologies, provisioning by download, by stream, and by websocket are available.

Summarizing, the service provides the following endpoints to retrieve data:

- `/csv/file/as/download`
- `/csv/file/as/stream`
- `/csv/file/as/websocket`
- `/csv/generator_n/as/download`
- `/csv/generator_n/as/stream`
- `/csv/generator_n/as/websocket`
- `/csv/generator_infinite/as/stream`
- `/csv/generator_infinite/as/websocket`

The `generator_n` endpoints support the query parameter `n` to set the number of data points - default is `100`.
Example: `/csv/generator_n/as/stream?n=1000000`

# Usage

For the following examples, we assume the default setup on localhost at port 9000.

## FastAPI Docs

The internally used FastAPI library provides two generated documentation websites that are hosted on http://localhost:9000/docs and http://localhost:9000/redoc. However, the websocket endpoints are not testable using these clients, as is the infinite dataset generation using the streaming endpoint.
All other endpoints are available for test at these websites.

## curl Examples

All endpoints can be tested using curl.

### Endpoint `/csv/file/as/download`

```bash
curl -o - http://localhost:9000/csv/file/as/download
```

### Endpoint `/csv/file/as/stream`

```bash
curl -o - http://localhost:9000/csv/file/as/stream
```

### Endpoint `/csv/file/as/websocket`

```bash
curl -o - --http1.1 --include --no-buffer --header "Connection: Upgrade" --header "Upgrade: websocket" --header "Host: localhost:9000" --header "Origin: http://localhost:9000" --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQAAAA==" --header "Sec-WebSocket-Version: 13" http://localhost:9000/csv/file/as/websocket
```

### Endpoint `/csv/generator_n/as/download`

```bash
curl -o - http://localhost:9000/csv/generator_n/as/download
```

### Endpoint `/csv/generator_n/as/stream`

```bash
curl -o - http://localhost:9000/csv/generator_n/as/stream
```

### Endpoint `/csv/generator_n/as/websocket`

```bash
curl -o - --http1.1 --include --no-buffer --header "Connection: Upgrade" --header "Upgrade: websocket" --header "Host: localhost:9000" --header "Origin: http://localhost:9000" --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQAAAA==" --header "Sec-WebSocket-Version: 13" http://localhost:9000/csv/generator_n/as/websocket
```

### Endpoint `/csv/generator_infinite/as/stream`

```bash
curl -o - http://localhost:9000/csv/generator_infinite/as/stream
```

### Endpoint `/csv/generator_infinite/as/websocket`

```bash
curl -o - --http1.1 --include --no-buffer --header "Connection: Upgrade" --header "Upgrade: websocket" --header "Host: localhost:9000" --header "Origin: http://localhost:9000" --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQAAAA==" --header "Sec-WebSocket-Version: 13" http://localhost:9000/csv/generator_infinite/as/websocket
```