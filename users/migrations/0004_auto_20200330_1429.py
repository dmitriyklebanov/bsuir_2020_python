# Generated by Django 3.0.3 on 2020-03-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200330_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default/profile_image.jpg', upload_to='profile_pics'),
        ),
    ]
