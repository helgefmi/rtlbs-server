# Generated by Django 2.0.3 on 2018-04-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_roomtime_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtime',
            name='media',
            field=models.FileField(blank=True, upload_to='roomtime/'),
        ),
    ]
