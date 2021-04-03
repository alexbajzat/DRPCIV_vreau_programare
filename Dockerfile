FROM python:3.9.2-buster

ARG TWILIO_AUTH
ARG TWILIO_SID

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY src/scan_job.py scan_job.py

ENV TWILIO_AUTH_KEY=TWILIO_AUTH
ENV TWILIO_ACCOUNT_SID=TWILIO_SID

ENTRYPOINT ["python3", "scan_job.py"]