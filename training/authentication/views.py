from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    PasswordChangeView as BasePasswordChangeView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)

from common.views.mixins import PreviousPageURLMixin, TitleMixin
from authentication.forms import (
    SignUpForm,
    LoginForm,
    UsernameChangeForm,
    EmailChangeForm,
    DeleteAccountForm
)


class SignUpView(
    TitleMixin,
    PreviousPageURLMixin,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'authentication/signup.html'
    form_class = SignUpForm
    success_message = _('Your account was created successfully')
    success_url = reverse_lazy('verbs-list')
    previous_page_url = reverse_lazy('login')
    title = _('Sign Up')

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request, *args, **kwargs)


class LoginView(
    TitleMixin,
    PreviousPageURLMixin,
    BaseLoginView
):
    template_name = 'authentication/login.html'
    authentication_form = LoginForm
    previous_page_url = reverse_lazy('verbs-list')
    title = _('Login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request, *args, **kwargs)


class AccountView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    DetailView
):
    template_name = 'authentication/account.html'
    previous_page_url = reverse_lazy('verbs-list')
    title = _('Account settings')

    def get_object(self):
        return self.request.user

    def get_previous_page_url(self):
        previous_page_url = super().get_previous_page_url()
        http_referer_url = urlparse(
            self.request.META.get('HTTP_REFERER')
        ).path
        if http_referer_url in [reverse('verbs-list'), reverse('tables-list')]:
            return http_referer_url
        return previous_page_url


class UsernameChangeView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    template_name = 'authentication/change.html'
    form_class = UsernameChangeForm
    success_message = _('Your username has been successfully updated !')
    success_url = reverse_lazy('account')
    previous_page_url = reverse_lazy('account')
    title = _('Change my username')

    def get_object(self):
        return self.request.user


class EmailChangeView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    template_name = 'authentication/change.html'
    form_class = EmailChangeForm
    success_message = _('Your email has been successfully updated !')
    success_url = reverse_lazy('account')
    previous_page_url = reverse_lazy('account')
    title = _('Change my email')

    def get_object(self):
        return self.request.user


class PasswordChangeView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    BasePasswordChangeView
):
    template_name = 'authentication/change.html'
    success_message = _('Your password has been successfully updated !')
    success_url = reverse_lazy('account')
    previous_page_url = reverse_lazy('account')
    title = _('Change my password')


class DeleteAccountView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'authentication/delete.html'
    form_class = DeleteAccountForm
    success_url = reverse_lazy('login')
    previous_page_url = reverse_lazy('account')
    title = _('Delete my account')

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {
                'current_user': self.request.user
            }
        )
        return kwargs

    def form_valid(self, form):
        messages.error(
            self.request,
            gettext('Your account has been sucessfully deleted !')
        )
        return super().form_valid(form)
