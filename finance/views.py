from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from finance.forms import PaymentForm
from finance.models import Balance, Expense, Payment


class UsersCreateView(LoginRequiredMixin, CreateView):
    template_name = 'finance/form.html'

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['name'] = self.model._meta.model_name.capitalize()
        return res


class UsersListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(account=self.request.user)


class UsersDetailView(LoginRequiredMixin, DetailView):
    def get_object(self):
        obj = super().get_object()
        if obj.account != self.request.user:
            raise PermissionDenied
        return obj


class UsersUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'finance/form.html'

    def form_valid(self, form):
        form.instance.account = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().account == self.request.user

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['name'] = self.model._meta.model_name.capitalize()
        return res


class UsersDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'finance/confirm_delete.html'

    def test_func(self):
        return self.get_object().account == self.request.user

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['name'] = self.model._meta.model_name
        res['detail_url'] = self.model._meta.model_name + '_detail'
        return res


class BalanceListView(UsersListView):
    model = Balance


class BalanceCreateView(UsersCreateView):
    model = Balance
    fields = ['name', 'amount', 'currency']


class BalanceDetailView(UsersDetailView):
    model = Balance

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['payment_list'] = Payment.objects.filter(balance=res['object']).order_by('-datetime')
        return res


class BalanceUpdateView(UsersUpdateView):
    model = Balance
    fields = ['name', 'amount']


class BalanceDeleteView(UsersDeleteView):
    model = Balance
    success_url = reverse_lazy('balance_list')


class ExpenseListView(UsersListView):
    model = Expense


class ExpenseCreateView(UsersCreateView):
    model = Expense
    fields = ['name']


class ExpenseDetailView(UsersDetailView):
    model = Expense

    def get_context_data(self, **kwargs):
        res = super().get_context_data(**kwargs)
        res['payment_list'] = Payment.objects.filter(expense=res['object']).order_by('-datetime')
        return res


class ExpenseUpdateView(UsersUpdateView):
    model = Expense
    fields = ['name']


class ExpenseDeleteView(UsersDeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')


class PaymentListView(UsersListView):
    model = Payment

    def get_queryset(self):
        return super().get_queryset().order_by('-datetime')


class PaymentCreateView(UsersCreateView):
    model = Payment
    form_class = PaymentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.balance.amount -= form.instance.amount
        form.instance.balance.save()
        return super().form_valid(form)


class PaymentDetailView(UsersDetailView):
    model = Payment


class PaymentUpdateView(UsersUpdateView):
    model = Payment
    fields = ['title', 'description', 'expense']


class PaymentDeleteView(UsersDeleteView):
    model = Payment
    success_url = reverse_lazy('payment_list')
