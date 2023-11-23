from django.contrib import admin

from client.models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid' )
    search_fields = ('name','uuid')
# Register your models here.
admin.site.register(Client,ClientAdmin)
