from django.db import models
from django.utils import timezone
from .custom_user_model import CustomUser

class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class Testimony(models.Model):
    CATEGORY_CHOICES = [
        ('healing', 'Healing'),
        ('salvation', 'Salvation'),
        ('deliverance', 'Deliverance'),
        ('provision', 'Provision'),
        ('other', 'Other')
    ]
    
    def testimony_image_path(instance, filename):
        # Generate a dynamic path based on user and category
        username = 'anonymous' if not instance.user else instance.user.username
        return f'testimonies/{username}/{instance.category}/{filename}'
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    testimony = models.TextField()
    image = models.ImageField(upload_to=testimony_image_path, null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.category} testimony by {self.user.username if self.user else 'Anonymous'}"
    
    class Meta:
        verbose_name_plural = "Testimonies"
        ordering = ['-created_at']