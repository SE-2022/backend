# Generated by Django 4.0.3 on 2022-05-10 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='isPerson',
            field=models.BooleanField(default=False),
        ),
    ]
