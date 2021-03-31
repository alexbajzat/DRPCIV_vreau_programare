import requests
import json
from twilio.rest import Client
import os

BASE_URL = 'https://www.drpciv.ro/drpciv-booking-api/getCalendar?'
ACCOUNT_SID = "AC52d3b8514449d0a9d485654116b36af7"


def fetch_available_days(start_date, end_date):
    request_url = BASE_URL + f'start={start_date}&end={end_date}&activityCode=1&countyCode=12'
    response = json.loads(requests.get(request_url).text)
    return parse_available_dates(response)


def parse_available_dates(dates):
    if dates is None:
        return
    dates_formatted = []
    for date in dates.keys():
        date = date[:-6]
        dates_formatted.append(f'available date: {date}')

    return set(dates_formatted)


def notify(dates, auth_token):
    client = Client(ACCOUNT_SID, auth_token)

    message = client.messages.create(
        to="+40749379976",
        from_="+17146778785",
        body=f"New dates: {str(dates)}")
    print(message.sid)


def main():
    twilio_auth_key = os.environ['TWILIO_AUTH_KEY']

    dates = fetch_available_days('2021-05-10', '2021-05-30')
    if len(dates) > 0:
        notify(dates, twilio_auth_key)


if __name__ == "__main__":
    main()
