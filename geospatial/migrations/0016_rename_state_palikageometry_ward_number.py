# Generated by Django 4.1 on 2024-04-08 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geospatial', '0015_palikageometry_extra_json'),
    ]

    operations = [
        migrations.RenameField(
            model_name='palikageometry',
            old_name='state',
            new_name='ward_number',
        ),
    ]
