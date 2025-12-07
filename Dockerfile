FROM python:3.14
RUN pip install -U pip prometheus-client

WORKDIR /app
COPY *.py /app
COPY gate /app/gate