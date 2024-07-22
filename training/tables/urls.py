from django.urls import path
from tables import views


urlpatterns = [
    path('', views.TableListView.as_view(), name='tables-list')
]
