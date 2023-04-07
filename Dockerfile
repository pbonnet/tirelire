FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

COPY scripts/. /app/scripts
COPY tirelire/. /app/tirelire
COPY requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["/app/scripts/container/start-server"]