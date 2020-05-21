from django.contrib import admin

from finance.models import Balance, Expense, Payment

admin.site.register(Balance)
admin.site.register(Expense)
admin.site.register(Payment)
