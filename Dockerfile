FROM python:3.8-slim-buster

ARG twilio_auth_key
ENV start_date
ENV end_date
ENV phone_number
ENV interval
ENV county_code

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

COPY src/scan_job.py scan_job.py

ENV TWILIO_AUTH_KEY=$twilio_auth_key

CMD ["python3", "scan_job.py", "--start-date", start_date, "--end-date", end_date, "--phone-number", phone_number, "--county-code", county_code]