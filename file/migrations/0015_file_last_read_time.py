# Generated by Django 3.2.12 on 2022-06-08 17:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0014_file_is_fav'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='last_read_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
