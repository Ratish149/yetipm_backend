# Generated by Django 5.1.3 on 2025-02-09 06:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_inquiry_lease_term_inquiry_move_in_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='postal_code',
            new_name='zip_code',
        ),
    ]
