# Generated by Django 4.1 on 2022-09-27 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_children', '0002_migrate_children'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='children',
            name='adopt_date',
        ),
        migrations.RemoveField(
            model_name='children',
            name='adopter',
        ),
        migrations.RemoveField(
            model_name='children',
            name='presenter',
        ),
        migrations.AlterField(
            model_name='children',
            name='join_date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 9, 27, 19, 54, 42, 805327), null=True),
        ),
    ]
