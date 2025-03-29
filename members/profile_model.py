from django.db import models
from django.conf import settings
from user.models import CustomUser

class Profile(models.Model):
    class Meta:
        app_label = 'members'
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    visit_date = models.DateField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)
    house_address = models.TextField()
    digital_address = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100)
    church_information = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    fellowship = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        # Set profile_complete to True when profile is saved
        if not self.user.profile_complete:
            self.user.profile_complete = True
            self.user.save()
        super().save(*args, **kwargs)