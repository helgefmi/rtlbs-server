# Generated by Django 2.0.3 on 2019-04-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_auto_20190213_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='link',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='run',
            name='emulated',
            field=models.NullBooleanField(),
        ),
    ]
