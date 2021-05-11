FROM tensorflow/serving:2.3.0-gpu

LABEL maintainer="nshpak"

COPY ml/models/commands/ /models/commands/
EXPOSE 8500