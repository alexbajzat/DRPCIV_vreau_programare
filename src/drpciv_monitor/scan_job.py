import requests
import json
import os
import argparse
import time
import logging
from notify_client import NotifyClient
from scheduler_helper import SchedulerHelper, date_string_to_datetime, date_to_string

BASE_URL = 'https://www.drpciv.ro/drpciv-booking-api/getAvailableDaysForSpecificService/1'


def configure_logger():
    logging.basicConfig(
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO)


class ScanJob(object):
    def __init__(self, dest_phone, dev_profile_enabled, sleep_interval, start_date, end_date, county_code,
                 twilio_number):
        configure_logger()
        self.__logger = logging.getLogger(__name__)
        self.__notify_client = NotifyClient(twilio_number)
        self.__dest_phone = dest_phone
        self.__scheduler_helper = SchedulerHelper(retain_period_seconds=40)
        self.__dev_profile_enabled = dev_profile_enabled
        self.__sleep_interval = sleep_interval
        self.__start_date = start_date
        self.__end_date = end_date
        self.__county_code = county_code

    def __fetch_available_days(self, start_date, end_date, county_code):
        request_url = BASE_URL + f'/{county_code}'
        response = json.loads(requests.get(request_url).text)
        return self.__process_available_dates(response, start_date, end_date)

    def __process_available_dates(self, dates, start_date, end_date):
        if dates is None:
            return
        dates_to_be_reported = []
        for date in dates:
            trimmed_date = date[:-9]
            date = date_string_to_datetime(trimmed_date)
            start_datetime = date_string_to_datetime(start_date)
            end_datetime = date_string_to_datetime(end_date)
            if start_datetime <= date <= end_datetime and self.__scheduler_helper.schedule_date(date):
                dates_to_be_reported.append(date)
        return set(dates_to_be_reported)

    def __notify(self, dates, dev=False):
        formatted_dates = list(map(lambda date: date_to_string(date), dates))
        if dev:
            self.__logger.info(f'Mocking Send: {formatted_dates}')
            return

        self.__notify_client.notify(self.__dest_phone, formatted_dates)

    def run(self):
        logging.info(f'Starting execution with arguments: start {self.__start_date}, end: {self.__end_date}, '
                     f'phone_number: {self.__dest_phone}')
        while True:
            dates = self.__fetch_available_days(self.__start_date, self.__end_date, self.__county_code)
            if len(dates) > 0:
                self.__notify(dates, self.__dev_profile_enabled)

            logging.info('Still going...')
            time.sleep(int(self.__sleep_interval))


def initialize_args():
    parser = argparse.ArgumentParser(description='Get available DRPCIV dates between {start_date} and {end_date} - '
                                                 'format yyyy-mm-dd')
    parser.add_argument('--start-date', dest='start_date')
    parser.add_argument('--end-date', dest='end_date')
    parser.add_argument('--county-code', dest='county_code', help='code specific for county to search in',
                        default=12)
    parser.add_argument('--phone-number', dest='dest_phone_number', help='phone number to send the notification to',
                        default=12)
    parser.add_argument('--twilio-phone-number', dest='twilio_phone_number', help='phone number from twilio',
                        default="+17146778785")
    parser.add_argument('--interval', dest='interval', help='time to sleep between searches (in seconds)',
                        default=60 * 10)
    return parser.parse_args()


def main():
    dev_profile_enabled = 'RUN_PROFILE' in os.environ and os.environ['RUN_PROFILE'] == 'dev'

    args = initialize_args()

    scan_job = ScanJob(args.dest_phone_number, dev_profile_enabled, args.interval, args.start_date, args.end_date,
                       args.county_code, args.twilio_phone_number)
    scan_job.run()


if __name__ == "__main__":
    main()
