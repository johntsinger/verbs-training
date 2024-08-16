from django.contrib.auth.models import AnonymousUser
from django.test import TestCase  # override_settings
from django.urls import reverse_lazy

from common.testcase.mixins import RequestFactoryMixin
from verbs.tests.fixtures import TestDataFixture
from verbs.views import VerbListView


class TestVerbsViews(
    TestDataFixture,
    RequestFactoryMixin,
    TestCase
):
    url = reverse_lazy('verbs-list')

    def test_get_queryset_anonymous_user(self):
        """
        Test that get_queryset does not return a queryset annotated
        with the result (is_success) for an anonymous user.
        """
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        view = VerbListView()
        view.setup(request)
        queryset = view.get_queryset()

        with self.assertRaises(AttributeError):
            queryset.first().is_success

    def test_get_queryset_authenticated_user(self):
        """
        Test that get_queryset returns a queryset annotated
        with the result (is_success) for an authenticated user.
        """
        request = self.factory.get(self.url)
        request.user = self.user
        view = VerbListView()
        view.setup(request)
        queryset = view.get_queryset()

        self.assertTrue(queryset.first().is_success)
