from datetime import datetime, timedelta


def date_string_to_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()


def date_to_string(date):
    return datetime.strftime(date, '%Y-%m-%d')


class SchedulerHelper(object):
    def __init__(self, retain_period_seconds=2400, number_of_notifies=2):
        self.__reported_dates = []
        self.__retain_period_seconds = retain_period_seconds
        self.__number_of_notifies = number_of_notifies

    def schedule_date(self, date):
        if len(self.__reported_dates) == 0:
            self.__reported_dates.append(ConsumableDate(date, self.__number_of_notifies))
            return True
        date_exists = False
        for idx, reporting in enumerate(self.__reported_dates):
            if reporting.get_date() == date:
                date_exists = True
                if reporting.get_timestamp() + timedelta(seconds=self.__retain_period_seconds) <= datetime.now():
                    self.__reported_dates[idx].reset()

                if reporting.get_count() > 0:
                    self.__reported_dates[idx].decrease_counter()
                    return True
        if not date_exists:
            self.__reported_dates.append(ConsumableDate(date, self.__number_of_notifies))
            return True
        return False


class ConsumableDate(object):
    def __init__(self, date, count, timestamp=datetime.now()):
        self.__date = date
        self.__count = count
        self.__initial_count = count
        self.__timestamp = timestamp

    def decrease_counter(self):
        self.__count = self.__count - 1

    def reset(self):
        self.__timestamp = datetime.now()
        self.__count = self.__initial_count

    def get_date(self):
        return self.__date

    def get_count(self):
        return self.__count

    def get_timestamp(self):
        return self.__timestamp
