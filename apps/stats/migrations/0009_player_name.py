# Generated by Django 2.0.3 on 2019-02-13 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20190213_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='name',
            field=models.TextField(default='n/a'),
            preserve_default=False,
        ),
    ]
