# Generated by Django 2.0.3 on 2019-02-08 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0005_auto_20190208_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
