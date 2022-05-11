# Generated by Django 3.2.12 on 2022-05-11 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0003_alter_file_teamid'),
        ('user', '0005_rename_root_dir_user_root_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='root_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file.file'),
        ),
    ]