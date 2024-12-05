from django.urls import include, path

from training.tables import views


app_name = "tables"

default_tables_urls = [
    path(
        "<uuid:pk>/<str:slug_name>/",
        views.DefaultTableDetailView.as_view(),
        name="detail",
    ),
    path("add/", views.DefaultTableCreateView.as_view(), name="add"),
    path(
        "<uuid:pk>/<str:slug_name>/change/",
        views.DefaultTableUpdateView.as_view(),
        name="change",
    ),
    path(
        "<uuid:pk>/<str:slug_name>/delete/",
        views.DefaultTableDeleteView.as_view(),
        name="delete",
    ),
    path(
        "<uuid:pk>/<str:slug_name>/training/",
        views.DefaultTableTrainingFormView.as_view(),
        name="training",
    ),
    path(
        "<uuid:pk>/<str:slug_name>/training/results/",
        views.DefaultTableResultView.as_view(),
        name="results",
    ),
]

user_tables_urls = [
    path(
        "<uuid:pk>/<str:slug_name>/",
        views.UserTableDetailView.as_view(),
        name="detail",
    ),
    path(
        "add/",
        views.UserTableCreateView.as_view(),
        name="add",
    ),
    path(
        "<uuid:pk>/<str:slug_name>/change/",
        views.UserTableUpdateView.as_view(),
        name="change",
    ),
    path(
        "<uuid:pk>/<str:slug_name>/delete/",
        views.UserTableDeleteView.as_view(),
        name="delete",
    ),
    path(
        "<uuid:pk>/<str:slug_name>/training/",
        views.UserTableTrainingFormView.as_view(),
        name="training",
    ),
    path(
        "<uuid:pk>/<str:slug_name>/training/results/",
        views.UserTableResultView.as_view(),
        name="results",
    ),
]

urlpatterns = [
    path("", views.TableListView.as_view(), name="list"),
    path("default/", include((default_tables_urls, "default"))),
    path("user/", include((user_tables_urls, "user"))),
]
