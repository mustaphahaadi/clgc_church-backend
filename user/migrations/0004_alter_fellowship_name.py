# Generated by Django 5.1.6 on 2025-04-02 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0003_customuser_profile_complete"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fellowship",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
