from django.contrib import admin

from .models import *

class ProjectBasicInline(admin.TabularInline):
    model = ProjectBasic
    extra = 0
    can_delete = False

class ProjectBasicAdmin(admin.ModelAdmin):
    list_display = ('project', 'owner',"uuid" )
    search_fields = ('uuid',)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectBasicInline,)
    list_display = ( 'uuid','client', )
    list_filter = ('assign_to_2d_designer','assign_to_3d_designer','viewer','technical_user')
    search_fields = ('uuid',)
# Register your models here.
admin.site.register(Project,ProjectAdmin)
admin.site.register(WallDecorations)
admin.site.register(DesignStyle)
admin.site.register(CeilingDecoration)
admin.site.register(LightingType)
admin.site.register(DesignColors)
admin.site.register(FlooringMaterial)
admin.site.register(Furniture)
admin.site.register(HightWindow)
admin.site.register(ClientOpenToMakeEdit)
admin.site.register(PlumbingEstablished)
admin.site.register(CeilingGypsumBoard)
admin.site.register(DoorProvided)
admin.site.register(CeramicExisted)
admin.site.register(ToiletType)
admin.site.register(Heater)
admin.site.register(Comment)
admin.site.register(ProjectBasic,ProjectBasicAdmin)
admin.site.register(ProjectFile)
admin.site.register(ProjectImage)
admin.site.register(Comment_image)
admin.site.register(ProjectDetails)
admin.site.register(SiteEng)
admin.site.register(SitesManager)
admin.site.register(Buyer)
admin.site.register(Moshtrayat)
admin.site.register(Floor)
admin.site.register(Step)
admin.site.register(ProjectStudy)
admin.site.register(Feedback)
admin.site.register(Reply)
admin.site.register(FeedbackFloor)
admin.site.register(ReplyFloor)
admin.site.register(StepImage)
