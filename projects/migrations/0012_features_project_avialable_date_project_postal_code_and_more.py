# Generated by Django 5.1.3 on 2025-01-14 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_rename_name_inquiry_first_name_inquiry_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='avialable_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='price_breakdown',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='inquiry',
            name='inquiry_type',
            field=models.CharField(blank=True, choices=[('Specific Property', 'Specific Property'), ('General Inquiry', 'General Inquiry')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('Single Family', 'Single Family'), ('Condominium', 'Condominium'), ('Townhouse', 'Townhouse'), ('Duplex', 'Duplex'), ('Other', 'Other')], default='Single Family', max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='features',
            field=models.ManyToManyField(blank=True, to='projects.features'),
        ),
    ]
