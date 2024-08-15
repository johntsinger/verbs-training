from unittest.mock import patch

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase  # override_settings
from django.urls import reverse_lazy, reverse

from authentication.tests.fixtures import TestDataFixture
from authentication.views import (
    SignUpView,
    LoginView,
    AccountView,
    UsernameChangeView,
    EmailChangeView,
    DeleteAccountView
)
from common.testcase.mixins import RequestFactoryMixin


class TestSignupView(
    TestDataFixture,
    RequestFactoryMixin,
    TestCase
):
    url = reverse_lazy('signup')

    def test_form_valid_logs_user_in(self):
        data = {
            'email': 'newuser@email.com',
            'username': 'newuser',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        request = self.factory.post(self.url, data=data)
        self.setUp_messages(request)

        view = SignUpView()
        view.setup(request)

        form = view.get_form()

        with patch('authentication.views.login') as mock:
            view.form_valid(form)
            mock.assert_called_once_with(request, view.object)

    def test_get_annonymous_user(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()

        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_get_authenticated_user_redirects_to_login_redirect_url(self):
        request = self.factory.get(self.url)
        request.user = self.user

        response = SignUpView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(settings.LOGIN_REDIRECT_URL)
        )


class TestLoginView(
    TestDataFixture,
    RequestFactoryMixin,
    TestCase
):
    url = reverse_lazy('login')

    def test_get_annonymous_user(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()

        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_get_authenticated_user_redirects_to_login_redirect_url(self):
        request = self.factory.get(self.url)
        request.user = self.user

        response = LoginView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse(settings.LOGIN_REDIRECT_URL)
        )


class TestAccountView(
    TestDataFixture,
    RequestFactoryMixin,
    TestCase
):
    url = reverse_lazy('account')

    def test_get_object_returns_current_authenticated_user(self):
        request = self.factory.get(self.url)
        request.user = self.user

        view = AccountView()
        view.setup(request)

        obj = view.get_object()
        self.assertEqual(obj, self.user)

    def test_get_previous_page_url_returns_http_referer(self):
        request = self.factory.get(self.url)
        request.user = self.user
        request.META = {'HTTP_REFERER': reverse('tables-list')}

        view = AccountView()
        view.setup(request)

        previous_page_url = view.get_previous_page_url()
        self.assertEqual(previous_page_url, request.META.get('HTTP_REFERER'))

    def test_get_previous_page_url_returns_previous_page_url(self):
        request = self.factory.get(self.url)
        request.user = self.user

        view = AccountView()
        view.setup(request)

        previous_page_url = view.get_previous_page_url()
        self.assertEqual(previous_page_url, view.previous_page_url)


class TestUsernameChangeView(
    TestDataFixture,
    RequestFactoryMixin,
    TestCase
):
    url = reverse_lazy('change-username')

    def test_get_object_returns_current_authenticated_user(self):
        request = self.factory.get(self.url)
        request.user = self.user

        view = UsernameChangeView()
        view.setup(request)

        obj = view.get_object()
        self.assertEqual(obj, self.user)

    # def test_get_context_data_contains_title(self):
    #     request = self.factory.get(self.url)
    #     request.user = self.user

    #     view = UsernameChangeView()
    #     view.setup(request, object=None)
    #     view.object = view.get_object()

    #     context = view.get_context_data()
    #     self.assertIn('title', context)
    #     self.assertEqual(context['title'], 'Change my username')


class TestEmailChangeView(
    TestDataFixture,
    RequestFactoryMixin,
    TestCase
):
    url = reverse_lazy('change-email')

    def test_get_object_returns_current_authenticated_user(self):
        request = self.factory.get(self.url)
        request.user = self.user

        view = EmailChangeView()
        view.setup(request)

        obj = view.get_object()
        self.assertEqual(obj, self.user)

    # def test_get_context_data_contains_title(self):
    #     request = self.factory.get(self.url)
    #     request.user = self.user

    #     view = EmailChangeView()
    #     view.setup(request, object=None)
    #     view.object = view.get_object()

    #     context = view.get_context_data()
    #     self.assertIn('title', context)
    #     self.assertEqual(context['title'], 'Change my email')
