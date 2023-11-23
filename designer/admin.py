from django.contrib import admin

from designer.models import ChatBoot, ChatState, Designer

# Register your models here.
admin.site.register(Designer)
admin.site.register(ChatBoot)
admin.site.register(ChatState)
