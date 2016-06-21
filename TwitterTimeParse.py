from datetime import tzinfo, timedelta, datetime, time, date


ZERO = timedelta(0)
HOUR = timedelta(hours=1)

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

mutc = UTC()

class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, offset, name):
        self.__offset = timedelta(minutes = offset)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO

import time as _time

STDOFFSET = timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET


class LocalTimezone(tzinfo):

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

Local = LocalTimezone()

def format_date(utc, isoformat=False):
    """Parse Twitter's UTC date into UTC or local time."""
    u = datetime.strptime(utc.replace('+0000','UTC'), '%a %b %d %H:%M:%S %Z %Y')
    # This is the least painful way I could find to create a non-naive
    # datetime including a UTC timezone. Alternative suggestions
    # welcome.
    unew = datetime.combine(u.date(), time(u.time().hour,
        u.time().minute, u.time().second, tzinfo=mutc))

    # Convert to localtime
    unew = unew.astimezone(Local)

    return unew
    #if isoformat:
    #    return unew.isoformat()
    #else:
    #    return unew.strftime('%Y-%m-%d %H:%M:%S %Z')