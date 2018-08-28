from django.contrib import admin

try:
    from utils.admin import BaseAdmin
except ImportError:
    BaseAdmin = admin.ModelAdmin
    
from .models import Tags, Posts

admin.site.register(Tags)


@admin.register(Posts)
class PostsAdmin(BaseAdmin):
    list_display = ('__str__', 'h1', 'is_active', 'changed', 'created')
    list_filter = ('is_active', 'tags')
    filter_horizontal = ('tags',)
