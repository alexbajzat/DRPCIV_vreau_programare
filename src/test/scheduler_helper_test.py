from drpciv_monitor.scheduler_helper import SchedulerHelper, date_string_to_datetime
import time


def test_scheduler_reporting_by_count():
    scheduler = SchedulerHelper(60, 1)
    date = date_string_to_datetime("2021-05-24")

    assert scheduler.schedule_date(date)
    assert scheduler.schedule_date(date)
    assert scheduler.schedule_date(date) is False


def test_scheduler_reporting_by_count_multiple_dates():
    scheduler = SchedulerHelper(60, 1)
    dates = [date_string_to_datetime("2021-05-24"), date_string_to_datetime("2021-05-25")]

    for date in dates:
        assert scheduler.schedule_date(date)
        assert scheduler.schedule_date(date)
        assert scheduler.schedule_date(date) is False


def test_scheduler_reset_by_time():
    scheduler = SchedulerHelper(5, 1)
    date = date_string_to_datetime("2021-04-20")

    assert scheduler.schedule_date(date)
    assert scheduler.schedule_date(date)
    assert scheduler.schedule_date(date) is False
    print('waiting for reset....')
    time.sleep(5)
    assert scheduler.schedule_date(date)


if __name__ == '__main__':
    test_scheduler_reporting_by_count()
    test_scheduler_reporting_by_count_multiple_dates()
    test_scheduler_reset_by_time()
