# Generated by Django 5.1.1 on 2025-01-29 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_alter_userprofile_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='adharcard',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]
