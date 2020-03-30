from django.contrib.auth.models import User
from django.db import models

from financial_manager.settings import MEDIA_DEFAULT

import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default=os.path.join(MEDIA_DEFAULT, 'profile_image.jpg'),
        upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
