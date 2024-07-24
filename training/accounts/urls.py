from django.urls import path

from accounts import views


urlpatterns = [
    path('', views.AccountView.as_view(), name='account'),
    path(
        'username/',
        views.UsernameChangeView.as_view(),
        name='change_username'
    ),
    path(
        'email/',
        views.EmailChangeView.as_view(),
        name='change_email'
    ),
    path(
        'password/',
        views.PasswordChangeView.as_view(),
        name='change_password'
    ),
    path(
        'delete-account/',
        views.DeleteAccountView.as_view(),
        name='delete_account'
    )
]
