from datetime import datetime
import os
from django.db import models
from django.core.validators import FileExtensionValidator
import uuid 
from multiselectfield import MultiSelectField
from project.forms import ColorChoicesFormField
from project.slck import send_slack_notification
from supportconstruction import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.db.models.signals import pre_delete
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver
class Project(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField( editable=False, unique=True,verbose_name="secret_key")
    client = models.ForeignKey("client.Client", verbose_name="project_owner", on_delete=models.SET_NULL,null=True,blank=True)
    branch = models.ForeignKey("branches.Branch", verbose_name="project_Branch", on_delete=models.SET_NULL,null=True,blank=True)
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
    ref_budget = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    

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
    def total_price_study(self):
        all_projects_prices=ProjectStudy.objects.filter(project=self)
        return all_projects_prices.aggregate(total_price=models.Sum('price'))['total_price']  
    @property
    def project_percentage(self):
        try:
            percentage=self.client.company_percentage
            return f'{percentage}%' 
        except: return 0
    @property
    def total_price_study_and_percentage(self):
        try:
            percentage=self.client.company_percentage
            all_projects_prices = ProjectStudy.objects.filter(project=self).aggregate(total_price=models.Sum('price'))['total_price']
            if all_projects_prices:
                return all_projects_prices + all_projects_prices * (percentage / 100)
            else:
                return 0
        except:return 0
    @property
    def study(self):
        studies = ProjectStudy.objects.filter(project=self)
        total_cost = 0
        studies_data=[]
        for study in studies:
            total_cost += study.total_price
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
        studies = {
                'studies_data': studies_data,
                'total_cost': total_cost,
                'company_perc': None,
                'company_perc_and_total': None
            }

        try:
            studies['company_perc'] = self.client.company_percentage
            studies['company_perc_and_total'] = (total_cost * (self.client.company_percentage / 100)) + total_cost
        except AttributeError:
            pass
        return studies
    def branch_message(self):
        text = '''
    :heavy_plus_sign: New project added to your projects. Please follow the link below for more details:
    <https://www.backend.support-constructions.com/client/project/{0}/update/>
    '''.format(self.client.uuid)

        return text

    def branch_message_study(self):
        text = '''
    :clipboard: Perform a study using the link below:
    <https://www.backend.support-constructions.com/project-study/create/{0}/>
    '''.format(self.client.uuid)

        return text
    def get_project_update(self, old_project):
        update = f"*{self.client}* updated data at `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
        
        fields = self._meta.fields
        
        for field in fields:
            field_name = field.name
            old_value = getattr(old_project, field_name)
            new_value = getattr(self, field_name)
            
            if old_value != new_value:
                update += f"• *{field.verbose_name}:*\n    From: `{old_value}`\n    To: `{new_value}`\n"
        
        return update
    

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if self.pk:
            old_project = Project.objects.get(pk=self.pk)
            project_update = self.get_project_update(old_project)
            
            if project_update:
                send_slack_notification(self.branch.slack, project_update)
        if self.branch and not self.pk:
            send_slack_notification(self.branch.slack,self.branch_message())
            send_slack_notification(self.branch.slack,self.branch_message_study())
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
            return f'{int((completed_conditions / total_conditions) * 100)}'
        return '0'
    @property
    def project_works_percentage_needs_approve(self):
        all_floors =Floor.objects.filter(project =self)
        total_conditions = all_floors.count()
        completed_conditions = 0
        for each_floor in all_floors:
            if each_floor.calculate_percentage_finished_need_approved() > 0:
                    completed_conditions += each_floor.calculate_percentage_finished_need_approved() / 100 

        if total_conditions > 0:
            return f'{int((completed_conditions / total_conditions) * 100)}'
        return '0'
    @property
    def basic_data_percentage(self):
        return ProjectBasic.objects.get(project = self).project_basic_percentage()
    
    def get_floors(self):
        return Floor.objects.filter(project=self)
    
    def steps(self):
        return Step.objects.filter(floor__in=self.get_floors())

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
class Location_airconditioning(models.Model):
    name = models.CharField( max_length=20)
    uuid = models.UUIDField( editable=False, unique=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
class Electronics_kitchen(models.Model):
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
    count_airconditioning = models.PositiveBigIntegerField(default=0,null=True)
    location_airconditioning = models.ManyToManyField(Location_airconditioning, verbose_name="location_airconditioning",blank=True)
    electronics_kitchen = models.ManyToManyField(Electronics_kitchen, verbose_name="electronics_kitchen",blank=True)
    count_kids = models.PositiveBigIntegerField(default=0,null=True)
    count_family = models.PositiveBigIntegerField(default=0,null=True)
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
    
    def message_adding_new_pic(self):
        text = f'''
                تم اضافة صورة للعميل يرجي المراجعه علي الرابط التالي:
                https://www.backend.support-constructions.com/projects/{self.project.client.uuid}/images/

                '''
        return text
    def save(self, *args, **kwargs):
        if not self.uuid:
            send_slack_notification(self.project.branch.slack,self.message_adding_new_pic())
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    def resize_image(self):
        # Retrieve the uploaded image
        img = Image.open(self.image)

        # Set the maximum size to 6 megabytes (6 * 1024 * 1024 bytes)
        max_size = 1 * 1024 * 1024

        # Check if the image size exceeds the maximum size
        if self.image.size > max_size:
            # Calculate the new image dimensions to maintain the aspect ratio
            width, height = img.size
            aspect_ratio = width / height
            new_width = int((max_size * aspect_ratio) ** 0.5)
            new_height = int(max_size / ((max_size * aspect_ratio) ** 0.5))

            # Resize the image
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

            # Create a BytesIO object to temporarily hold the resized image data
            temp_buffer = BytesIO()
            img.save(temp_buffer, format='JPEG')

            # Create a new InMemoryUploadedFile with the resized image data
            self.image = InMemoryUploadedFile(
                temp_buffer,
                None,
                f"{self.image.name.split('.')[0]}.jpg",
                'image/jpeg',
                temp_buffer.tell(),
                None
            )
@receiver(pre_delete, sender=ProjectImage2D)
def delete_image_file(sender, instance, **kwargs):
    # Get the path to the image file
    try:
        image_path = instance.image.url
    except:
        try: image_path = instance.image
        except: image_path = instance.image.path
    # Check if the image file exists
    if os.path.exists(image_path):
        # Delete the image file
        os.remove(image_path)
class CommentImage2D(models.Model):
    project_image = models.ForeignKey(ProjectImage2D, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField( editable=False, unique=True)
    
    def __str__(self):
        return self.text
    
    def message_adding_new_pic_comment(self):
        text = f'''
                علق العميل علي الصورة باسم {self.project_image.name} :
                "{self.text}"
                يمكنك الرد علي الرابط التالي
                https://www.backend.support-constructions.com/projects/{self.project_image.project.client.uuid}/images/

                '''
        return text
    def save(self, *args, **kwargs):
        if not self.uuid:
            send_slack_notification(self.project_image.project.branch.slack,self.message_adding_new_pic_comment())
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
class SitesManager(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(editable=False, unique=True)
    branch = models.ForeignKey("branches.Branch", on_delete=models.SET_NULL,null=True,blank=True)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        branch = 'under training' if not self.branch else self.branch
        return f"{self.name}_{branch}"

class SiteEng(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(editable=False, unique=True)
    branch = models.ForeignKey("branches.Branch", on_delete=models.SET_NULL,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    def __str__(self):
        branch = 'under training' if not self.branch else self.branch
        return f"{self.name}_{branch}"


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
    def last_feed(self):
        return FeedbackFloor.objects.filter(floor=self).last()
    def calculate_percentage_finished(self):
        total_steps = self.steps_count()
        finished_steps = Step.objects.filter(
                Q(floor=self, status='FINISHED') | Q(floor=self, status='finished')
            ).count()
        if total_steps > 0 and finished_steps > 0:
            return (finished_steps / total_steps) * 100
        else:
            return 0
    def calculate_percentage_finished_need_approved(self):
        total_steps = self.steps_count()
        finished_steps = Step.objects.filter(
                 Q(floor=self, status='FINISHED')
            ).count()
        if total_steps > 0 and finished_steps > 0:
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
        try:
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
        except:return 0
    def calculate_duration_coming(self):
    # Get the current date
        current_day = datetime.now().date()

        # Retrieve all end dates for the steps
        end_dates = list(Step.objects.filter(floor=self).values_list('end_date', flat=True))

        # Filter end dates that are greater than or equal to the current day
        upcoming_end_dates = [date for date in end_dates if date is not None and date >= current_day]

        if upcoming_end_dates:
            # Find the maximum end date among the upcoming end dates
            max_end_date = max(upcoming_end_dates)

            # Calculate the duration from the current day to the maximum end date
            duration = (max_end_date - current_day).days
            return duration

        return None
    def start_date(self):
        start_dates = list(Step.objects.filter(floor=self).values_list('start_date', flat=True))
        start_dates = [date for date in start_dates if date is not None]
        if start_dates:
            min_start_date = min(start_dates)
            return min_start_date.strftime('%Y-%m-%d')
        else:
            return None

    def end_date(self):
        end_dates = list(Step.objects.filter(floor=self).values_list('end_date', flat=True))
        end_dates = [date for date in end_dates if date is not None]
        if end_dates:
            max_end_date = max(end_dates)
            return max_end_date.strftime('%Y-%m-%d')
        else:
            return None
    def generate_slack_message(self):
        message = f"""تمت إضافة بند جديد بنجاح: {self.name}/n/n لمشروع {self.project.name}"""
        return message

    def save(self, *args, **kwargs):
        try:
            if not self.uuid:
                if self.project.branch :
                    send_slack_notification(self.project.branch.slack,self.generate_slack_message())
                elif self.site_manager.branch:
                    send_slack_notification(self.site_manager.branch.slack,self.generate_slack_message())
                else: send_slack_notification("#new-customers",self.generate_slack_message())
        except:send_slack_notification("#new-customers",self.generate_slack_message())
        self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    def __str__(self) :
        return self.name + '_'+self.project.client.name
    def get_feedbacks(self):
        feedbacks = FeedbackFloor.objects.filter(floor=self).values("message", "status", "is_seen", "uuid")
        feedbacks_data = []
        # for feedback in feedbacks:
        #     feedback["replies"] = list(ReplyFloor.objects.filter(feedback_floor__uuid=feedback["uuid"]).values("message","site_manager","site_Eng","uuid"))
        #     feedbacks_data.append(feedback)
        return feedbacks_data
    def feedbacks(self):
        feedbacks = FeedbackFloor.objects.filter(floor=self)
       
        return feedbacks
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
        return self.title+ "_"+self.project.name
    def generate_slack_message(self):
        message_arabic = f"تمت إضافة دراسة جديدة '{self.title}' إلى المشروع '{self.project.name}'."
        message_english = f"A new study '{self.title}' has been added to the project '{self.project.name}'."
        
        message = f"Arabic (العربية):\n{message_arabic}\n\nEnglish:\n{message_english}\n\nurl: https://www.backend.support-constructions.com/project-study/create/{self.project.client.uuid}/"
        return message
    def save(self, *args, **kwargs):
        # Calculate the total price based on the count and price
        self.total_price = self.count * self.price
        if not self.uuid:
            if self.project.branch:
                send_slack_notification(self.project.branch.slack,self.generate_slack_message())
            else: send_slack_notification("#new-customers",self.generate_slack_message())
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)
    def get_feeds_with_replies(self):
        feeds = Feedback.objects.filter(project_study= self)
        result = []
        for feed in feeds:
            feed.is_seen =True
            feed.is_process= True
            feed.save()
            result.append({
                'feed':feed.message,
                'id':feed.id,
                'created_at':feed.created_at,
                'replies':feed.replies.all().values('id','message','uuid','created_at'),
                'uuid':feed.uuid,
                'uuid_target':'#'+f'{feed.uuid}',
            })
        return result
         
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
        message = "F "
        
        if self.project_study:
            message += self.project_study.project.name

        return message 
    def message_(self):
        message = f"*Message*: {self.message}\n"
        message += f"*Created At*: {self.created_at}\n"
        message += f"*Is Accepted*: {self.is_accepted}\n"
        message += f"*Is Seen*: {self.is_seen}\n"
        message += f"*Is Process*: {self.is_process}\n"
        message += f"*Is Finished*: {self.is_finished}\n"
        
        return message

    def save(self, *args, **kwargs):
        if not self.uuid:
            send_slack_notification("#customer-service",self.message_())
            send_slack_notification(self.project_study.project.branch.slack,self.message_())
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
    site_eng = models.ForeignKey(SiteEng, on_delete=models.SET_NULL, null=True, blank=True)
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
    
    @property
    def get_null_fields(self):
        null_fields = []
        if self.start_date is None:
            null_fields.append('تاريخ البدء')
        if self.end_date is None:
            null_fields.append('تاريخ الانتهاء')

        if null_fields:
            message = "الحقول التالية فارغة حاليًا: {}".format("، ".join(null_fields))
            message += "يرجى اتخاذ الإجراء المناسب."
        else:
            message = "لا توجد حقول فارغة شكرا لك."

        return message
    def get_step_update(self, old_project):
        update = f"*{self.name}* updated data at `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
        
        fields = self._meta.fields
        
        for field in fields:
            field_name = field.name
            old_value = getattr(old_project, field_name)
            new_value = getattr(self, field_name)
            
            if old_value != new_value:
                update += f"• *{field.verbose_name}:*\n    From: `{old_value}`\n    To: `{new_value}`\n"
        
        return update
    def save(self, *args, **kwargs):
        if self.pk:
            old_project = Step.objects.get(pk=self.pk)
            try:
                send_slack_notification(self.floor.project.branch.slack,self.get_step_update(old_project))
            except:pass
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
            try:
                send_slack_notification(self.step.floor.project.branch.slack,f"تم اضافة صورة الي {self.step.name}")
            except:pass
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def get_image_url(self):
        return self.image.url