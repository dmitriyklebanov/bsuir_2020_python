# Generated by Django 3.0.6 on 2020-05-21 08:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_auto_20200521_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='amount',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
