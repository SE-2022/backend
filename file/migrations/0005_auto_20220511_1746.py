# Generated by Django 3.2.12 on 2022-05-11 09:46

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('file', '0004_alter_file_teamid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='CommentID',
            new_name='commentID',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='FileID',
            new_name='fileID',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='TeamID',
            new_name='teamID',
        ),
    ]
