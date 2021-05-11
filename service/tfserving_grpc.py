import os
import grpc
import numpy as np
from typing import NamedTuple
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

from service import audio


class GrpcParams(NamedTuple):
    hostport: str
    input_tensor: str
    output_tensor: str
    model_spec: str
    signature: str
    model_spec_version: str = None


def commands_params() -> GrpcParams:
    return GrpcParams(
        hostport=os.getenv("TFSERVING_HOSTNAME", "localhost:8500"),
        input_tensor="input_1",
        output_tensor="dense_1",
        model_spec="commands",
        model_spec_version=None,  # can be None
        signature="serving_default",
    )


class ServingGrpc:
    def __init__(self, grpc_params: GrpcParams):
        options = [("grpc.max_receive_message_length", 16 * 500 * 700)]
        channel = grpc.insecure_channel(grpc_params.hostport, options=options)
        stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

        self.stub = stub
        self.grpc_params = grpc_params

    def predict(self, *args):
        pass


class CommandsServingGrpc(ServingGrpc):
    CLASS_MAP = ["right", "go", "no", "left", "stop", "up", "down", "yes"]

    def __init__(self, grpc_params=commands_params()):
        super(CommandsServingGrpc, self).__init__(grpc_params)

    def predict(self, input_bytes):
        spectogram = audio.get_spectrogram(audio.decode_audio(input_bytes))
        grpc_request = predict_pb2.PredictRequest()
        grpc_request.model_spec.name = self.grpc_params.model_spec
        grpc_request.model_spec.signature_name = self.grpc_params.signature
        if self.grpc_params.model_spec_version is not None:
            grpc_request.model_spec.version.value = int(self.grpc_params.model_spec_version)

        grpc_request.inputs[self.grpc_params.input_tensor].CopyFrom(
            tf.make_tensor_proto(np.asarray([spectogram]), dtype=tf.float32, shape=[1] + list(spectogram.shape))
        )

        result = self.stub.Predict(grpc_request, 300.0)
        confidences = np.array(result.outputs[self.grpc_params.output_tensor].float_val)
        return confidences, self.CLASS_MAP[np.argmax(confidences)]
