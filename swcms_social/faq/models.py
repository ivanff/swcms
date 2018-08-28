from django.db import models
from django.urls import reverse

try:
    from utils.models import AbstractTextModel
except ImportError:
    AbstractTextModel = models.Model


class Subject(models.Model):
    h1 = models.CharField("H1", max_length=250)
    order = models.IntegerField(default=0, help_text="Меньше первее", db_index=True)

    def __str__(self):
        return self.h1

    class Meta:
        ordering = ('order',)
        verbose_name = 'тема помощи'
        verbose_name_plural = 'темы помощи'


class FaqQuerySet(models.QuerySet):
    def active(self, *args, **kwargs):
        kwargs['is_active'] = True
        return super().filter(*args, **kwargs)


class Faq(AbstractTextModel):
    subject = models.ForeignKey(Subject, verbose_name="Тема",
                                null=True, blank=True, on_delete=models.SET_NULL)
    order = models.IntegerField(default=0, help_text="Меньше первее")

    objects = FaqQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('app-faq', args=(self.pk,))

    class Meta:
        ordering = ('subject__order', 'order',)
        index_together = [('subject', 'order')]
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'