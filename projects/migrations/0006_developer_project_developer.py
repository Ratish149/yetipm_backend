# Generated by Django 5.1.3 on 2024-12-24 06:30

import django.db.models.deletion
import projects.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_document_options_project_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('website', models.URLField(blank=True)),
                ('details', models.TextField(blank=True)),
                ('logo', models.FileField(blank=True, upload_to='developer_logos/')),
            ],
            bases=(projects.models.SlugMixin, models.Model),
        ),
        migrations.AddField(
            model_name='project',
            name='developer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.developer'),
        ),
    ]
