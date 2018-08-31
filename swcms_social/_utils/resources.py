from collections import OrderedDict

from babel.dates import get_timezone_location
from pytz import common_timezones_set

from .tools import format_gmt_offset, get_gmt_offset

timezones = common_timezones_set - {'UTC'}

__TIMEZONES_DICT = OrderedDict()
__tz_offset_tz_name_map = {}

for tz_name in timezones:
    gmt_offset = get_gmt_offset(tz_name)
    tz_locale_name = get_timezone_location(tz_name, locale='ru', return_city=True)
    first_tz_name = __tz_offset_tz_name_map.setdefault(gmt_offset, tz_name)
    if __TIMEZONES_DICT.setdefault(first_tz_name, [tz_locale_name]) != [tz_locale_name]:
        if tz_locale_name not in __TIMEZONES_DICT[first_tz_name]:
            __TIMEZONES_DICT[first_tz_name].append(tz_locale_name)

TIMEZONES = []
for tz_name, tz_locale_names in __TIMEZONES_DICT.items():
    tz_locale_names = sorted(tz_locale_names)
    for tz_locale_name in tz_locale_names:
        TIMEZONES.append([
            tz_name, "(GMT%s) %s" % (format_gmt_offset(get_gmt_offset(tz_name)), tz_locale_name)
        ])

TIMEZONES = sorted(TIMEZONES, key=lambda item: get_gmt_offset(item[0]))

