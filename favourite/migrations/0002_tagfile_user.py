# Generated by Django 4.0.3 on 2022-05-22 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_root_file'),
        ('favourite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagfile',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.user'),
            preserve_default=False,
        ),
    ]
