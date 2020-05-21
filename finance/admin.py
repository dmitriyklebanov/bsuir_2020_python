from django.contrib import admin

from finance.models import Balance, Expense, Payment

admin.site.register(Balance)
admin.site.register(Payment)


def safe_delete_expenses(_, request, queryset):
    for expense in queryset:
        expense.delete()


safe_delete_expenses.short_description = 'Safe delete selected expenses'


class ExpenseAdmin(admin.ModelAdmin):
    actions = [safe_delete_expenses, ]


admin.site.register(Expense, ExpenseAdmin)
