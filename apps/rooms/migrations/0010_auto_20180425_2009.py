# Generated by Django 2.0.3 on 2018-04-25 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0009_auto_20180425_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomtime',
            name='idle',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
