from datetime import datetime
from django.db import models
from django.core.validators import FileExtensionValidator
import uuid 
from multiselectfield import MultiSelectField
from project.forms import ColorChoicesFormField


class Project(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField( editable=False, unique=True,verbose_name="secret_key")
    client = models.ForeignKey("client.Client", verbose_name="project_owner", on_delete=models.SET_NULL,null=True,blank=True)
    assign_to_2d_designer = models.ForeignKey("designer.Designer", verbose_name="assigned_2d_designer", on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_2d_designer')
    assign_to_3d_designer = models.ForeignKey("designer.Designer", verbose_name="assigned_3d_designer", on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_3d_designer')
    viewer = models.ForeignKey("teamview.Viewer", verbose_name="project_viewer_from_team_viewer", on_delete=models.SET_NULL,null=True,blank=True,related_name='team_viewer')
    technical_user = models.ForeignKey("technical.Technical", verbose_name="project_technical", on_delete=models.SET_NULL,null=True,blank=True,related_name='technical_user_for_project')
    # technical_user
    # basicInfo = models.ForeignKey("ProjectBasic", verbose_name="project_basic_information", on_delete=models.SET_NULL,null=True,blank=True)
    # detailInfo = models.ForeignKey("ProjectBasic", verbose_name="project_in_detail_information", on_delete=models.SET_NULL,null=True,blank=True)
    # moshtrayat = models.ForeignKey("ProjectMoshtrayat", verbose_name="moshtrayat", on_delete=models.SET_NULL,null=True,blank=True)
    # basicInfo =
    is_client_approved_study = models.BooleanField(default=False) 
    is_client_approved_2d = models.BooleanField(default=False) 
    is_client_approved_3d = models.BooleanField(default=False) 
    is_finished = models.BooleanField(default=False)
    ref_budget = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.name
    @property
    def roadmap(self):
        floors = Floor.objects.filter(project=self)
        floors_data=[]
        for floor in floors:
            floor_data = {
                'floor_name': floor.name,
                'floor_uuid': floor.uuid,
                'site_eng': floor.site_eng.name if floor.site_eng else None,
                'steps_count': floor.steps_count(),
                'moshtrayat_budget': floor.calculate_budget(),
                'durations': f"{floor.calculate_duration()} days",
                'coming_durations': f"{floor.calculate_duration_coming()} days",
                'start_date': floor.start_date(),
                'end_date': floor.end_date(),
                'feedbacks': floor.get_feedbacks(),
                'pic': [re for image in floor.all_images() for re in image],
            }
            floors_data.append(floor_data)
        
        return floors_data
    
    @property
    def study(self):
        studies = ProjectStudy.objects.filter(project=self)
        studies_data=[]
        for study in studies:
            study_data = {
                'study_name': study.title,
                'description': study.description,
                'measurement': study.measurement,
                'count': study.count,
                'price':study.price,
                'total_cost': study.total_price,
                'start_date': study.start_date,
                'end_date': study.end_date,
                'feedbacks': study.feedback_client.all().values("message","status",'created_at'),
                'uuid': study.uuid,
            }
            studies_data.append(study_data)
        
        return studies_data

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    @property
    def is_assigned_to_2d(self):
        if self.assign_to_2d_designer:
            return True
        else: return False
    @property
    def is_assigned_to_3d(self):
        if self.assign_to_3d_designer:
            return True
        else: return False
    @property
    def project_works_percentage(self):
        all_floors =Floor.objects.filter(project =self)
        total_conditions = all_floors.count()
        completed_conditions = 0
        print(all_floors)
        for each_floor in all_floors:
            print(each_floor.calculate_percentage_finished())
            if each_floor.calculate_percentage_finished() >0:
                completed_conditions += each_floor.calculate_percentage_finished() / 100 

        if total_conditions >0:
            return (completed_conditions / total_conditions) * 100
        return 0
    @property
    def basic_data_percentage(self):
        return ProjectBasic.objects.get(project = self).project_basic_percentage()

# data in details
class WallDecorations(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class DesignStyle(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class CeilingDecoration(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class LightingType(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class DesignColors(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class FlooringMaterial(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class Furniture(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class HightWindow(models.Model):
    name = models.CharField( max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
# finished data in details adding comments to project
# starting one option choice
from django.db import models


class ClientOpenToMakeEdit(models.Model):
    CHOICES = [
        ("Yes", 'Yes'),
        ("No", 'No'),
    ]
    
    name = models.CharField(choices=CHOICES, max_length=10)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

class PlumbingEstablished(models.Model):
    CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    name = models.CharField(choices=CHOICES, max_length=10)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

class CeilingGypsumBoard(models.Model):
    CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    name = models.CharField(choices=CHOICES, max_length=10)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

class DoorProvided(models.Model):
    CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    name = models.CharField(choices=CHOICES, max_length=10)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

class CeramicExisted (models.Model):
    CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    
    name = models.CharField(choices=CHOICES, max_length=10)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class ToiletType(models.Model):
    name = models.CharField( max_length=20)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class Heater(models.Model):
    name = models.CharField( max_length=20)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
# end one option choice
# finished data in details adding comments to project
class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments_project')
    content = models.TextField()
    can_client_sea=models.BooleanField(default=False)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_client_project')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_project')
    designer = models.ForeignKey('designer.Designer', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_designer_project')
    viewer = models.ForeignKey('teamview.Viewer', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_viewer_project')
    technical = models.ForeignKey('technical.Technical', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_technical_project')
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
# this felid is for details of project comments 

class ProjectBasic(models.Model):
    project = models.ForeignKey(Project, verbose_name="project_basic", on_delete=models.SET_NULL,null=True,blank=True)
    location = models.CharField( max_length=550,null=True,blank=True,)
    dimensions = models.CharField( max_length=100,null=True,blank=True)
    meters = models.IntegerField(null=True,blank=True)
    design_styles = models.ManyToManyField(DesignStyle, verbose_name="design_styles",blank=True)
    design_colors = models.ManyToManyField(DesignColors, verbose_name="design_colors",blank=True)
    ceiling_decoration = models.ManyToManyField(CeilingDecoration, verbose_name="ceiling_decoration",blank=True)
    lighting_type = models.ManyToManyField(LightingType, verbose_name="lighting_type",blank=True)
    wall_decorations = models.ManyToManyField(WallDecorations, verbose_name="Wall_decorations",blank=True)
    flooring_material = models.ManyToManyField(FlooringMaterial, verbose_name="flooring_material",blank=True)
    furniture = models.ManyToManyField(Furniture, verbose_name="owner_furniture",blank=True)
    hight_window = models.CharField(max_length=20,null=True,blank=True)
    clientOpenToMakeEdit = models.ForeignKey(ClientOpenToMakeEdit, verbose_name="clientOpenToMakeEdit",on_delete=models.SET_NULL,null=True,blank=True)
    plumbingEstablished = models.ForeignKey(PlumbingEstablished, verbose_name="plumbingEstablished",on_delete=models.SET_NULL,null=True,blank=True)
    ceilingGypsumBoard = models.ForeignKey(CeilingGypsumBoard, verbose_name="ceilingGypsumBoard",on_delete=models.SET_NULL,null=True,blank=True)
    doorProvided = models.ForeignKey(DoorProvided, verbose_name="doorProvided",on_delete=models.SET_NULL,null=True,blank=True)
    ceramicExisted = models.ForeignKey(CeramicExisted, verbose_name="ceramicExisted",on_delete=models.SET_NULL,null=True,blank=True)
    toiletType = models.ForeignKey(ToiletType, verbose_name="toiletType",on_delete=models.SET_NULL,null=True,blank=True)
    heater = models.ForeignKey(Heater, verbose_name="heater",on_delete=models.SET_NULL,null=True,blank=True)
    is_add_fur_2d = models.BooleanField(verbose_name="do_you_want_to_add_furniture_?",default=True)
    is_boiler = models.BooleanField(verbose_name="is_there_any_boiler?",default=False)
    count_boiler = models.PositiveBigIntegerField(default=0,null=True)
    count_kids = models.PositiveBigIntegerField(default=0,null=True)
    count_kids_male = models.PositiveBigIntegerField(default=0,null=True)
    count_kids_female = models.PositiveBigIntegerField(default=0,null=True)
    count_rooms = models.PositiveBigIntegerField(default=0,null=True)
    uuid = models.UUIDField( editable=False, unique=True)
    
    def owner(self):
        try:
            return self.project.client.name
        except: return None 
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    def project_basic_percentage(self):
        total_conditions = 14
        completed_conditions = 0
        if self.location:
            completed_conditions += 1
        if self.dimensions:
            completed_conditions += 1
        if self.meters:
            completed_conditions += 1
        if self.design_styles:
            completed_conditions += 1
        if self.design_colors:
            completed_conditions += 1
        if self.ceiling_decoration:
            completed_conditions += 1
        if self.lighting_type:
            completed_conditions += 1
        if self.wall_decorations:
            completed_conditions += 1
        if self.flooring_material:
            completed_conditions += 1
        if self.furniture:
            completed_conditions += 1
        if self.hight_window:
            completed_conditions += 1
        if self.is_add_fur_2d:
            completed_conditions += 1
        if self.is_boiler:
            completed_conditions += 1
        if self.count_boiler:
            completed_conditions += 1
        return (completed_conditions / total_conditions) * 100

class Notes(models.Model):
    project_basic = models.ForeignKey(ProjectBasic, on_delete=models.SET_NULL,null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255)
    uuid = models.UUIDField( editable=False, unique=True)
    
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, verbose_name="project_file", on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField( max_length=50)
    file = models.FileField(upload_to='uploads/Files/')
    uuid = models.UUIDField( editable=False, unique=True)
    can_client_sea=models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

class ProjectFile3D(models.Model):
    project = models.ForeignKey(Project, verbose_name="project_file", on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField( max_length=50)
    file = models.FileField(upload_to='uploads/Files/')
    uuid = models.UUIDField( editable=False, unique=True)
    can_client_sea=models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

class ProjectImage2D(models.Model):
    project = models.ForeignKey(Project, verbose_name="project_file", on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField( max_length=50)
    image = models.ImageField(upload_to='uploads/images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])
    uuid = models.UUIDField( editable=False, unique=True)
    can_client_sea=models.BooleanField(default=False)   
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class CommentImage2D(models.Model):
    project_image = models.ForeignKey(ProjectImage2D, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField( editable=False, unique=True)
    
    def __str__(self):
        return self.text
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class ReplyCommentImage2D(models.Model):
    comment = models.ForeignKey(CommentImage2D, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField( editable=False, unique=True)
    
    def __str__(self):
        return self.text
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, verbose_name="project_file", on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField( max_length=50)
    image = models.ImageField(upload_to='uploads/images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])
    uuid = models.UUIDField( editable=False, unique=True)
    can_client_sea=models.BooleanField(default=False)   
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class CommentOptions(models.Model):
    project_basic = models.ForeignKey(ProjectBasic, on_delete=models.CASCADE, related_name='comments_options')
    comment = models.TextField()
    Key_option= models.CharField(max_length=20)
    created_by= models.CharField(max_length=40,null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_options')
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.content
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def is_reply(self):
        return self.parent is not None

class Comment_image(models.Model):
    image = models.ForeignKey(ProjectImage, on_delete=models.CASCADE, related_name='comments_images')
    content = models.TextField()
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, null=True, blank=True, related_name='replies_clients')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    designer = models.ForeignKey('designer.Designer', on_delete=models.CASCADE, null=True, blank=True, related_name='repliesDesignerS')
    viewer = models.ForeignKey('teamview.Viewer', on_delete=models.CASCADE, null=True, blank=True, related_name='repliesViewer')
    technical = models.ForeignKey('technical.Technical', on_delete=models.CASCADE, null=True, blank=True, related_name='repliesTechnical')
    uuid = models.UUIDField( editable=False, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    @property
    def owner(self):
        if self.designer:
            return self.designer
        elif self.viewer:
            return self.viewer
        elif self.technical:
            return self.technical
        elif self.client:
            return self.client

    def is_reply(self):
        return self.parent is not None
    
    def parent_uuid(self):
        if self.parent:
            return self.parent.uuid
        else:return None
    @property
    def is_reply_1(self):
        res = False
        if self.parent is not None:
            res = True
        return res
    
class ProjectDetails(models.Model):# not used yet
    colors=models.CharField( max_length=9)
    project = models.ForeignKey(Project, verbose_name="project_details", on_delete=models.SET_NULL,null=True,blank=True)
    uuid = models.UUIDField( editable=False, unique=True)
    can_client_sea=models.BooleanField(default=False)   
    def __str__(self) :
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class SiteEng(models.Model):
    name = models.CharField(max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)

    def get_floors_data(self):
        floors_data = []
        floors = self.floorEng.all()
        
        for floor in floors:
            floor_data = {
                'floor_name': floor.name,
                'site_manager': floor.site_manager.name if floor.site_manager else None,
                'moshtrayat_count': floor.steps.count(),
                'moshtrayat_budget': floor.calculate_budget(),
                'moshtrayat_duration': floor.calculate_duration(),
            }
            floors_data.append(floor_data)
        
        return floors_data
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class SitesManager(models.Model):
    name = models.CharField(max_length=50)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self) :
        return self.name
    def get_floors_data(self):
        floors_data = []
        floors = self.floorEng.all()
        
        for floor in floors:
            floor_data = {
                'floor_name': floor.name,
                'site_eng': floor.site_eng.name if floor.site_eng else None,
                'moshtrayat_count': floor.steps.count(),
                'moshtrayat_budget': floor.calculate_budget(),
                'moshtrayat_duration': floor.calculate_duration(),
            }
            floors_data.append(floor_data)
        
        return floors_data
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class Moshtrayat(models.Model):
    name = models.CharField(max_length=50)
    step_moshtrayat = models.ForeignKey('Step', on_delete=models.CASCADE, related_name='stepMoshtrayats')
    buyer = models.ForeignKey('Buyer', on_delete=models.CASCADE)
    price = models.FloatField(default=0.0)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.FloatField(default=0.0)
    delivered_to_site_eng = models.BooleanField(default=False)
    approved_buying = models.BooleanField(default=False)
    approved_delivery = models.BooleanField(default=False)
    approved_sending = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered_by_site_eng = models.BooleanField(null=True)
    ordered_by_site_manager = models.BooleanField(null=True)
    uuid = models.UUIDField( editable=False, unique=True)
    
    
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()

        self.total_cost = self.quantity * self.price
        super().save(*args, **kwargs)
class Buyer(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self) :
        return self.name
    def get_related_data(self):
        moshtrayat = Moshtrayat.objects.filter(buyer=self)
        return moshtrayat


    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class Floor(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project , on_delete=models.CASCADE)
    site_eng = models.ForeignKey(SiteEng, on_delete=models.SET_NULL, null=True, blank=True, related_name='floorEng')
    site_manager = models.ForeignKey(SitesManager, on_delete=models.SET_NULL, null=True, blank=True, related_name='floorEng')
    uuid = models.UUIDField( editable=False, unique=True)
    def all_images(self):
        res =Step.objects.filter(floor = self)
        test = [ ]
        for image in res:
            print(image.all_images(),5555555555555)
            if len(image.all_images()) > 0:
                test.append(image.all_images())
        return test
    def calculate_percentage_finished(self):
        total_steps = Step.objects.filter(floor = self).count()
        finished_steps = Step.objects.filter(floor = self, status='FINISHED').count()
        print((finished_steps / total_steps) * 100, "total")
        if total_steps > 0:
            return (finished_steps / total_steps) * 100
        else:
            return 0
    def steps_count(self):
        return Step.objects.filter(floor = self).count()
    def steps(self):
        return Step.objects.filter(floor = self)
    def calculate_budget(self):
        total_budget = 0.0
        for step in self.steps().all():
            total_budget += step.total_budget()
        return total_budget

    def calculate_duration(self):
        if self.steps:
            # Step 1: Retrieve all start dates for the steps
            start_dates = list(Step.objects.filter(floor=self).values_list('start_date', flat=True))
            
            # Step 2: Find the minimum start date
            min_start_date = min(start_dates)

            # Step 3: Retrieve all end dates for the steps
            end_dates = list(Step.objects.filter(floor=self).values_list('end_date', flat=True))
            print(end_dates)
            # Step 4: Find the maximum end date
            max_end_date = max(end_dates)
            print (min_start_date, max_end_date)
            if min_start_date and max_end_date:
                return (max_end_date - min_start_date).days
        return None
    def calculate_duration_coming(self):
    # Get the current date
        current_day = datetime.now().date()

        # Retrieve all end dates for the steps
        end_dates = list(Step.objects.filter(floor=self).values_list('end_date', flat=True))

        # Filter end dates that are greater than or equal to the current day
        upcoming_end_dates = [date for date in end_dates if date >= current_day]

        if upcoming_end_dates:
            # Find the maximum end date among the upcoming end dates
            max_end_date = max(upcoming_end_dates)

            # Calculate the duration from the current day to the maximum end date
            duration = (max_end_date - current_day).days
            return duration

        return None
    def start_date(self):
        start_dates = list(Step.objects.filter(floor=self).values_list('start_date', flat=True))
        
        # Step 2: Find the minimum start date
        min_start_date = min(start_dates)
        print(min_start_date.strftime('%Y-%m-%d'))
        return f"{min_start_date.strftime('%Y-%m-%d')}"
    def end_date(self):
        start_dates = list(Step.objects.filter(floor=self).values_list('end_date', flat=True))
        
        # Step 2: Find the minimum start date
        min_start_date = max(start_dates)
        print(min_start_date.strftime('%Y-%m-%d'))
        return f"{min_start_date.strftime('%Y-%m-%d')}"
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    def __str__(self) :
        return self.name
    def get_feedbacks(self):
        feedbacks = FeedbackFloor.objects.filter(floor=self).values("message", "status", "is_seen", "uuid")
        feedbacks_data = []
        # for feedback in feedbacks:
        #     feedback["replies"] = list(ReplyFloor.objects.filter(feedback_floor__uuid=feedback["uuid"]).values("message","site_manager","site_Eng","uuid"))
        #     feedbacks_data.append(feedback)
        return feedbacks_data
class ProjectStudy(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    price = models.IntegerField(blank=False, null=False)
    measurement = models.CharField(max_length=150)
    count = models.IntegerField(blank=False, null=False)
    total_price = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    feedback_client = models.ManyToManyField('Feedback', related_name='project_feedbacks',blank=True)
    uuid = models.UUIDField( editable=False, )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Calculate the total price based on the count and price
        self.total_price = self.count * self.price
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class FeedbackFloor(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    replies = models.ManyToManyField('ReplyFloor', related_name='feedbacks_floor', blank=True)
    process = 'process'
    finished = 'finished'
    STATUS_CHOICES = [
        (process, 'process'),
        (finished, 'finished'),
    ]
    is_accepted = models.BooleanField(default=True)
    is_seen = models.BooleanField(default=False)
    
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="process")
    uuid = models.UUIDField( editable=False, )

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    @property
    def get_all_reply(self):
        return ReplyFloor.objects.filter(feedback_floor = self)
class Feedback(models.Model):
    project_study = models.ForeignKey(ProjectStudy, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    replies = models.ManyToManyField('Reply', related_name='feedbacks_floor',blank=True,null=True)
    process = 'process'
    finished = 'finished'
    STATUS_CHOICES = [
        (process, 'process'),
        (finished, 'finished'),
    ]
    is_accepted = models.BooleanField(default=True)
    is_seen = models.BooleanField(default=False)
    is_process = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="process")
    uuid = models.UUIDField( editable=False, )

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    def get_current_action(self):
        if self.is_accepted and not self.is_seen:
            return 'Pending (Not Seen)'
        elif self.is_process  and not self.is_finished:
            return 'In Process'
        elif self.is_finished :
            return 'Finished'
        elif self.is_accepted and self.is_seen and not (self.is_process or self.is_finished):
            return 'In Negotiation'
        else:
            return 'Unknown'
class ReplyFloor(models.Model):
    feedback_floor = models.ForeignKey(FeedbackFloor, on_delete=models.CASCADE)
    site_Eng = models.ForeignKey(SiteEng, on_delete=models.SET_NULL, null=True, blank=True)
    site_manager = models.ForeignKey(SitesManager, on_delete=models.SET_NULL,null=True, blank=True)
    message = models.CharField(max_length=1000)
    uuid = models.UUIDField( editable=False, )
    created_at = models.DateField(auto_now=True,)
    
    def __str__(self):
        return self.message
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    
    
class Reply(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    site_manager = models.ForeignKey(SiteEng, on_delete=models.SET_NULL, null=True, blank=True)
    site_manager = models.ForeignKey(SitesManager, on_delete=models.SET_NULL,null=True, blank=True)
    message = models.CharField(max_length=1000)
    uuid = models.UUIDField( editable=False, )
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.message
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    


class Step(models.Model):
    name = models.CharField(max_length=250)
    taxes = models.FloatField(default=0.0)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    # moshtrayat = models.ForeignKey(Moshtrayat, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(auto_now=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, null=True, blank=True)
    CHOICE_TYPES = (
        ('PENDING', 'PENDING'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('FINISHED', 'FINISHED'),
    )
    status = models.CharField(max_length=250, choices=CHOICE_TYPES)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self) :
        return self.name + '_' + self.floor.name + '_' +self.floor.project.client.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    
    def all_images(self):
        z = StepImage.objects.filter(step = self)
        res =[]
        for x in z:
            res.append(x.get_image_url())
        return res
    def total_budget(self):
        total_budget  = 0
        moshtrayat = Moshtrayat.objects.filter(step_moshtrayat  =self)
        if moshtrayat : 
            for moshtra in moshtrayat:
                # print(moshtra.total_cost, "moshtra.price")
                total_budget += moshtra.total_cost
        return total_budget
class StepImage(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='step_images/')
    uuid = models.UUIDField( editable=False, unique=True)
    is_client_can_sea  = models.BooleanField(default=False)
     
    def __str__(self) :
        return self.step.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_image_url(self):
        return self.image.url