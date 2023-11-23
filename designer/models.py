from django.db import models
import uuid 
from django.contrib.auth.models import User

# Create your models here.
class Designer(models.Model):
    name = models.CharField(max_length = 150)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4()
        super().save(*args, **kwargs)



class ChatBoot(models.Model):
    message = models.CharField(max_length = 150)
    response = models.TextField(max_length = 10000,null=True,blank=True)
    
    def __str__(self) -> str:
        res =""
        if self.response:
            res  = "has response"
        return self.message + ":>"+ res
class ChatState(models.Model):
    works = models.BooleanField(default=False)



    def __str__(self):
        if self.works:
            return "works"
        
        else:return "not works"
    