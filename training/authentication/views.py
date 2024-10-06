from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
    PasswordResetDoneView as BasePasswordResetDoneView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
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


class LoginView(
    TitleMixin,
    PreviousPageURLMixin,
    BaseLoginView
):
    template_name = 'authentication/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    previous_page_url = reverse_lazy('verbs:list')
    title = _('Login')


class SignUpView(
    TitleMixin,
    PreviousPageURLMixin,
    SuccessMessageMixin,
    CreateView
):
    template_name = 'authentication/signup.html'
    form_class = SignUpForm
    success_message = _('Your account was created successfully')
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    redirect_authenticated_user = True
    previous_page_url = reverse_lazy('authentication:login')
    title = _('Sign Up')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if (
            self.redirect_authenticated_user
            and self.request.user.is_authenticated
        ):
            redirect_to = self.success_url
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected."
                    "Check that your LOGIN_REDIRECT_URL doesn't point "
                    "to a signup page."
                )
            return redirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(
            self.request,
            self.object,
            backend='authentication.backends.EmailBackend'
        )
        return valid


class PasswordResetView(
    TitleMixin,
    PreviousPageURLMixin,
    SuccessMessageMixin,
    BasePasswordResetView
):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.txt'
    success_url = reverse_lazy('authentication:password-reset-done')
    previous_page_url = reverse_lazy('authentication:login')
    title = _('Reset password')


class PasswordResetConfirmView(
    PreviousPageURLMixin,
    BasePasswordResetConfirmView
):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('authentication:login')
    previous_page_url = reverse_lazy('authentication:login')


class PasswordResetDoneView(
    PreviousPageURLMixin,
    BasePasswordResetDoneView
):
    template_name = 'authentication/password_reset_done.html'
    previous_page_url = reverse_lazy('authentication:login')


class AccountView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    DetailView
):
    template_name = 'authentication/account.html'
    previous_page_url = reverse_lazy('verbs:list')
    title = _('Account settings')

    def get_object(self):
        return self.request.user

    def get_previous_page_url(self):
        previous_page_url = super().get_previous_page_url()
        http_referer_url = urlparse(
            self.request.META.get('HTTP_REFERER')
        ).path
        if http_referer_url in [reverse('tables:list')]:
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
    success_url = reverse_lazy('authentication:account')
    previous_page_url = reverse_lazy('authentication:account')
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
    success_url = reverse_lazy('authentication:account')
    previous_page_url = reverse_lazy('authentication:account')
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
    success_url = reverse_lazy('authentication:account')
    previous_page_url = reverse_lazy('authentication:account')
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
    success_url = reverse_lazy('authentication:login')
    previous_page_url = reverse_lazy('authentication:account')
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
        messages.success(
            self.request,
            gettext('Your account has been sucessfully deleted !')
        )
        return super().form_valid(form)
