# auto generated by update_py.py
import time
import sys
import datetime
import pytz

class Timer:

    nano_seconds_per_second = 1e9

    @staticmethod
    def nano():
        return Timer.time_to_nano(time.time())

    @staticmethod
    def datetime():
        return datetime.datetime.now(pytz.timezone('Asia/Shanghai'))

    @staticmethod
    def nano_to_datetime(nano):
        return datetime.datetime.fromtimestamp(1.0 * nano / Timer.nano_seconds_per_second, pytz.timezone('Asia/Shanghai'))

    @staticmethod
    def get_nano(time_str, format='%Y-%m-%d %H:%M:%S'):
        time_parsed = time.mktime(time.strptime(time_str, format))
        return Timer.time_to_nano(time_parsed)

    @staticmethod
    def time_to_nano(t):
        if sys.version_info < (3, 0):
            return long(t * Timer.nano_seconds_per_second)
        else:
            return int(t * Timer.nano_seconds_per_second)