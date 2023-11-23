from django.contrib import admin

from markting.models import Marketing
class MarketingAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid' )
    search_fields = ('name','uuid')
# Register your models here.
admin.site.register(Marketing,MarketingAdmin)