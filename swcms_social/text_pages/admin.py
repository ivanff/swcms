from django.contrib import admin
from .models import Pages
from swcms_social._utils.admin import BaseAdmin


@admin.register(Pages)
class PagesAdmin(BaseAdmin):
    list_display = ('__str__', 'url', 'display_absolute_url', 'is_active', 'changed', 'created')
    list_filter = ('is_active',)