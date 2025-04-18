from django.db import models
from user.models import CustomUser

# Create your models here.
class PrayerRequest(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False)
    description = models.TextField()
    author = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    prayer_count = models.IntegerField(default=0)
    isAnswered = models.BooleanField(default=False)
    isPrivate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
