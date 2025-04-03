from django.db import models
from user.models import CustomUser
from django.core.validators import FileExtensionValidator
from .validators import validate_vdieo_size
# Create your models here.
def mp3_sermon_directory(instance,filename):
    return f"sermons/mp3/{filename}"

def mp4_sermon_directory(instance,filename):
    return f"sermons/mp4/{filename}"

class Sermon(models.Model):
    title = models.CharField(max_length=50,null=False)
    description = models.TextField()
    speaker = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    mp3 = models.FileField(upload_to=mp3_sermon_directory,null=True,blank=True,validators=[
        FileExtensionValidator(allowed_extensions=["mp3"])
    ])
    video = models.FileField(upload_to=mp4_sermon_directory,null=True,blank=True,validators=[
        FileExtensionValidator(allowed_extensions=["mp4","avi"])
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title