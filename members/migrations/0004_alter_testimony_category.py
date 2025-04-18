# Generated by Django 5.1.6 on 2025-04-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0003_rename_testimony_testimony_content_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testimony",
            name="category",
            field=models.CharField(
                choices=[
                    ("healing", "Healing"),
                    ("salvation", "Salvation"),
                    ("deliverance", "Deliverance"),
                    ("provision", "Provision"),
                    ("breakthrough", "breakthrough"),
                    ("other", "Other"),
                ],
                max_length=100,
            ),
        ),
    ]
