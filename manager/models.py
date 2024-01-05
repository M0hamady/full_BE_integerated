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
        except Manager.DoesNotExist:
            return False
    def is_viewer(self):
        try:
            viewer = Viewer.objects.get(user=self)
            # return True
        except Viewer.DoesNotExist:
            return False
        if viewer:
            return True
    def is_branchManager(self):
        try:
            viewer = SitesManager.objects.get(user=self)
            # return True
        except SitesManager.DoesNotExist:
            return False
        if viewer.is_manager and viewer.is_active and viewer.branch:
            return True
    def is_branchEng(self):
        try:
            viewer = SiteEng.objects.get(user=self)
            # return True
        except SiteEng.DoesNotExist:
            return False
        if viewer.is_active and viewer.branch:
            return True