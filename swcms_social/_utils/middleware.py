from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.urls import is_valid_path
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

import pytz

from tz_detect.middleware import TimezoneMiddleware


class RedirectTrailingSlashMiddleware(MiddlewareMixin):
    response_redirect_class = HttpResponsePermanentRedirect

    def process_request(self, request):
        if settings.APPEND_SLASH:
            return

        if '/admin/' in request.path:
            return

        if '/utils/login_as' in request.path:
            return

        if '/sandbox/' in request.path:
            return

        if '/__debug__/' in request.path:
            return

        if request.path_info.endswith('/'):
            urlconf = getattr(request, 'urlconf', None)

            if is_valid_path(request.path_info[:-1], urlconf):
                new_path = request.path_info[:-1]

                if request.method == 'GET':
                    if request.META['QUERY_STRING']:
                        new_path += '?' + request.META['QUERY_STRING']

                if settings.DEBUG and request.method in ('POST', 'PUT', 'PATCH'):
                    raise RuntimeError(
                        "You called this URL via %(method)s, but the URL doesn't end "
                        "in a slash and you have APPEND_SLASH set. Django can't "
                        "redirect to the slash URL while maintaining %(method)s data. "
                        "Change your form to point to %(url)s (note the trailing "
                        "slash), or set APPEND_SLASH=False in your Django settings." % {
                            'method': request.method,
                            'url': request.get_host() + new_path,
                        }
                    )
                return self.response_redirect_class(new_path)


class UserTimezoneMiddleware(TimezoneMiddleware):

    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.timezone:
                timezone.activate(pytz.timezone(request.user.timezone))
                return
        super().process_request(request)
