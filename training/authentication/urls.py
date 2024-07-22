from django.urls import path
from django.contrib.auth.views import LogoutView
from authentication import views


"""
from django.contrib.auth.views import LoginView
from authentication.forms import LoginForm

path(
    "login/",
    LoginView.as_view(
        template_name="authentication/login.html",
        authentication_form=LoginForm
    ),
    name="login"
),
"""


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
