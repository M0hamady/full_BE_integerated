from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Manager)
admin.site.register(User, UserAdmin)

@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'timestamp')
    list_filter = ('user', 'timestamp')
# class GuidelineInline(admin.TabularInline):
#     model = GuidelineContent
#     extra = 0

# class GuidanceManagerAdmin(admin.ModelAdmin):
#     inlines = [GuidelineInline]
#     list_display = ['user', 'calculate_finished_percentage']
#     list_filter = ['user','engineers']
#     search_fields = ['user__username',]

#     def get_engineers_count(self, obj):
#         return obj.engineers.count()
#     get_engineers_count.short_description = 'Engineers Count'

#     def get_guidelines_count(self, obj):
#         return obj.get_guidelines.count()
#     get_guidelines_count.short_description = 'Guidelines Count'

# class GuidelineAdmin(admin.ModelAdmin):
#     list_display = ['message', 'is_seen', 'is_finished']
#     list_filter = ['is_seen', 'is_finished']
#     search_fields = ['message']

# admin.site.register(GuidanceManager, GuidanceManagerAdmin)
# admin.site.register(GuidelineContent, GuidelineAdmin)