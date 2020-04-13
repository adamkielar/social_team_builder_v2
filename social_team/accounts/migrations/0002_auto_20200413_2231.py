# Generated by Django 3.0.5 on 2020-04-13 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(blank=True, choices=[('ANDROID_DEVELOPER', 'Android Developer'), ('DESIGNER', 'Designer'), ('IOS_DEVELOPER', 'IOS Developer'), ('JAVA_DEVELOPER', 'Java Developer'), ('PHP_DEVELOPER', 'PHP Developer'), ('PYTHON_DEVELOPER', 'Python Developer'), ('RAILS_DEVELOPER', 'Rails Developer'), ('WORDPRESS_DEVELOPER', 'Wordpress Developer'), ('OTHER', 'Other')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OtherSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=markdownx.models.MarkdownxField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('url', models.URLField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='main_skills',
            field=models.ManyToManyField(to='accounts.MainSkill'),
        ),
        migrations.AddField(
            model_name='user',
            name='other_skills',
            field=models.ManyToManyField(to='accounts.OtherSkill'),
        ),
    ]
