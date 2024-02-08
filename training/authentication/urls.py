from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from authentication import views
from authentication.forms import LoginForm


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='authentication/login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
