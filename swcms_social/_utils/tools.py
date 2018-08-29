import datetime

import pytz


def get_gmt_offset(tz):
    tz_now = datetime.datetime.now(pytz.timezone(tz))
    return tz_now.utcoffset().total_seconds() / 60 / 60.0


def format_gmt_offset(offset):
    if offset == 0:
        return "+00:00"

    symbol = '+'
    if offset < 0:
        symbol = '-'

    return "%s%02d:%02d" % (
        symbol,
        abs(offset),
        abs(60 * (offset - int(offset)))
    )
