# Generated by Django 5.1.3 on 2025-01-14 10:44

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_tag_blog_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('picture', models.FileField(upload_to='')),
                ('about', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('category_image', models.FileField(blank=True, upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='name',
        ),
        migrations.AddField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(default='tag', max_length=200),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=500)),
                ('blog_duration_to_read', models.CharField(blank=True, max_length=100)),
                ('thumbnail_image', models.FileField(upload_to='')),
                ('thumbnail_image_alt_description', models.CharField(max_length=300)),
                ('blog_content', tinymce.models.HTMLField(blank=True)),
                ('meta_title', models.CharField(max_length=200)),
                ('meta_description', models.TextField()),
                ('meta_keywords', models.TextField(blank=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category')),
                ('tags', models.ManyToManyField(to='blog.tag')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
    ]
