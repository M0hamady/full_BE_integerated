from django.contrib import admin

from .models import *

class ProjectBasicInline(admin.TabularInline):
    model = ProjectBasic
    extra = 0
    can_delete = False
class ProjectStudyBasicInline(admin.TabularInline):
    model = ProjectStudy
    extra = 0
    can_delete = False

class ProjectBasicAdmin(admin.ModelAdmin):
    list_display = ('project', 'owner','meters',"uuid" )
    search_fields = ('uuid','project__location','project__meters','project__client__name')
    # list_editable = ('status',)
    
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectBasicInline,ProjectStudyBasicInline)
    list_display = ( 'uuid','client', 'ref_budget','total_price_study','project_percentage','total_price_study_and_percentage','branch')
    list_filter = ('assign_to_2d_designer','assign_to_3d_designer','viewer','technical_user','branch' )
    search_fields = ('uuid',)
from django.contrib import admin
from .models import ProjectImage2D

class StepInline(admin.TabularInline):
    model = Step
    extra = 1

class FloorAdmin(admin.ModelAdmin):
    inlines = [StepInline]
    list_display = ('name', 'project')
    list_filter = ('project', 'site_eng', 'site_manager')
    search_fields = ('name', 'project__name')
    # list_editable = ('name', 'project')

admin.site.register(Floor, FloorAdmin)
class StepAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor', 'status')
    list_filter = ('floor', 'status', 'start_date', 'end_date')
    search_fields = ('name', 'floor__name', 'floor__project__client__name', 'start_date', 'end_date')
    list_editable = ('status',)

admin.site.register(Step, StepAdmin)
class ProjectImage2DAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'created_at')
    list_filter = ('created_at','project')
    search_fields = ('name', 'project__client__uuid')
    # list_editable = ('name', 'project')

admin.site.register(ProjectImage2D, ProjectImage2DAdmin)
class CommentImage2DAdmin(admin.ModelAdmin):
    list_display = ('text', 'project_image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'project_image__name')
    # list_editable = ('text',)

admin.site.register(CommentImage2D, CommentImage2DAdmin)
class ProjectStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'price', 'measurement', 'count', 'total_price', 'start_date', 'end_date')
    list_filter = ('project', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    # list_editable = ('price', 'count','title','measurement','count','start_date','end_date')

admin.site.register(ProjectStudy, ProjectStudyAdmin)
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
# admin.site.register(ProjectImage2D)
admin.site.register(ProjectFile3D)
# admin.site.register(CommentImage2D)
admin.site.register(ReplyCommentImage2D)
admin.site.register(Buyer)
admin.site.register(Moshtrayat)
# admin.site.register(Floor)
# admin.site.register(Step)
# admin.site.register(ProjectStudy)
admin.site.register(Feedback)
admin.site.register(Reply)
admin.site.register(FeedbackFloor)
admin.site.register(ReplyFloor)
admin.site.register(StepImage)
