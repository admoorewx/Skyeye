# Generated by Django 4.1.3 on 2022-12-10 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_lat_alter_profile_lon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(blank=True, default=9999),
            preserve_default=False,
        ),
    ]