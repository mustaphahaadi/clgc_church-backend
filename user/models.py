from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    GENDER = (
        ("male","Male"),
        ("female","Female"),
    )

    middle_name = models.CharField(max_length=25,null=True,blank=True)
    telephone = models.CharField(max_length=12,null=False)
    country_code = models.CharField(max_length=5,null=False,blank=False,default="+233")
    gender = models.CharField(max_length=6,choices=GENDER,null=False)
    profile_complete = models.BooleanField(default=False)

    # For otp
    activation_code = models.CharField(max_length=50,null=True,blank=True)
    otp_code = models.CharField(max_length=6,null=True,blank=True)
    
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

class Fellowship(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    description = models.TextField()
    leader = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)
    # activities = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Profile(models.Model):
    MARTIAL_STATUS = (
        ("married","Married"),
        ("single","Single"),
        ("divorced","Divorced"),
    )

    class Meta:
        app_label = 'members'
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    martial_status =  models.CharField(max_length=8,choices=MARTIAL_STATUS,null=True) # ADDED NEW FIELD
    visit_date = models.DateField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)
    house_address = models.TextField()
    digital_address = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100)
    church_information = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    fellowship = models.ForeignKey(Fellowship,on_delete=models.SET_NULL,null=True,blank=True)
    born_again = models.BooleanField(default=False) # ADDED NEW FIELD
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
