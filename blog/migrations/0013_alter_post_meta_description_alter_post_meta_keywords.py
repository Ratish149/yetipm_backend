# Generated by Django 5.1.3 on 2025-01-29 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_post_meta_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='meta_description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='meta_keywords',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
