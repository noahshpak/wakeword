# Wake Word

## Organization

- `ml` - directory for anything machine learning: models, notebooks, etc
- `service` - backend code - currently a Flask app that interfaces with Tensorflow Serving over gRPC. We use Gunicorn as our WSGI when running in production.


## Getting Started

*Note the current setup requires Docker!*


1. `make create_venv` - create a virtual environemnt
2. `make build`
3. `make run`