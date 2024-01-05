from django.db import models
import uuid 

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField( editable=False, unique=True,verbose_name="secret_key")
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)


# branch manger
