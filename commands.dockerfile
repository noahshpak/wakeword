FROM tensorflow/serving:2.3.0-gpu

LABEL maintainer="nshpak"

ENV MODEL_NAME=commands
COPY ml/models/$MODEL_NAME/ /models/$MODEL_NAME/
EXPOSE 8500