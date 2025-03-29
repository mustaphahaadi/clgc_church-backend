from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    GENDER = (
        ("male","Male"),
        ("male","Female"),
    )

    middle_name = models.CharField(max_length=25,null=True,blank=True)
    telephone = models.CharField(max_length=12,null=False)
    country_code = models.CharField(max_length=5,null=False,blank=False,default="+233")
    gender = models.CharField(max_length=6,choices=GENDER,null=False)
    
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)