# Generated by Django 3.2.12 on 2022-06-04 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20220604_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='information',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]
