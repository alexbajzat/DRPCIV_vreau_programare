import os
from twilio.rest import Client
import logging


class NotifyClient(object):
    def __init__(self, twilio_number):
        twilio_key = os.environ['TWILIO_AUTH_KEY']
        twilio_sid = os.environ['TWILIO_ACCOUNT_SID']
        logging.info(f'yeah, not the best practice but: key {twilio_key}, sid {twilio_sid}')
        self.__twilio_number = twilio_number
        self.__client = Client(twilio_sid, twilio_key)
        self.__logger = logging.getLogger(__name__)

    def notify(self, dest_phone, dates):
        message = self.__client.messages.create(
            to=dest_phone,
            from_=self.__twilio_number,
            body=f"New dates: {str(dates)}")

        self.__logger.info(f'Sent to {dest_phone} with sid {message.sid}, dates: {dates}')
