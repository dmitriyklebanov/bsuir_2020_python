from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory
from django.urls import reverse

import pytest

from finance.models import Balance
from finance.views import BalancesListView, BalanceDetailView


@pytest.mark.django_db
class TestListView:
    def test_balance_list_view(self):
        url = reverse('balances')

        request = RequestFactory().get(url)
        user = User.objects.create(username='tmp', email='tmp@example.com')
        request.user = user

        response = BalancesListView.as_view()(request)

        assert response.status_code == 200

    def test_balance_detail_view(self):
        user1 = User.objects.create(username='tmp1')
        user2 = User.objects.create(username='tmp2')
        balance = Balance.objects.create(account=user2, name='42', amount=34)

        url = reverse('balance_detail', kwargs={'pk': balance.id})

        request = RequestFactory().get(url)
        request.user = user1

        with pytest.raises(PermissionDenied):
            BalanceDetailView.as_view()(request, pk=balance.id)
