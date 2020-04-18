# Generated by Django 3.0.5 on 2020-04-18 16:01

from django.db import migrations, models
import django.db.models.deletion
import markdownx.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('description', markdownx.models.MarkdownxField(default='', max_length=2500)),
                ('project_timeline', models.TextField(default='')),
                ('applicant_requirements', models.TextField(default='', max_length=2500)),
                ('project_status', models.CharField(blank=True, choices=[('OPEN', 'Open'), ('CLOSED', 'Closed')], max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='accounts.Profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255)),
                ('description', markdownx.models.MarkdownxField(default='')),
                ('position_status', models.CharField(blank=True, choices=[('APPLY', 'Apply'), ('FILLED', 'Filled')], max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('main_skill', models.ManyToManyField(related_name='positions_main', to='accounts.MainSkill')),
                ('other_skill', models.ManyToManyField(related_name='positions_other', to='accounts.OtherSkill')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_status', models.CharField(blank=True, choices=[('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('UNDECIDED', 'Undecided')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_applicants', to='projects.Position')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_applicants', to='projects.Project')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='accounts.Profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
