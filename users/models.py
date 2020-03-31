from django.contrib.auth.models import User
from django.db import models

from PIL import Image
from phone_field.models import PhoneField

from financial_manager.settings import MEDIA_DEFAULT

import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = PhoneField(blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

    image = models.ImageField(
        default=os.path.join(MEDIA_DEFAULT, 'profile_image.jpg'),
        upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)