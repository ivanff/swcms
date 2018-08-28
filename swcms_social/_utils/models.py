
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class AbstractTextModel(models.Model):
    h1 = models.CharField("H1", max_length=250, blank=True, default="")
    text = RichTextUploadingField("Текст")

    is_active = models.BooleanField("Активен", default=True)

    def __str__(self):
        return self.h1 or str(self.id)

    class Meta:
        ordering = ('-id',)
        abstract = True


class SeoModel(models.Model):
    title = models.CharField("<title>", max_length=250, blank=True, default='')
    desc = models.TextField('<meta name="description">', blank=True, default='')
    keys = models.TextField('<meta name="keywords">', blank=True, default='')

    created = models.DateTimeField("создан", auto_now_add=True)
    changed = models.DateTimeField("изменен", auto_now=True)

    class Meta:
        abstract = True