# Generated by Django 2.0.3 on 2018-04-25 19:35

from django.db import migrations, models
import server.apps.rooms.models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0008_auto_20180420_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtime',
            name='media',
            field=models.FileField(blank=True, upload_to=server.apps.rooms.models.media_file_name),
        ),
    ]
