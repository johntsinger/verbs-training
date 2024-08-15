# from django.test import TestCase  # override_settings
# from django.urls import reverse_lazy, reverse
# from django.contrib.auth import get_user_model, get_user


# User = get_user_model()


# class BaseTestCase(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(
#             email='user@email.com',
#             password='password',
#             username='username'
#         )


# class TestSignupView(BaseTestCase):
#     url = reverse_lazy('signup')

#     def get_newuser_data(self):
#         return {
#             'email': 'newuser@email.com',
#             'username': 'newuser',
#             'password1': 'wxcv1234',
#             'password2': 'wxcv1234'
#         }

#     def test_templates_used(self):
#         template = 'authentication/signup.html'
#         response = self.client.get(self.url)
#         self.assertTemplateUsed(response, template)

#     def test_get_signup_page(self):
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code,
#             200
#         )

#     def test_get_signup_page_redirect_if_user_is_authenticated(self):
#         self.client.login(
#             email='user@email.com',
#             password='password'
#         )
#         response = self.client.get(self.url)
#         self.assertRedirects(response, reverse('account'))

#     def test_post_valid_data_creates_new_user(self):
#         user_count = User.objects.count()
#         self.client.post(
#             self.url,
#             data=self.get_newuser_data()
#         )
#         self.assertEqual(user_count + 1, User.objects.count())

#     def test_post_valid_data_log_user_in(self):
#         self.client.post(
#             self.url,
#             data=self.get_newuser_data()
#         )
#         user = get_user(self.client)
#         self.assertTrue(user.is_authenticated)

#     def test_post_valid_data_redirects_to_verbs_list_page(self):
#         response = self.client.post(
#             self.url,
#             data=self.get_newuser_data()
#         )
#         self.assertRedirects(response, reverse('verbs-list'))

#     def test_post_invalid_data(self):
#         user_count = User.objects.count()
#         invalid_data = {
#             'email': '',
#             'username': '',
#             'password1': '',
#             'password2': ''
#         }
#         response = self.client.post(
#             self.url,
#             data=invalid_data
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(user_count, User.objects.count())


# class TestLoginView(BaseTestCase):
#     url = reverse_lazy('login')

#     def test_templates_used(self):
#         template = 'authentication/login.html'
#         response = self.client.get(self.url)
#         self.assertTemplateUsed(response, template)

#     def test_get_login_page(self):
#         response = self.client.get(self.url)
#         self.assertEqual(
#             response.status_code,
#             200
#         )

#     def test_get_login_page_redirects_if_user_is_authenticated(self):
#         self.client.login(
#             email='user@email.com',
#             password='password'
#         )
#         response = self.client.get(self.url)
#         self.assertRedirects(response, reverse('verbs-list'))


# class TestAccountView(BaseTestCase):
#     pass
