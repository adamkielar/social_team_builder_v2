# Generated by Django 3.0.5 on 2020-04-14 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200413_2231'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainskill',
            old_name='skill_name',
            new_name='main_skill',
        ),
        migrations.RenameField(
            model_name='otherskill',
            old_name='skill_name',
            new_name='other_skill',
        ),
        migrations.RemoveField(
            model_name='userproject',
            name='slug',
        ),
    ]
