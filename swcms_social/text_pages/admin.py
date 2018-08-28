from django.contrib import admin
from .models import Pages

try:
    from utils.admin import BaseAdmin
except ImportError:
    BaseAdmin = admin.ModelAdmin


@admin.register(Pages)
class PagesAdmin(BaseAdmin):
    list_display = ('__str__', 'url', 'display_absolute_url', 'is_active', 'changed', 'created')
    list_filter = ('is_active',)