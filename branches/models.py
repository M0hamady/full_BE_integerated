from django.db import models
import uuid 

# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=100)
    slack = models.CharField(max_length=100,null=True,blank=True)
    uuid = models.UUIDField( editable=False, unique=True,verbose_name="secret_key")
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# branch manger
