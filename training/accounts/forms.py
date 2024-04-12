from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Submit
from crispy_forms.bootstrap import InlineRadios, FieldWithButtons
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms


User = get_user_model()


class UsernameChangeForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "onfocus": 'moveCursorOnFocus(this)'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
        )


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
        )


class DeleteAccountForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)'
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(request, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if (
                self.user_cache is None
                or self.user_cache != self.current_user
            ):
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
