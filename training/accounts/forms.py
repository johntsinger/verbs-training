from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class UsernameChangeForm(forms.ModelForm):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "onfocus": "moveCursorOnFocus(this)"
            }
        )
    )

    error_messages = {
        "invalid_username": _(
            "A user with that username already exists."
        ),
    }

    def clean(self):
        username = self.cleaned_data.get("username")

        if (
            User.objects.filter(username=username).exists()
            and username != self.instance.username
        ):
            raise self.get_invalid_username_error()

        return self.cleaned_data

    def get_invalid_username_error(self):
        return ValidationError(
            {
                "username": self.error_messages["invalid_username"]
            },
            code="invalid_username",
        )

    class Meta:
        model = User
        fields = (
            "username",
        )


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "onfocus": "moveCursorOnFocus(this)"
            }
        )
    )

    error_messages = {
        "invalid_email": _(
            "A user with that email already exists."
        ),
    }

    def clean(self):
        email = self.cleaned_data.get("email")

        if (
            User.objects.filter(email=email).exists()
            and email != self.instance.email
        ):
            raise self.get_invalid_email_error()

    def get_invalid_email_error(self):
        return ValidationError(
            {
                "email": self.error_messages["invalid_email"]
            },
            code="invalid_email",
        )

    class Meta:
        model = User
        fields = (
            "email",
        )


class DeleteAccountForm(forms.ModelForm):
    """
    Form to delete the account of the logged-in user.
    Requires email address and password to confirm deletion.
    """
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "onfocus": "moveCursorOnFocus(this)"
            }
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password"
            }
        ),
    )

    error_messages = {
        "invalid_credentials": _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
    }

    class Meta:
        model = User
        fields = (
            "email",
            "password"
        )

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            if (
                email != self.current_user.email
                or not self.current_user.check_password(password)
            ):
                raise self.get_invalid_credentials_error()
            """
            self.user_cache = authenticate(
                email=email, password=password
            )
            if (
                self.user_cache is None
                or self.user_cache != self.current_user
            ):
                raise self.get_invalid_credentials_error()
            """

        return self.cleaned_data

    def get_invalid_credentials_error(self):
        return ValidationError(
            self.error_messages["invalid_credentials"],
            code="invalid_credentials",
        )
