# Generated by Django 3.1.6 on 2021-02-20 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210219_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='joined',
        ),
    ]
