# Generated by Django 5.1.3 on 2025-01-10 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_developer_project_developer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='documents',
        ),
        migrations.RemoveField(
            model_name='project',
            name='plans',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='price_ending_at',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='project',
            name='developer',
        ),
        migrations.RemoveField(
            model_name='project',
            name='lot_size',
        ),
        migrations.RemoveField(
            model_name='project',
            name='price_starting_from',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_video_url',
        ),
        migrations.RemoveField(
            model_name='project',
            name='status',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
    ]