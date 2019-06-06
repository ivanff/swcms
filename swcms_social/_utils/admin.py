from django.contrib.postgres.fields.jsonb import JSONField
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.forms.widgets import HiddenInput
from django.http import HttpResponse
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe

from .tools import UnicodeWriter
from .templatetags._utils_tags import admin_url


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as_continue = True
    save_as = True

    def display_absolute_url(self, obj):
        url = obj.get_absolute_url()
        return mark_safe('<a href="{url}">{url}</a>'.format(url=url))

    display_absolute_url.allow_tags = True
    display_absolute_url.short_description = "Смотреть"


class ReadOnlyBaseAdmin(BaseAdmin):
    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class NgAppBaseAdmin(BaseAdmin):
    change_form_template = "admin/change_form_ng_app.html"
    formfield_overrides = {
        JSONField: {'widget': HiddenInput}
    }


def admin_change_link(field_name):
    def func(instance):
        value = instance
        prev_value = instance
        for s in field_name.split('__'):
            prev_value = value
            value = getattr(value, s)

        if not getattr(func, 'short_description', None):
            func.short_description = prev_value.__class__._meta.get_field(s).verbose_name
        return mark_safe("<a href='%s' target='_blank'>%s</a>" % (
            admin_url(value),
            value
        ))
    func.__name__ = "%s_%s" % (field_name, get_random_string(6))
    func.admin_order_field = field_name
    return func


def list_display_login_as(obj):
    return mark_safe("<a href='%s' target='_blank'>Login as %s</a>" % (
        reverse('login_as', args=(obj.id,)),
        obj.get_full_name(),
    ))


list_display_login_as.short_description = 'Login As'


def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')
    writer = UnicodeWriter(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        row = []
        for field in field_names:
            if field in field_names:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                val = u"%s" % (val,)
                row.append(val)
        writer.writerow(row)
    return response
export_as_csv.short_description = u'Экспортировать выбранное в формате электронной таблицы csv'