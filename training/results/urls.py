from django.urls import include, path
from results import views


app_name = 'results'

user_tables_urls = [
    path(
        '<uuid:pk>/<str:slug_name>/reset/',
        views.UserTableResetView.as_view(),
        name='reset'
    )
]

default_tables_urls = [
    path(
        '<uuid:pk>/<str:slug_name>/reset/',
        views.DefaultTableResetView.as_view(),
        name='reset'
    )
]

urlpatterns = [
    path('reset-all/', views.AllTablesResetView.as_view(), name='reset-all'),
    path('default/', include((default_tables_urls, 'default'))),
    path('user/', include((user_tables_urls, 'user'))),
]
