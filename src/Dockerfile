# syntax=docker/dockerfile:1
FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY ./web-ui/requirements.txt /usr/src/app/
RUN pip install -U -r requirements.txt
COPY ./web-ui /usr/src/app/
COPY ./entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
