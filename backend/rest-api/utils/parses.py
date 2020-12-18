import datetime


def parse_date_time_str_to_datetime(date_time_str) -> datetime.datetime:
    return datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')


def parse_datetime_to_date_time_str(datetime_obj: datetime.datetime) -> str:
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
