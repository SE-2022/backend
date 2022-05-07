# Generated by Django 3.2.12 on 2022-05-07 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_send_time', models.DateTimeField(auto_now_add=True)),
                ('msg_contend', models.TextField()),
                ('msg_isRead', models.BooleanField(default=False)),
                ('msg_userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]