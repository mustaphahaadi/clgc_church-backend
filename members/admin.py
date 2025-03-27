from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contact
from .models import Member


admin.site.register(Contact)
admin.site.register(Member)