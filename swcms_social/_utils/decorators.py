from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

from .tools import is_recaptcha_valid


def logging_response(logger):
    def decorator(view):
        @wraps(view)
        def logging_wrapper(request, *args, **kwargs):
            resp = view(request, *args, **kwargs)
            if hasattr(resp, 'content'):
                logger.info("""
request.body: %s
response.content: %s
                """, request.body, resp.content)
            return resp

        return logging_wrapper

    return decorator


def unlogin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, for_auth_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=for_auth_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def human_required(view_func, field_name=None):
    """
    This decorator is aimed to verify Google recaptcha in the backend side.
    """

    def wrapped(request, *args, **kwargs):
        if is_recaptcha_valid(request, field_name=(field_name or 'recaptcha')):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    return wrapped
