import requests
import json
from twilio.rest import Client
import os
import argparse
from datetime import datetime
import time
import logging

BASE_URL = 'https://www.drpciv.ro/drpciv-booking-api/getAvailableDaysForSpecificService/1'
ACCOUNT_SID = "AC52d3b8514449d0a9d485654116b36af7"

reported_dates = set()


def fetch_available_days(start_date, end_date, county_code):
    request_url = BASE_URL + f'/{county_code}'
    response = json.loads(requests.get(request_url).text)
    return process_available_dates(response, start_date, end_date)


def process_available_dates(dates, start_date, end_date):
    if dates is None:
        return
    dates_formatted = []
    for date in dates:
        trimmed_date = date[:-9]
        date = datetime.strptime(trimmed_date, '%Y-%m-%d')
        start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        if start_datetime <= date <= end_datetime and trimmed_date not in reported_dates:
            dates_formatted.append(trimmed_date)
            # reported_dates.add(trimmed_date)

    return set(dates_formatted)


def notify(dates, auth_token, dest_phone_number, dev=False):
    if dev:
        logging.info(f'Mocking Send: {str(dates)} to {dest_phone_number}')
        return

    client = Client(ACCOUNT_SID, auth_token)
    message = client.messages.create(
        to=dest_phone_number,
        from_="+17146778785",
        body=f"New dates: {str(dates)}")

    logging.info(f'sent with sid {message.sid}')


def initialize_args():
    parser = argparse.ArgumentParser(description='Get available DRPCIV dates between {start_date} and {end_date} - '
                                                 'format yyyy-mm-dd')
    parser.add_argument('--start-date', dest='start_date')
    parser.add_argument('--end-date', dest='end_date')
    parser.add_argument('--county-code', dest='county_code', help='code specific for county to search in', default=12)
    parser.add_argument('--phone-number', dest='dest_phone_number', help='phone number to send the notification to',
                        default=12)
    parser.add_argument('--interval', dest='interval', help='time to sleep between searches (in seconds)',
                        default=60 * 10)
    return parser.parse_args()


def configure_logger():
    logging.basicConfig(
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO)


def main():
    twilio_auth_key = os.environ['TWILIO_AUTH_KEY']
    dev_profile_enabled = 'RUN_PROFILE' in os.environ and os.environ['RUN_PROFILE'] == 'dev'

    args = initialize_args()

    configure_logger()
    logging.info(f'Starting execution with arguments: start {args.start_date}, end: {args.end_date}, '
                 f'phone_number: {args.dest_phone_number}')

    while True:
        dates = fetch_available_days(args.start_date, args.end_date, args.county_code)
        if len(dates) > 0:
            notify(dates, twilio_auth_key, args.dest_phone_number, dev_profile_enabled)

        logging.info('Still going...')
        time.sleep(int(args.interval))


if __name__ == "__main__":
    main()
