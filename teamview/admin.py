from django.contrib import admin
from django.utils.html import format_html
from.models import Viewer

class ViewerAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('name', 'uuid')
    readonly_fields = ('uuid', )

    

    def is_active_label(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">Active</span>')
        else:
            return format_html('<span style="color: red;">Inactive</span>')
    is_active_label.short_description = 'Status'

admin.site.register(Viewer, ViewerAdmin)