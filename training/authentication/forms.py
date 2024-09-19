from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)',
                'autocomplete': 'email'
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': _(
            'Please enter a correct email and password. Note that both '
            'fields may be case-sensitive.'
        ),
        'inactive': _('This account is inactive.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "email" field.
        self.email_field = User._meta.get_field(User.EMAIL_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(
                self.email_field.verbose_name
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = User.objects.normalize_email(email)
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login'
        )


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
        help_texts = {
            'email': _(
                'Required. 254 characters of fewer. '
                'Must be a valid email address.'
            )
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (
            email
            and User.objects.filter(email__iexact=email).exists()
        ):
            raise self.get_unique_email_error()
        else:
            return email

    def get_unique_email_error(self):
        return ValidationError(
            User._meta.get_field('email').error_messages['unique'],
            code='unique_email'
        )


class UsernameChangeForm(forms.ModelForm):
    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)',
                'autocomplete': 'username'
            }
        ),
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits '
            'and @/./+/-/_ only.'
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if (
            username
            and User.objects.filter(
                username__iexact=username
            ).exclude(
                username=self.instance.username
            ).exists()
        ):
            raise self.get_unique_username_error()
        else:
            return username

    def get_unique_username_error(self):
        return ValidationError(
            User._meta.get_field('username').error_messages['unique'],
            code='unique_username'
        )


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)',
                'autocomplete': 'email'
            }
        ),
        help_text=_(
            'Required. 254 characters of fewer. Must be a valid email address.'
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and User.objects.filter(
                email__iexact=email
            ).exclude(
                email=self.instance.email
            ).exists()
        ):
            raise self.get_unique_email_error()
        else:
            return email

    def get_unique_email_error(self):
        return ValidationError(
            User._meta.get_field('email').error_messages['unique'],
            code='unique_email'
        )


class DeleteAccountForm(forms.Form):
    """
    Form to delete the account of the logged-in user.
    Requires email address and password to confirm deletion.
    """
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)',
                'autocomplete': 'email',
            }
        )
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'off'
            }
        ),
    )

    error_messages = {
        'invalid_credentials': _(
            'Please enter a correct email and password. Note that both '
            'fields may be case-sensitive.'
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "email" field.
        self.email_field = User._meta.get_field(User.EMAIL_FIELD)
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(
                self.email_field.verbose_name
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = User.objects.normalize_email(email)
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(email=email, password=password)
            if (
                self.user_cache is None
                or self.user_cache != self.current_user
            ):
                raise self.get_invalid_credentials_error()

        return self.cleaned_data

    def get_invalid_credentials_error(self):
        return ValidationError(
            self.error_messages['invalid_credentials'],
            code='invalid_credentials'
        )
