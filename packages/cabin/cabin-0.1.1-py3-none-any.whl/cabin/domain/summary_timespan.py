from enum import Enum

from pandas.tseries.offsets import (
    DateOffset,
    Day,
    Hour,
    MonthBegin,
    QuarterBegin,
    Week,
    YearBegin,
)


class SummaryTimespan(Enum):
    """A timespan for a data summmary.

    Values correspond to keys for DateOffset objects in pandas:
    https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
    """

    HOURLY = "H"
    DAILY = "D"
    WEEKLY = "W-MON"
    MONTHLY = "MS"
    SEASONAL = "QS-DEC"
    YEARLY = "AS"

    def to_offset(self) -> DateOffset:
        if self.value == "H":
            return Hour(1)
        elif self.value == "D":
            return Day(1)
        elif self.value == "W-MON":
            return Week(1, weekday=0)
        elif self.value == "MS":
            return MonthBegin(1)
        elif self.value == "QS-DEC":
            return QuarterBegin(startingMonth=10)
        elif self.value == "AS":
            return YearBegin(1)
        raise NotImplementedError(self.value)
