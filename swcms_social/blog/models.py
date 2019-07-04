from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from .._utils.models import AbstractTextModel, SeoModel


class Tags(models.Model):
    title = models.CharField("Заголовок", max_length=250, blank=True, default="")
    h1 = models.CharField("H1", max_length=250, blank=True, default="")
    name = models.CharField("Имя", max_length=250, blank=True, default="")

    @cached_property
    def get_absolute_url(self):
        return reverse('blog:list') + '?tag=%s' % (self.id,)

    def __str__(self):
        return self.title or self.id

    class Meta:
        ordering = ('-id',)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class PostsQuerySet(models.QuerySet):
    def active(self, *args, **kwargs):
        kwargs['is_active'] = True
        return super().filter(*args, **kwargs)


class Posts(AbstractTextModel, SeoModel):
    tags = models.ManyToManyField(Tags, blank=True)
    anons = models.TextField("Анонс", blank=True, default="")

    objects = PostsQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('blog:detail', args=(self.id,))

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ('-created',)
