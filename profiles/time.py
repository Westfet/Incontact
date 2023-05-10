import datetime
import zoneinfo

import pytz


def now_datetime(args, localize: pytz.tzinfo.DstTzInfo = None, **kwargs) -> datetime.datetime:
    now = datetime.datetime.now(args, kwargs)

    if localize:
        now = now.astimezone(localize)

    return now


def now_utc() -> datetime.datetime:
    return datetime.datetime.now(pytz.UTC)


def now_date(*args, localize: pytz.tzinfo.DstTzInfo = None, kwargs) -> datetime.date:
    now = now_datetime(*args, localize, **kwargs)
    return now.date()


def actual_timezone() -> zoneinfo.ZoneInfo:
    return zoneinfo.ZoneInfo('Europe/Moscow')


def now_tz() -> datetime.datetime:
    return datetime.datetime.now(tz=actual_timezone())


def to_tz_date(timestamp: datetime.datetime) -> datetime.date:
    return timestamp.astimezone(tz=actual_timezone()).date()


def to_tz_datetime(timestamp: datetime.datetime) -> datetime.datetime:
    return timestamp.astimezone(tz=actual_timezone())