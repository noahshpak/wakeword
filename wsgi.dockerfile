FROM python:3.8-slim
LABEL maintainer="nshpak"

WORKDIR /service

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN groupadd -g 1000 wakeword_group && \
    useradd -r -u 1000 -g wakeword_group wakeword_user

USER wakeword_user


ENV PYTHONUNBUFFERED TRUE
EXPOSE 5000