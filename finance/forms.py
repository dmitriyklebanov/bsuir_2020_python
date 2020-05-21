from django import forms
from django.core.exceptions import ValidationError

from .models import Balance, Expense, Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['balance'].queryset = Balance.objects.filter(account=user)
        self.fields['expense'].queryset = Expense.objects.filter(account=user)

    class Meta:
        model = Payment
        fields = ['title', 'description', 'amount', 'balance', 'expense']

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        balance = cleaned_data.get('balance')
        payment_amount = cleaned_data.get('amount')
        if payment_amount > balance.amount:
            raise ValidationError('Payment amount should be less or equal balance amount!')
        return cleaned_data
