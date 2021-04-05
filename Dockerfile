FROM python:3.9.2-buster

ARG TWILIO_AUTH
ARG TWILIO_SID

ENV TWILIO_AUTH_KEY=TWILIO_AUTH
ENV TWILIO_ACCOUNT_SID=TWILIO_SID

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY src/drpciv_monitor/* .

ENTRYPOINT ["python3", "scan_job.py"]