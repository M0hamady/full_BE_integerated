import uuid
from django.conf import settings 
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User, Permission
from project.models import SiteEng, SitesManager

from teamview.models import Viewer

# Create your models here.
class Manager(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

        
class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Provide a custom related_name
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Provide a custom related_name
        related_query_name='user'
    )

    def is_manager(self):
        try:
            manager = Manager.objects.get(user=self)
            return True
        except :
            return False
    def is_viewer(self):
        try:
            viewer = Viewer.objects.get(user=self)
            # return True
        except:
            return False
        if viewer:
            return True
    def is_branchManager(self):
        try:
            viewer = SitesManager.objects.get(user=self)
            # return True
        except :
            return False
        if viewer.is_manager and viewer.is_active and viewer.branch:
            return True
    def is_branchEng(self):
        try:
            viewer = SiteEng.objects.get(user=self)
            # return True
        except :
            return False
        if viewer.is_active and viewer.branch:
            return True
    def is_designer(self):
        try:
            viewer = SiteEng.objects.get(user=self)
            # return True
        except :
            return False
        if viewer.is_active and viewer.branch:
            return True
        
        
# class GuidelineContent(models.Model):
#     message = models.CharField(max_length=1000, blank=True, null=True)
#     is_seen = models.BooleanField(default=False)
#     is_finished = models.BooleanField(default=False)
#     manager = models.ForeignKey('GuidanceManager', on_delete=models.CASCADE)

# class GuidanceManager(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     engineers = models.on(User, related_name='guid_line_content', blank=True, through='Guideline')

#     def send_guidelines(self, message):
#         guideline = GuidelineContent.objects.create(message=message, manager=self)

#     def get_engineers(self):
#         return self.engineers.all()

#     def get_guidelines(self):
#         return GuidelineContent.objects.filter(manager =self)

#     def mark_guideline_as_seen(self, guideline_id):
#         guideline = self.get_guidelines.filter(id=guideline_id).first()
#         if guideline:
#             guideline.is_seen = True
#             guideline.save()

#     def mark_guideline_as_finished(self, guideline_id):
#         guideline = GuidelineContent.objects.get(id=guideline_id)
#         if guideline:
#             guideline.is_finished = True
#             guideline.save()

#     def count_finished_guidelines(self):
#         return self.get_guidelines().filter(is_finished=True).count()

#     def calculate_finished_percentage(self):
#         total_guidelines = self.get_guidelines().count()
#         if total_guidelines > 0:
#             finished_guidelines = self.count_finished_guidelines()
#             percentage = (finished_guidelines / total_guidelines) * 100
#             return percentage
#         return 0