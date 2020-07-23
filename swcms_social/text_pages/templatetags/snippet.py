from django import template
from django.conf import settings
from django.db.models import Q
from django.template import Template
from django.urls import reverse
from django.utils import translation
from django.utils.safestring import mark_safe

from swcms_social.text_pages.models import Snippet

register = template.Library()


@register.simple_tag(takes_context=True)
def snippet(context, slug):
    user = getattr(context.get('request', object()), 'user', None)
    try:
        snippet = Snippet.objects.get(slug=slug)
    except Snippet.DoesNotExist:
        result = "<p>Snippet with slug '{slug}' not found</p>".format(slug=slug)

        if user:
            if user.is_staff:
                result += "<a href='{url}?slug={slug}&site={site_id}' target='_blank'>Add snippet '{slug}'</a>".format(
                    url=reverse('admin:%s_%s_add' % (Snippet._meta.app_label, Snippet._meta.model_name)),
                    site_id=settings.SITE_ID,
                    slug=slug,
                )
        return mark_safe(result)

    if snippet.tpl:
        context['snippet'] = snippet
        result = Template(snippet.tpl).render(context)
        if user:
            if user.is_staff:
                url = reverse('admin:%s_%s_change' % (Snippet._meta.app_label, Snippet._meta.model_name),
                              args=(snippet.id,))
                result += "<a href='{url}?slug={slug}&site={site_id}' target='_blank'>Change snippet '{slug}'</a>".format(
                    url=url,
                    site_id=settings.SITE_ID,
                    slug=slug,
                )
        return mark_safe(result)
    elif template:
        return mark_safe("""
<!-- snippet_slug: {snippet.slug}, snippet_id: {snippet.id}, LANGUAGE_CODE: {LANGUAGE_CODE} -->
{snippet.content}""".format(snippet=snippet, LANGUAGE_CODE=translation.get_language()))
    else:
        if settings.DEBUG:
            return mark_safe("<!-- snippet slug: %(slug)s, id: %(id)s -->%(text)s".format(
                slug=snippet.slug,
                id=snippet.id,
                text=snippet.text
            ))
        else:
            return mark_safe(snippet.text)
