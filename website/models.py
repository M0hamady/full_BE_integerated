import os
import uuid
from django.db import models
from django.conf import settings

# Create your models here.



class Section(models.Model):
    welcome_text = models.CharField( max_length=50)
    welcome_img = models.ImageField( upload_to="website/header/navigation", height_field=None, width_field=None, max_length=None)
    welcome_description = models.CharField( max_length=50,null=True,blank=True)
    def __str__(self):
        return self.welcome_text


    def get_welcome_img_url(self):
        if self.welcome_img:
            return settings.MEDIA_URL + str(self.welcome_img)
        return ""


class EmployeeWebsite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='employee_pictures')
    job_title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
from django.db.models.signals import pre_delete
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver

class Pic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pics/')
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        # Perform image resizing if needed
        self.resize_image()

        # Call the save method of the parent model to perform the default save behavior
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

@receiver(pre_delete, sender=Pic)
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