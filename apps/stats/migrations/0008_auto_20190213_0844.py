# Generated by Django 2.0.3 on 2019-02-13 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_remove_run_first_run_by_player'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='run',
            options={'ordering': ['date']},
        ),
        migrations.AlterField(
            model_name='run',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='run',
            name='status',
            field=models.TextField(db_index=True),
        ),
    ]