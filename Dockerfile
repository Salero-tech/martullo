FROM python:latest

RUN mkdir -p /usr/src/
WORKDIR /usr/src/bot/
COPY bot/ .


RUN python3 -m pip install -r requirements.pip


CMD [ "python3", "main.py" ]