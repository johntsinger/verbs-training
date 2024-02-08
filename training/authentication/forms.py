from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, HTML, Submit
from crispy_forms.bootstrap import InlineRadios, FieldWithButtons
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django import forms


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password'
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
