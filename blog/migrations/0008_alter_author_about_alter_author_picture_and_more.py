# Generated by Django 5.1.3 on 2025-01-28 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_thumbnail_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='picture',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=300, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.tag'),
        ),
        migrations.AlterField(
            model_name='post',
            name='thumbnail_image_alt_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
