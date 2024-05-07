from django.urls import path
from verbs import views


urlpatterns = [
    path('', views.VerbListView.as_view(), name='verbs'),
]
