from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import (
    CreateView
)
from django.urls import reverse_lazy
from common.views.mixins import PreviousPageURLMixin
from authentication.forms import (
    SignUpForm
)


class SignUpView(
    PreviousPageURLMixin,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'authentication/signup.html'
    form_class = SignUpForm
    success_message = "Your account was created successfully"
    success_url = reverse_lazy('login')
    previous_page_url = reverse_lazy('login')
