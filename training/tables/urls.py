from django.urls import path
from tables import views


app_name = 'tables'
urlpatterns = [
    path('', views.TableListView.as_view(), name='list'),
    path(
        '<uuid:pk>/<str:slug_name>/',
        views.TableDetailView.as_view(),
        name='detail'
    ),
    path(
        '<uuid:pk>/<str:slug_name>/training/',
        views.TrainingFormView.as_view(),
        name='training'
    ),
    path(
        '<uuid:pk>/<str:slug_name>/training/results/',
        views.ResultView.as_view(),
        name='results'
    )
]
