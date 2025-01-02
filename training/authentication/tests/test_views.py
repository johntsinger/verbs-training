import itertools
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.contrib.messages import constants
from django.contrib.messages.storage.base import Message
from django.contrib.messages.test import MessagesTestMixin
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from training.authentication.views import SignUpView

User = get_user_model()


class AssertionMixin:
    def assertContainsFormErrors(self, response, form):
        """Asserts that form errors are rendered in the template."""
        for error in list(itertools.chain(*form.errors.values())):
            with self.subTest(error=error):
                self.assertContains(response, error)


class AuthenticationViewsTestCase(AssertionMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user",
            email="user@email.com",
            password="password",
        )
        cls.inactive_user = User.objects.create_user(
            username="inactive_user",
            email="inactive_user@email.com",
            password="password",
            is_active=False,
        )
        cls.user2 = User.objects.create_user(
            username="user2",
            email="user2@email.com",
            password="password",
        )


class TestLoginView(AuthenticationViewsTestCase):
    url = reverse_lazy("authentication:login")

    def test_redirect_authenticated_users(self):
        """If logged in redirect to LOGIN_REDIRECT_URL."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_get(self):
        template_expected = "authentication/login.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post_valid_data(self):
        data = {"email": "user@email.com", "password": "password"}
        response = self.client.post(self.url, data=data)
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_post_invalid_data(self):
        data = {"email": "b@b.com", "password": "x"}
        response = self.client.post(self.url, data=data)
        user = get_user(self.client)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_authenticated)
        # Verify if errors are rendered in the template
        self.assertContainsFormErrors(response, response.context["form"])


class TestSignupView(MessagesTestMixin, AuthenticationViewsTestCase):
    url = reverse_lazy("authentication:signup")

    @patch.object(SignUpView, "success_url", url)
    def test_redirect_loop(self):
        error_message = (
            "Redirection loop for authenticated user detected."
            "Check that your LOGIN_REDIRECT_URL doesn't point "
            "to a signup page."
        )

        self.client.force_login(self.user)

        with self.assertRaisesMessage(ValueError, error_message):
            self.client.get(self.url)

    def test_redirect_authenticated_user(self):
        """If logged in redirect to LOGIN_REDIRECT_URL."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_get(self):
        template_expected = "authentication/signup.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post_valid_data(self):
        user_count = User.objects.count()
        data = {
            "email": "newuser@email.com",
            "username": "newuser",
            "password1": "wxcv1234",
            "password2": "wxcv1234",
        }
        expected_messages = [
            Message(constants.SUCCESS, "Your account was created successfully.")
        ]
        response = self.client.post(self.url, data=data, follow=True)
        user = get_user(self.client)
        self.assertEqual(user_count + 1, User.objects.count())
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))
        self.assertMessages(response, expected_messages)

    def test_post_invalid_data(self):
        user_count = User.objects.count()
        data = {
            "email": "",
            "username": "user2",
            "password1": "x",
            "password2": "x",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_count, User.objects.count())
        # Verify if errors are rendered in the template
        self.assertContainsFormErrors(response, response.context["form"])


class TestAccountView(AuthenticationViewsTestCase):
    url = reverse_lazy("authentication:account")

    def setUp(self):
        self.client.force_login(self.user)

    def test_redirect_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_URL) + f"?next={self.url}",
        )

    def test_get(self):
        template_expected = "authentication/account.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)


class TestUsernameChangeView(MessagesTestMixin, AuthenticationViewsTestCase):
    url = reverse_lazy("authentication:change-username")

    def setUp(self):
        self.client.force_login(self.user)

    def test_redirect_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_URL) + f"?next={self.url}",
        )

    def test_get(self):
        template_expected = "authentication/change.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post_valid_data(self):
        data = {
            "username": "newusername",
        }
        expected_messages = [
            Message(constants.SUCCESS, "Your username has been successfully updated.")
        ]
        response = self.client.post(self.url, data=data, follow=True)
        user = get_user(self.client)
        self.assertEqual(user.username, data["username"])
        self.assertRedirects(response, reverse("authentication:account"))
        self.assertMessages(response, expected_messages)

    def test_post_invalid_data(self):
        data = {"username": "user2"}
        response = self.client.post(self.url, data=data)
        user = get_user(self.client)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.username, "user")
        # Verify if errors are rendered in the template
        self.assertContainsFormErrors(response, response.context["form"])


class TestEmailChangeView(MessagesTestMixin, AuthenticationViewsTestCase):
    url = reverse_lazy("authentication:change-email")

    def setUp(self):
        self.client.force_login(self.user)

    def test_redirect_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_URL) + f"?next={self.url}",
        )

    def test_get(self):
        template_expected = "authentication/change.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post_valid_data(self):
        data = {
            "email": "new@email.com",
        }
        expected_messages = [
            Message(constants.SUCCESS, "Your email has been successfully updated.")
        ]
        response = self.client.post(self.url, data=data, follow=True)
        user = get_user(self.client)
        self.assertEqual(user.email, data["email"])
        self.assertRedirects(response, reverse("authentication:account"))
        self.assertMessages(response, expected_messages)

    def test_post_invalid_data(self):
        data = {"email": "invalid_email"}
        response = self.client.post(self.url, data=data)
        user = get_user(self.client)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.email, "user@email.com")
        # Verify if errors are rendered in the template
        self.assertContainsFormErrors(response, response.context["form"])


class TestDeleteAccountView(MessagesTestMixin, AuthenticationViewsTestCase):
    url = reverse_lazy("authentication:delete-account")

    def setUp(self):
        self.client.force_login(self.user)

    def test_redirect_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_URL) + f"?next={self.url}",
        )

    def test_get(self):
        template_expected = "authentication/delete.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post_valid_data(self):
        user_count = User.objects.count()
        data = {
            "email": "user@email.com",
            "password": "password",
        }
        expected_messages = [
            Message(constants.SUCCESS, "Your account has been sucessfully deleted.")
        ]
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(user_count - 1, User.objects.count())
        self.assertRedirects(response, reverse("authentication:login"))
        self.assertMessages(
            response,
            expected_messages,
        )

    def test_post_invalid_data(self):
        user_count = User.objects.count()
        data = {
            "email": "incorrect@email.com",
            "password": "incorrect_password",
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_count, User.objects.count())
        # Verify if errors are rendered in the template
        self.assertContainsFormErrors(response, response.context["form"])

    def test_get_form_kwargs_add_current_user_to_form(self):
        response = self.client.get(self.url)
        user = get_user(self.client)
        self.assertTrue(hasattr(response.context["form"], "current_user"))
        self.assertEqual(response.context["form"].current_user, user)
