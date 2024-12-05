from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.forms.fields import Field, EmailField
from django.test import TestCase, override_settings
from django.utils.text import capfirst

from training.authentication.forms import (
    LoginForm,
    SignUpForm,
    UsernameChangeForm,
    EmailChangeForm,
    DeleteAccountForm
)


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


class TestLoginForm(TestDataMixin, TestCase):
    form_class = LoginForm

    def test_email_field_max_length_matches_user_model(self):
        form = self.form_class()
        self.assertEqual(form.fields['email'].max_length, 254)
        self.assertEqual(form.fields['email'].widget.attrs['maxlength'], 254)

    def test_email_field_label(self):
        class CustomLoginForm(self.form_class):
            email = EmailField(label='Test')

        form = CustomLoginForm()
        self.assertEqual(form.fields['email'].label, 'Test')

    def test_email_field_label_not_set(self):
        class CustomLoginForm(self.form_class):
            email = EmailField()

        form = CustomLoginForm()
        email_field = User._meta.get_field(User.EMAIL_FIELD)
        self.assertEqual(
            form.fields['email'].label,
            capfirst(email_field.verbose_name)
        )

    def test_normalize_email_domain(self):
        data_expected = 'user@email.com'
        data = {
            'email': 'user@EMAIL.COM',
            'password': 'password'
        }
        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], data_expected)

    def test_success(self):
        data = {
            'email': 'user@email.com',
            'password': 'password'
        }
        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.non_field_errors(), [])

    def test_email_does_not_exists(self):
        data = {
            'email': 'does_not_exists@email.com',
            'password': 'password'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            [form.error_messages.get('invalid_login')]
        )

    def test_invalid_email(self):
        data = {
            'email': 'invalid_email',
            'password': 'password'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [EmailValidator.message]
        )

    def test_blank_email(self):
        """Email is required."""
        data = {
            'email': '',
            'password': 'password'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_incorrect_password(self):
        data = {
            'email': 'user@email.com',
            'password': 'incorrect_password'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            [form.error_messages.get('invalid_login')]
        )

    def test_blank_password(self):
        """Password is required."""
        data = {
            'email': 'user@email.com',
            'password': ''
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['password'].errors,
            [Field.default_error_messages.get('required')]
        )

    # Use an authentication backend that allows inactive users,
    # as EmailBackend rejects inactive users.
    @override_settings(
        AUTHENTICATION_BACKENDS=[
            'training.authentication.backends.AllowAllUsersEmailBackend'
        ]
    )
    def test_inactive_user_error(self):
        """
        Login as an inactive user with a backend that allows inactive
        users should raise inactive error.
        """
        data = {
            'email': 'inactive_user@email.com',
            'password': 'password'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            [form.error_messages.get('inactive')]
        )

    def test_inactive_user_display_invalid_login_instead_of_inactive(self):
        """
        Login as an inactive user with a backend that does not allows
        inactive users should raise invalid_login error.
        """
        data = {
            'email': 'inactive_user@email.com',
            'password': 'password'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            [form.error_messages.get('invalid_login')]
        )

    def test_get_invalid_login_error(self):
        error = self.form_class().get_invalid_login_error()
        self.assertIsInstance(error, ValidationError)
        self.assertEqual(
            error.message,
            'Please enter a correct email and password. Note that both '
            'fields may be case-sensitive.',
        )
        self.assertEqual(error.code, 'invalid_login')


class TestSingupForm(TestDataMixin, TestCase):
    form_class = SignUpForm

    def test_email_help_text(self):
        form = self.form_class()
        self.assertEqual(
            form.fields['email'].help_text,
            'Required. 254 characters of fewer. Must be a valid email address.'
        )

    def test_success(self):
        data = {
            'username': 'new_user',
            'email': 'new_user@email.com',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.non_field_errors(), [])

    def test_normalize_email_domain(self):
        # The normalization happens in AbstractUser.clean() and ModelForm
        # validation calls Model.clean().
        data_expected = 'new_user@email.com'
        data = {
            'username': 'new_user',
            'email': 'new_user@EMAIL.COM',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, data_expected)

    def test_normalize_username(self):
        # The normalization happens in AbstractBaseUser.clean() and ModelForm
        # validation calls Model.clean().
        ohm_username = "testΩ"  # U+2126 OHM SIGN
        data = {
            "username": ohm_username,
            "email": 'new_user@email.com',
            "password1": "wxcv1234",
            "password2": "wxcv1234",
        }
        form = self.form_class(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertNotEqual(user.username, ohm_username)
        # U+03A9 GREEK CAPITAL LETTER OMEGA
        self.assertEqual(user.username, "testΩ")

    def test_empty_email(self):
        """Email is required."""
        data = {
            'username': 'new_user',
            'email': '',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_blank_username(self):
        """Username is required."""
        data = {
            'username': '',
            'email': 'new_user@email.com',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_blank_password1(self):
        """Password1 is required."""
        data = {
            'username': 'new_user',
            'email': 'new_user@email.com',
            'password1': '',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['password1'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_blank_password2(self):
        """Password2 is required."""
        data = {
            'username': 'new_user',
            'email': 'new_user@email.com',
            'password1': 'wxcv1234',
            'password2': ''
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['password2'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_email_already_exists(self):
        data = {
            'username': 'new_user',
            'email': 'user@email.com',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [User._meta.get_field('email').error_messages.get('unique')]
        )

    def test_email_uppercase_already_exists(self):
        """
        Signup with an email whose user part is in uppercase should
        raise unique email error if this email already exists in
        lowercase.
        """
        data = {
            'username': 'new_user',
            'email': 'USER@EMAIL.COM',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [User._meta.get_field('email').error_messages.get('unique')]
        )

    def test_username_already_exists(self):
        data = {
            'username': 'user',
            'email': 'new_user@email.com',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [User._meta.get_field('username').error_messages.get('unique')]
        )

    def test_username_upercase_already_exists(self):
        """
        Signup with an uppercase username should raise unique
        error if this username already exists in lowercase.
        """
        data = {
            'username': 'USER',
            'email': 'new_user@email.com',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [User._meta.get_field('username').error_messages.get('unique')]
        )

    def test_invalid_email(self):
        data = {
            'username': 'new_user',
            'email': 'user',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [EmailValidator.message]
        )

    def test_invalid_username(self):
        data = {
            'username': '(# invalid &)',
            'email': 'new_user@email',
            'password1': 'wxcv1234',
            'password2': 'wxcv1234'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [UnicodeUsernameValidator.message]
        )

    def test_password_mismatch_error(self):
        data = {
            'username': 'new_user',
            'email': 'new_user@email.com',
            'password1': 'wxcv1234',
            'password2': '1234wxcv'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['password2'].errors,
            [form.error_messages.get('password_mismatch')]
        )

    def test_get_unique_email_error(self):
        error = self.form_class().get_unique_email_error()
        self.assertIsInstance(error, ValidationError)
        self.assertEqual(
            error.message,
            User._meta.get_field('email').error_messages.get('unique'),
        )
        self.assertEqual(error.code, 'unique_email')


class TestUsernameChangeForm(TestDataMixin, TestCase):
    form_class = UsernameChangeForm

    def test_username_help_text(self):
        form = self.form_class(instance=self.user)
        self.assertEqual(
            form.fields['username'].help_text,
            'Required. 150 characters or fewer. Letters, digits '
            'and @/./+/-/_ only.'
        )

    def test_initial_value(self):
        form = self.form_class(instance=self.user)
        self.assertEqual(form.initial.get('username'), self.user.username)

    def test_success(self):
        data = {
            'username': 'new_username'
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.non_field_errors(), [])

    def test_normalize_username(self):
        # The normalization happens in AbstractBaseUser.clean() and ModelForm
        # validation calls Model.clean().
        ohm_username = "testΩ"  # U+2126 OHM SIGN
        data = {
            "username": ohm_username
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertNotEqual(user.username, ohm_username)
        # U+03A9 GREEK CAPITAL LETTER OMEGA
        self.assertEqual(user.username, "testΩ")

    def test_blank_username(self):
        """Username is required."""
        data = {
            'username': ''
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_username_already_exists(self):
        data = {
            'username': 'user2',
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [User._meta.get_field('username').error_messages.get('unique')]
        )

    def test_username_upercase_already_exists(self):
        """
        Change username with an uppercase username should raise unique
        error if this username already exists in lowercase.
        """
        data = {
            'username': 'USER2',
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [User._meta.get_field('username').error_messages.get('unique')]
        )

    def test_invalid_username(self):
        data = {
            'username': '(# invalid &)',
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['username'].errors,
            [UnicodeUsernameValidator.message]
        )

    def test_get_unique_username_error(self):
        error = self.form_class().get_unique_username_error()
        self.assertIsInstance(error, ValidationError)
        self.assertEqual(
            error.message,
            User._meta.get_field('username').error_messages.get('unique'),
        )
        self.assertEqual(error.code, 'unique_username')


class TestEmailChangeForm(TestDataMixin, TestCase):
    form_class = EmailChangeForm

    def test_email_help_text(self):
        form = self.form_class(instance=self.user)
        self.assertEqual(
            form.fields['email'].help_text,
            'Required. 254 characters of fewer. Must be a valid email address.'
        )

    def test_initial_value(self):
        form = self.form_class(instance=self.user)
        self.assertEqual(form.initial.get('email'), self.user.email)

    def test_success(self):
        data = {
            'email': 'new@email.com'
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.non_field_errors(), [])

    def test_normalize_email_domain(self):
        # The normalization happens in AbstractUser.clean() and ModelForm
        # validation calls Model.clean().
        data_expected = 'new@email.com'
        data = {
            'email': 'new@EMAIL.COM'
        }
        form = self.form_class(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.email, data_expected)

    def test_blank_email(self):
        """Email is required."""
        data = {
            'email': ''
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_email_already_exists(self):
        data = {
            'email': 'user2@email.com',
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [User._meta.get_field('email').error_messages.get('unique')]
        )

    def test_email_uppercase_already_exists(self):
        """
        An email whose user part is in uppercase should
        raise unique email error if this email already exists in
        lowercase.
        """
        data = {
            'email': 'USER2@EMAIL.COM'
        }
        form = self.form_class(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [User._meta.get_field('email').error_messages.get('unique')]
        )

    def test_invalid_email(self):
        data = {
            'email': 'invalid_email',
        }
        form = self.form_class(instance=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [EmailValidator.message]
        )

    def test_get_unique_email_error(self):
        error = self.form_class().get_unique_email_error()
        self.assertIsInstance(error, ValidationError)
        self.assertEqual(
            error.message,
            User._meta.get_field('email').error_messages.get('unique'),
        )
        self.assertEqual(error.code, 'unique_email')


class TestDeleteAccountForm(TestDataMixin, TestCase):
    form_class = DeleteAccountForm

    def test_email_field_max_length_matches_user_model(self):
        form = self.form_class()
        self.assertEqual(form.fields['email'].max_length, 254)
        self.assertEqual(form.fields['email'].widget.attrs['maxlength'], 254)

    def test_email_field_label(self):
        class CustomDeleteAccountForm(self.form_class):
            email = EmailField(label='Test')

        form = CustomDeleteAccountForm()
        self.assertEqual(form.fields['email'].label, 'Test')

    def test_email_field_label_not_set(self):
        class CustomDeleteAccountForm(self.form_class):
            email = EmailField()

        form = CustomDeleteAccountForm()
        email_field = User._meta.get_field(User.EMAIL_FIELD)
        self.assertEqual(
            form.fields['email'].label,
            capfirst(email_field.verbose_name)
        )

    def test_normalize_email_domain(self):
        data_expected = 'user@email.com'
        data = {
            'email': 'user@EMAIL.COM',
            'password': 'password'
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], data_expected)

    def test_success(self):
        data = {
            'email': 'user@email.com',
            'password': 'password'
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.non_field_errors(), [])

    def test_email_does_not_exists(self):
        data = {
            'email': 'does_not_exists@email.com',
            'password': 'password'
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            [form.error_messages.get('invalid_credentials')]
        )

    def test_invalid_email(self):
        data = {
            'email': 'invalid_email',
            'password': 'password'
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [EmailValidator.message]
        )

    def test_blank_email(self):
        """Email is required."""
        data = {
            'email': '',
            'password': 'password'
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['email'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_incorrect_password(self):
        data = {
            'email': 'user@email.com',
            'password': 'incorrect_password'
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            [form.error_messages.get('invalid_credentials')]
        )

    def test_blank_password(self):
        """Password is required."""
        data = {
            'email': 'user@email.com',
            'password': ''
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form['password'].errors,
            [Field.default_error_messages.get('required')]
        )

    def test_use_credentials_of_another_existing_user(self):
        data = {
            'email': self.user2.email,
            'password': 'password'
        }
        form = self.form_class(current_user=self.user, data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(),
            [form.error_messages.get('invalid_credentials')]
        )

    def test_get_invalid_credentials_error(self):
        error = self.form_class().get_invalid_credentials_error()
        self.assertIsInstance(error, ValidationError)
        self.assertEqual(
            error.message,
            'Please enter a correct email and password. Note that both '
            'fields may be case-sensitive.',
        )
        self.assertEqual(error.code, 'invalid_credentials')
