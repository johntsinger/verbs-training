from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'onfocus': 'moveCursorOnFocus(this)',
                'autocomplete': 'username'
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = gettext(
            '150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        )
