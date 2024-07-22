from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import (
    CreateView
)
from django.urls import reverse_lazy
from django.shortcuts import redirect
from common.views.mixins import PreviousPageURLMixin
from authentication.forms import (
    SignUpForm,
    LoginForm
)


class SignUpView(
    PreviousPageURLMixin,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'authentication/signup.html'
    form_class = SignUpForm
    success_message = 'Your account was created successfully'
    success_url = reverse_lazy('login')
    previous_page_url = reverse_lazy('login')

    def form_valid(self, form):
        repsonse = super().form_valid(form)
        login(self.request, self.object)
        return repsonse

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account')
        return super().get(request, *args, **kwargs)


class LoginView(
    PreviousPageURLMixin,
    BaseLoginView
):
    template_name = 'authentication/login.html'
    authentication_form = LoginForm
    previous_page_url = reverse_lazy('verbs-list')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('verbs-list')
        return super().get(request, *args, **kwargs)
