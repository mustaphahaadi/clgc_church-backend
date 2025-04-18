from django.db import models
from datetime import timedelta
from django.utils import timezone
def event_image_dir(instance,filename):
    return f"media/events/{filename}"

# Create your models here.
class Events(models.Model):
    title = models.CharField(max_length=255,null=False)
    location = models.CharField(max_length=255,null=False)
    date = models.DateField(default=timezone.now())
    time = models.TimeField(default=timedelta(minutes=5))
    description = models.TextField()
    category = models.CharField(max_length=255,null=False)
    image = models.ImageField(upload_to=event_image_dir,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title