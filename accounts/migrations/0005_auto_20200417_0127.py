# Generated by Django 3.0.5 on 2020-04-17 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200416_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]