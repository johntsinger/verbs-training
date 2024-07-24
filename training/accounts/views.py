from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView as BasePasswordChangeView,
)
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    UpdateView,
    DeleteView
)
from common.views.mixins import PreviousPageURLMixin

from accounts.forms import (
    UsernameChangeForm,
    EmailChangeForm,
    DeleteAccountForm
)


User = get_user_model()


class AccountView(
    PreviousPageURLMixin,
    LoginRequiredMixin,
    DetailView
):
    template_name = 'accounts/account.html'
    previous_page_url = reverse_lazy('verbs-list')

    def get_object(self):
        return self.request.user

    def get_previous_page_url(self):
        previous_page_url = super().get_previous_page_url()
        http_referer_url = urlparse(
            self.request.META.get('HTTP_REFERER')
        ).path
        if http_referer_url in [reverse('verbs-list')]:
            return http_referer_url
        return previous_page_url


class UsernameChangeView(
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    template_name = 'accounts/change.html'
    form_class = UsernameChangeForm
    success_message = _('Your username has been successfully updated !')
    success_url = reverse_lazy('account')
    previous_page_url = reverse_lazy('account')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'username'
        return context


class EmailChangeView(
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    template_name = 'accounts/change.html'
    form_class = EmailChangeForm
    success_message = _('Your email has been successfully updated !')
    success_url = reverse_lazy('account')
    previous_page_url = reverse_lazy('account')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'email'
        return context


class PasswordChangeView(
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    BasePasswordChangeView
):
    template_name = 'accounts/change.html'
    success_message = _('Your password has been successfully updated !')
    success_url = reverse_lazy('account')
    previous_page_url = reverse_lazy('account')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'password'
        return context


class DeleteAccountView(
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    template_name = 'accounts/delete.html'
    form_class = DeleteAccountForm
    success_url = reverse_lazy('login')
    previous_page_url = reverse_lazy('account')

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
