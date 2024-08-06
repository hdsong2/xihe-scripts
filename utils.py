# -*- encoding: utf-8 -*-

from datetime import datetime


def str_to_datetime(date_string: str, format='%Y-%m-%d %H:%M:%S') -> datetime:
    return datetime.strptime(date_string.strip(), format)

def str_to_timestamp(date_string: str, format='%Y-%m-%d %H:%M:%S') -> int:
    return int(str_to_datetime(date_string, format).timestamp())