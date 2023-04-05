FROM python:3.10-slim

COPY tirelire/. /app/tirelire
COPY requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

CMD ["python", "/app/tirelire/manage.py", "runserver", "0.0.0.0:8000"]