#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import pytz

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_ZONE = pytz.timezone("Asia/Shanghai")


def timestamp_to_datetime_with_tz(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, tz=TIME_ZONE)


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def timestamp_to_datetime_str(timestamp, format_str=DATE_TIME_FORMAT):
    return datetime.datetime.fromtimestamp(timestamp).strftime(format_str)


def datetime_to_timestamp(date_time):
    return date_time.second


def datetime_str_to_timestamp(date_time_str, format_str=DATE_TIME_FORMAT):
    return int(time.mktime(time.strptime(date_time_str, format_str)))


def get_now_timestamp():
    return int(time.time())


if __name__ == '__main__':
    ts = get_now_timestamp()
    print ts
    dt = timestamp_to_datetime(ts)
    print dt
    dt_str = timestamp_to_datetime_str(ts)
    print dt_str
    print datetime_to_timestamp(dt)
    print datetime_str_to_timestamp(dt_str)
