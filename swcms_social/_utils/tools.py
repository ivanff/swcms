import datetime
import requests
from django.conf import settings
from ipware import get_client_ip
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


def is_recaptcha_valid(request, field_name='recaptcha'):
    """
    Verify if the response for the Google recaptcha is valid.
    """
    if hasattr(request, 'data'):
        data = request.data
    else:
        data = request.POST

    return requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': settings.GOOGLE['recaptcha']['secret'],
            'response': data.get(field_name),
            'remoteip': get_client_ip(request)
        },
        verify=True
    ).json().get("success", False)
