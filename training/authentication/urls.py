from django.urls import path
from django.contrib.auth.views import LogoutView
from authentication import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('account/', views.AccountView.as_view(), name='account'),
    path(
        'account/username/',
        views.UsernameChangeView.as_view(),
        name='change-username'
    ),
    path(
        'account/email/',
        views.EmailChangeView.as_view(),
        name='change-email'
    ),
    path(
        'account/password/',
        views.PasswordChangeView.as_view(),
        name='change-password'
    ),
    path(
        'account/delete/',
        views.DeleteAccountView.as_view(),
        name='delete-account'
    )
]
