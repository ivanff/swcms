from functools import partial

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from swcms_social._utils.tools import _update_filename


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


def attachment_upload(path):
    return partial(_update_filename, path=path)


class Attachment(models.Model):
    file = models.FileField(u'Файл', upload_to=attachment_upload('attachments/'))
    is_image = models.BooleanField(u"Изображение", default=False, editable=False)
    title = models.CharField(u'Название', blank=True, default="", max_length=255)
    desc = models.TextField(u'Описание', blank=True, default="")

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey()

    def get_file_format(self):
        try:
            return self.file.name.rsplit('.')[-1].lower()
        except:
            return ''

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.is_image = self.get_file_format() in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif']
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True

