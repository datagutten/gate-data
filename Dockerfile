FROM python:3.14
RUN pip install -U pip prometheus-client flask requests

WORKDIR /app
COPY *.py /app
COPY feig /app/feig