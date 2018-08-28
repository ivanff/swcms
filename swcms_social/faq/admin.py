from django.contrib import admin

from .models import Faq, Subject
from swcms_social._utils.admin import BaseAdmin


@admin.register(Subject)
class SubjectAdmin(BaseAdmin):
    list_display = ('id', 'h1', 'order')
    list_editable = ('order',)
    search_fields = ('h1',)


@admin.register(Faq)
class FaqAdmin(BaseAdmin):
    list_display = ('id', 'h1', 'subject', 'is_active', 'order')
    list_editable = ('order',)
    search_fields = ('h1',)
    list_filter = ('subject',)
    list_select_related = ('subject',)