import time
import datetime
from scheduler import Scheduler

from send_values import send_values


def send_scheduler():
    schedule = Scheduler()
    schedule.hourly(
        datetime.time(minute=30, second=15),
        send_values,
    )

    #TODO for test only
    # schedule.minutely(datetime.time(second=15), send_values)

    while True:
        schedule.exec_jobs()
        time.sleep(1)


if __name__ == "__main__":
    send_scheduler()
