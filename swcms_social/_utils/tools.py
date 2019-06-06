import datetime
import requests
import os
from django.conf import settings
from ipware import get_client_ip
import pytz
import csv


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


def update_filename(instance, filename, path):
    sub_dir_name = os.path.dirname(filename)
    filename = os.path.basename(filename)
    if sub_dir_name:
        if not os.path.exists(settings.MEDIA_ROOT + '/' + path + '/' + sub_dir_name):
            os.mkdir(settings.MEDIA_ROOT + '/' + path + '/' + sub_dir_name)
        return path + sub_dir_name + '/' + filename
    return path + filename


class _UnicodeWriteWrapper(object):
    """Simple write() wrapper that converts unicode to bytes."""

    def __init__(self, binary, encoding, errors):
        self.binary = binary
        self.encoding = encoding
        self.errors = errors

    def write(self, string):
        return self.binary.write(string.encode(self.encoding, self.errors))


class UnicodeWriter(object):
    def __init__(self, f, dialect=csv.excel, encoding='utf-8', errors='strict',
                 *args, **kwds):
        if f is None:
            raise TypeError

        f = _UnicodeWriteWrapper(f, encoding=encoding, errors=errors)
        self.writer = csv.writer(f, dialect, *args, **kwds)

    def writerow(self, row):
        return self.writer.writerow(row)

    def writerows(self, rows):
        return self.writer.writerows(rows)

    @property
    def dialect(self):
        return self.writer.dialect
