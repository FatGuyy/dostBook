# Generated by Django 4.2.2 on 2023-09-09 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='file',
        ),
    ]
