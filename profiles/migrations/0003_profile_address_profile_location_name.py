# Generated by Django 4.1.3 on 2022-12-10 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_email_alter_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(default=9999, max_length=240),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='location_name',
            field=models.CharField(default='None', max_length=120),
            preserve_default=False,
        ),
    ]
