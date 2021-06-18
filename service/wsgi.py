import io
import soundfile as sf
import logging
import sys
import traceback

from flask import Flask, request, render_template

from flask_socketio import SocketIO

from service.tfserving_grpc import CommandsServingGrpc

app = Flask(__name__)
socketio = SocketIO(app)

commands_model = CommandsServingGrpc()


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("my event")
def handle_my_custom_event(json):
    # print("received json: " + str(json))
    wav_data = json["data"]["audio"]["data"]
    confidences, label = commands_model.predict(wav_data)
    print(confidences, label)
    socketio.emit("prediction", f"Label: {label}")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {".wav"}


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return "Upload a .wav file"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            confidences, label = commands_model.predict(file.read())
            return label
    except Exception:
        print("Exception in user code:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)


def setup_gunicorn_logging(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def setup_socketio(app):
    app = SocketIO(app)
    return app


def start_production():
    setup_gunicorn_logging(app)
    setup_socketio(app)
    return app
