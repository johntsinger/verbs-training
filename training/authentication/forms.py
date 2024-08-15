from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)',
                'autocomplete': 'email'
            }
        )
    )


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email',
            'username',
            'password1',
            'password2'
        )
        help_texts = {
            'email': _(
                'Required. 254 characters of fewer. '
                'Must be a valid email address.'
            )
        }


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
            '150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
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
            '254 characters of fewer. Must be a valid email address.'
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
        )


class DeleteAccountForm(forms.ModelForm):
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

    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if (
            email != self.current_user.email
            or not self.current_user.check_password(password)
        ):
            raise self.get_invalid_credentials_error()

    def get_invalid_credentials_error(self):
        return ValidationError(
            self.error_messages['invalid_credentials'],
            code='invalid_credentials',
        )
