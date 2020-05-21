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
    name = models.CharField(max_length=30, unique=True)
    amount = models.FloatField(validators=[MaxValueValidator(MAX_VALUE), MinValueValidator(0)])
    currency = models.CharField(max_length=5, default='USD', choices=CURRENCY_CHOICES)

    def __str__(self):
        return f'{self.account.username}_{self.name}'

    def get_absolute_url(self):
        return reverse('balance_detail', kwargs={'pk': self.pk})


class Expense(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense')
    name = models.CharField(max_length=30, unique=True)
    amount = models.FloatField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f'{self.account.username}_{self.name}'

    def get_absolute_url(self):
        return reverse('expense_detail', kwargs={'pk': self.pk})

    def get_default(self):
        return Expense.objects.get_or_create(account=self.account, name='other')[0]

    def delete(self):
        obj = self.get_default()
        obj.amount += self.amount
        obj.save()

        payments = Payment.objects.filter(expense=self)
        for payment in payments:
            payment.expense = self.get_default()
            payment.save()

        super().delete()


class Payment(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment')

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    amount = models.FloatField(validators=[
        MaxValueValidator(Balance.MAX_VALUE), MinValueValidator(0)])
    balance = models.ForeignKey(Balance, on_delete=models.CASCADE, related_name='payment')
    expense = models.ForeignKey(Expense, on_delete=models.DO_NOTHING, related_name='payment')

    def delete(self):
        self.expense.amount -= self.amount
        self.expense.amount.save()
        super().delete()
