from django.db import models
import uuid
# Create your models here.
class Technical(models.Model):
    name = models.CharField(max_length = 150)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)