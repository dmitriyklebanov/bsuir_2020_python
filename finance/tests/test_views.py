from django.contrib.auth.models import User
from django.test import RequestFactory

from django.urls import reverse

import pytest

from finance.views import BalancesListView


@pytest.mark.django_db
class TestListView:
    def test_balance_list_view(self):
        url = reverse('balances')

        request = RequestFactory().get(url)
        user = User.objects.create(username='tmp', email='tmp@example.com')
        request.user = user

        response = BalancesListView.as_view()(request)

        assert response.status_code == 200
