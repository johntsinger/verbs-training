# from unittest.mock import patch

# from django.contrib.auth import get_user_model
# from django.shortcuts import redirect
# from django.test import TestCase
# from django.urls import reverse_lazy, reverse

# from authentication.views import (
#     SignUpView,
#     AccountView,
#     UsernameChangeView,
#     EmailChangeView,
#     DeleteAccountView
# )
# from common.testcase.mixins import RequestFactoryMixin


# User = get_user_model()


# class TestDataMixin:
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(
#             username='user',
#             email='user@email.com',
#             password='password'
#         )
#         cls.inactive_user = User.objects.create_user(
#             username='inactive_user',
#             email='inactive_user@email.com',
#             password='password',
#             is_active=False
#         )
#         cls.user2 = User.objects.create_user(
#             username='user2',
#             email='user2@email.com',
#             password='password'
#         )


# class TestSignupView(
#     TestDataMixin,
#     RequestFactoryMixin,
#     TestCase
# ):
#     view_class = SignUpView
#     url = reverse_lazy('signup')

#     def test_dispatch_get_raise_error_if_success_url_point_to_signup_page(
#         self
#     ):
#         error_message = (
#             "Redirection loop for authenticated user detected."
#             "Check that your LOGIN_REDIRECT_URL doesn't point "
#             "to a signup page."
#         )

#         request = self.factory.get(self.url)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)
#         # change success url to point to the signup page
#         view.success_url = self.url

#         with self.assertRaises(
#             ValueError,
#             msg=error_message
#         ):
#             view.dispatch(request)

#     @patch(
#         'authentication.views.redirect',
#         autospec=True,
#         side_effect=redirect
#     )
#     def test_dispatch_get_redirect_autenticated_user_to_login_redirect_url(
#         self,
#         mock_redirect
#     ):
#         request = self.factory.get(self.url)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)

#         view.dispatch(request)

#         mock_redirect.assert_called_once_with(view.success_url)

#     def test_post_form_valid_logs_user_in(self):
#         data = {
#             'email': 'newuser@email.com',
#             'username': 'newuser',
#             'password1': 'wxcv1234',
#             'password2': 'wxcv1234'
#         }
#         request = self.factory.post(self.url, data=data)
#         self.setUp_messages(request)

#         view = self.view_class()
#         view.setup(request)

#         form = view.get_form()

#         with patch('authentication.views.login') as mock:
#             view.form_valid(form)
#         mock.assert_called_once_with(
#             request,
#             view.object,
#             backend='authentication.backends.EmailBackend'
#         )


# class TestAccountView(
#     TestDataMixin,
#     RequestFactoryMixin,
#     TestCase
# ):
#     view_class = AccountView
#     url = reverse_lazy('account')

#     def test_get_object_returns_current_authenticated_user(self):
#         request = self.factory.get(self.url)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)

#         obj = view.get_object()
#         self.assertEqual(obj, self.user)

#     def test_get_previous_page_url_returns_http_referer(self):
#         request = self.factory.get(self.url)
#         request.user = self.user
#         request.META = {'HTTP_REFERER': reverse('tables-list')}

#         view = self.view_class()
#         view.setup(request)

#         previous_page_url = view.get_previous_page_url()
#         self.assertEqual(previous_page_url, request.META.get('HTTP_REFERER'))

#     def test_get_previous_page_url_returns_previous_page_url(self):
#         request = self.factory.get(self.url)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)

#         previous_page_url = view.get_previous_page_url()
#         self.assertEqual(previous_page_url, view.previous_page_url)


# class TestUsernameChangeView(
#     TestDataMixin,
#     RequestFactoryMixin,
#     TestCase
# ):
#     view_class = UsernameChangeView
#     url = reverse_lazy('change-username')

#     def test_get_object_returns_current_authenticated_user(self):
#         request = self.factory.get(self.url)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)

#         obj = view.get_object()
#         self.assertEqual(obj, self.user)


# class TestEmailChangeView(
#     TestDataMixin,
#     RequestFactoryMixin,
#     TestCase
# ):
#     view_class = EmailChangeView
#     url = reverse_lazy('change-email')

#     def test_get_object_returns_current_authenticated_user(self):
#         request = self.factory.get(self.url)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)

#         obj = view.get_object()
#         self.assertEqual(obj, self.user)


# class TestDeleteAccountView(
#     TestDataMixin,
#     RequestFactoryMixin,
#     TestCase
# ):
#     view_class = DeleteAccountView
#     url = reverse_lazy('delete-account')

#     def test_get_object_returns_current_authenticated_user(self):
#         request = self.factory.get(self.url)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)

#         obj = view.get_object()
#         self.assertEqual(obj, self.user)

#     def test_get_form_kwargs_contains_current_user(self):
#         data = {
#             'email': 'user@email.com',
#             'password': 'password'
#         }
#         request = self.factory.post(self.url, data=data)
#         request.user = self.user

#         view = self.view_class()
#         view.setup(request)

#         kwargs = view.get_form_kwargs()
#         self.assertIn('current_user', kwargs)
#         self.assertEqual(kwargs['current_user'], self.user)

#     def test_form_valid_sends_messages(self):
#         message_expected = 'Your account has been sucessfully deleted !'
#         data = {
#             'email': 'user@email.com',
#             'password': 'password'
#         }
#         request = self.factory.post(self.url, data=data)
#         request.user = self.user
#         self.setUp_messages(request)

#         view = self.view_class()
#         view.setup(request)
#         view.object = view.get_object()

#         form = view.get_form()
#         form.cleaned_data = data
#         with patch('authentication.views.messages.error') as mock:
#             view.form_valid(form)
#         mock.assert_called_once_with(request, message_expected)
