from django.contrib import admin
from .models import Client, ClientAction, Payment
from project.models import  Project, ProjectBasic, ProjectFile, ProjectImage
admin.site.register(Payment)

class ProjectBasicDetailsInline(admin.StackedInline):
    model = ProjectBasic
    max_num = 1
    verbose_name_plural = 'Basic Details'

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage

class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1
    can_delete = False
    verbose_name_plural = 'ProjectFiles'

class ProjectInline(admin.TabularInline):
    model = Project
    inlines = [ProjectBasicDetailsInline, ProjectFileInline, ProjectImageInline]
    extra = 0
    can_delete = False
    verbose_name_plural = 'Project'

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name','client_access_key', 'needed_action','email', 'created_date')
    search_fields = ('name', 'email')
    list_filter = ('is_active', 'created_date')
    readonly_fields = ('created_date',)
    inlines = [ProjectInline,] 

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj and obj.project_client():
            pass
            # fields += ('project_data',) # Include the associated project data field
        return fields

    def project_data(self, obj):
        project = obj.project_client()
        if project:
            return f"Project Name: {project.name}\nProject Description: {project.description}"
        return "No associated project found."
    def client_access_key(self, obj):
        return obj.uuid
    project_data.short_description = 'Associated Project'

admin.site.register(Client,ClientAdmin)
admin.site.register(ClientAction)

