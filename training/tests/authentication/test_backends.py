from django.contrib.auth import authenticate, get_user_model, get_user
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import TestCase, override_settings


User = get_user_model()


class TestDataMixin:
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
            email='user@email.com',
            password='password'
        )
        cls.inactive_user = User.objects.create_user(
            username='inactive_user',
            email='inactive_user@email.com',
            password='password',
            is_active=False
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            email='user2@email.com',
            password='password'
        )


class TestEmailBackend(TestDataMixin, TestCase):

    def test_authenticate_email_none(self):
        self.assertIsNone(authenticate(password='password'))

    def test_authenticate_email_or_password_none(self):
        self.assertIsNone(authenticate(email='user@email.com'))

    def test_authenticate_incorrect_email(self):
        self.assertIsNone(
            authenticate(email='incorrect@email.com', password='pasword')
        )

    def test_authenticate_incorrect_password(self):
        self.assertIsNone(
            authenticate(email='user@email.com', password='incorrect')
        )

    def test_authenticate_inactive_user(self):
        self.assertIsNone(
            authenticate(email='inactive_user@email.com', password='password')
        )

    def test_authenticate_success(self):
        self.assertEqual(
            authenticate(email='user@email.com', password='password'),
            self.user
        )

    def test_get_user(self):
        self.client.force_login(self.user)
        request = HttpRequest()
        request.session = self.client.session
        user = get_user(request)
        self.assertEqual(user, self.user)

    def test_get_user_inactive(self):
        self.client.force_login(self.inactive_user)
        request = HttpRequest()
        request.session = self.client.session
        user = get_user(request)
        self.assertIsInstance(user, AnonymousUser)

    def test_get_user_does_not_exist(self):
        self.client.force_login(self.user2)
        request = HttpRequest()
        request.session = self.client.session
        self.user2.delete()
        user = get_user(request)
        self.assertIsInstance(user, AnonymousUser)


@override_settings(
    AUTHENTICATION_BACKENDS=[
        'authentication.backends.AllowAllUsersEmailBackend'
    ]
)
class TestAllowAllUsersEmailBackend(TestDataMixin, TestCase):

    def test_authenticate_inactive_user(self):
        self.assertFalse(self.inactive_user.is_active)
        self.assertEqual(
            authenticate(email='inactive_user@email.com', password='password'),
            self.inactive_user
        )

    def test_get_user_inactive_user(self):
        self.client.force_login(self.inactive_user)
        request = HttpRequest()
        request.session = self.client.session
        user = get_user(request)
        self.assertEqual(user, self.inactive_user)
