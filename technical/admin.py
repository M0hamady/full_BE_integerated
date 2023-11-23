from django.contrib import admin

from technical.models import Technical
class TechnicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid' )
    search_fields = ('name','uuid')
# Register your models here.
admin.site.register(Technical,TechnicalAdmin)
