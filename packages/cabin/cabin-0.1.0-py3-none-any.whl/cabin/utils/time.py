from datetime import datetime

from cabin.domain.summary_timespan import SummaryTimespan
from dateutil import tz, utils


def timestamp(dt: datetime) -> int:
    """Returns the datetime as a Unix timestamp with second precision.
    Note that the timezone will be converted to UTC.

    Args:
    - dt: The datetime

    Returns: A timestamp
    """
    return round(as_utc(dt).timestamp())


def fromtimestamp(ts: int) -> datetime:
    """Returns a datetime constructed from a Unix timestamp with second
    precision.
    Assumes the timestamp was in UTC.

    Args:
    - ts: The timestamp

    Returns: The datetime
    """
    return datetime.fromtimestamp(float(ts), tz=tz.UTC)


def as_utc(dt: datetime) -> datetime:
    """Returns the datetime object with a UTC timezone.
    Date and time data is adjusted so that the timestamp remains the same.

    Args:
    - dt: The datetime

    Returns: A datetime with the same timestamp, with the timezone set to UTC
    """
    dt = utils.default_tzinfo(dt, tz.UTC)
    return dt.astimezone(tz.UTC)


def start_of_day(dt: datetime) -> datetime:
    """Returns a datetime with the same day, month, year, and tzinfo values but
    with the time set to the start of the day.

    Args:
    - dt: The datetime

    Returns: A new datetime with the time set to 00:00
    """
    return datetime(dt.year, dt.month, dt.day, tzinfo=dt.tzinfo)


def start_of(timespan: SummaryTimespan, dt: datetime) -> datetime:
    """Returns a datetime which is set to the start of the interval specified by
    the timespan.
    """
    if timespan == SummaryTimespan.HOURLY:
        stripped_dt = dt.replace(minute=0, second=0, microsecond=0)
    else:
        stripped_dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return timespan.to_offset().rollback(stripped_dt)


def dateint(dt: datetime) -> int:
    """Formats a datetime as an integer (YYYYMMDD).

    Args:
    - dt: The datetime

    Returns: The date int
    """
    return int(dt.strftime(r"%Y%m%d"))
