from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Balance(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'United States Dollar'),
        ('EUR', 'Euro'),
        ('BYN', 'Belarusian Ruble'),
        ('RUS', 'Russian Ruble'),
    ]

    MAX_VALUE = 999999999999999

    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balance')
    name = models.CharField(max_length=30)
    amount = models.FloatField(validators=[MaxValueValidator(MAX_VALUE), MinValueValidator(0)])
    currency = models.CharField(max_length=5, default='USD', choices=CURRENCY_CHOICES)

    def __str__(self):
        return f'{self.account.username}_{self.name}'

    def get_absolute_url(self):
        return reverse('balance_detail', kwargs={'pk': self.pk})


class Expense(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense')
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.account.username}_{self.name}'
