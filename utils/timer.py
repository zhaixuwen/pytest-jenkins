import time
import datetime


class Timer:
    @classmethod
    def get_timestamp(cls):
        return str(int(time.time()) * 1000)

    @classmethod
    def get_date(cls):
        return time.strftime("%Y-%m-%d", time.localtime())

    @classmethod
    def get_ago_timestamp(cls, days=3):
        ago_date = datetime.datetime.now() - datetime.timedelta(days)
        ago_timestamp = int(time.mktime(ago_date.timetuple())) * 1000
        return str(ago_timestamp)
