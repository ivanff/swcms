from django import template
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.urls.base import reverse

register = template.Library()


@register.simple_tag
def admin_url(obj, action='change'):
    if not action in ('add', 'change', 'delete'):
        raise ValueError
    if action == 'add':
        url = reverse(admin_urlname(obj.__class__._meta, action))
    elif action in ('change', 'delete'):
        url = reverse(admin_urlname(obj.__class__._meta, action), args=(obj.id,))
    else:
        raise ValueError
    return url
