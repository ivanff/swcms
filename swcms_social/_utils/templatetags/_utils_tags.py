from django import template
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.messages import get_messages
from django.urls.base import reverse

import json

from django.utils.html import escapejs

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


@register.simple_tag(takes_context=True)
def messages_to_json(context):
    result = {}
    messages = get_messages(context['request'])
    for m in messages:
        item = [{'message': m.message, 'level': m.level, 'extra_tags': m.extra_tags}]
        if result.setdefault(m.tags, item) != item:
            result[m.tags].extend(item)
    return escapejs(json.dumps(result))