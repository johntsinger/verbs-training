from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import (
    CreateView
)
from django.urls import reverse_lazy
from authentication.forms import (
    SignUpForm
)


class SignUpView(
    SuccessMessageMixin,
    CreateView
):
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    success_message = "Your account was created successfully"
