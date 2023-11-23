from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Viewer(models.Model):
    name = models.CharField(max_length = 150)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


