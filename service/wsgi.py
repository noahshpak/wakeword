import logging
from flask import Flask, request
from service.tfserving_grpc import CommandsServingGrpc


app = Flask(__name__)


commands_model = CommandsServingGrpc()


@app.route("/")
def index():
    return "Wake Word!"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {".wav"}


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "Upload a .wav file"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    if file:
        confidences, label = commands_model.predict(file.read())
        print(confidences)
        return label


def setup_gunicorn_logging(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def start_production():
    setup_gunicorn_logging(app)
    return app
