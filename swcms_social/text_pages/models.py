from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

import re

from swcms_social._utils.models import AbstractTextModel, SeoModel


class PagesQuerySet(models.QuerySet):
    def active(self, *args, **kwargs):
        kwargs['is_active'] = True
        return super().filter(*args, **kwargs)


path_re = re.compile(r'^\/(?:[/?#]?[^\s]*)[^\/]$')
validate_path = RegexValidator(
    path_re,
    "Введите правильный url, без указания схемы и домена",
    'invalid'
)


class Pages(AbstractTextModel, SeoModel):
    url = models.CharField("URL", max_length=250, validators=[validate_path],
                           help_text="/about/test/test2", unique=True)

    objects = PagesQuerySet.as_manager()

    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ('-created',)


class Snippet(models.Model):
    slug = models.SlugField()
    content = RichTextUploadingField(blank=True, config_name=settings.CKEDITOR_CONFIGS.get('snippet', 'default'))
    tpl = models.TextField(blank=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'сниппет'
        verbose_name_plural = 'сниппеты'
