FROM python:3.9.2-buster

ARG TWILIO_AUTH

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY src/scan_job.py scan_job.py

ENV TWILIO_AUTH_KEY=TWILIO_AUTH

# ENTRYPOINT ["python3", "scan_job.py"]