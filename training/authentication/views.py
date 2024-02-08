from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Case, When, Value, BooleanField
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    ModelFormMixin
)
from django.urls import reverse_lazy
from authentication.forms import (
    LoginForm,
    SignUpForm
)


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm
    success_message = "Your account was created successfully"

