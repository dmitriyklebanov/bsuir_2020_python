from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from finance.models import Balance, Expense


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


class ExpenseUpdateView(UsersUpdateView):
    model = Expense
    fields = ['name']


class ExpenseDeleteView(UsersDeleteView):
    model = Expense
    success_url = reverse_lazy('expense_list')
