# Generated by Django 3.2.12 on 2022-06-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0015_file_last_read_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='last_read_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
