from django.urls import path
from tables import views


app_name = 'tables'
urlpatterns = [
    path('', views.TableListView.as_view(), name='list'),
    path('<int:pk>/', views.TableDetailView.as_view(), name='detail')
]
