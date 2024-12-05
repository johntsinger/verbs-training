from django.urls import path

from training.verbs import views


app_name = "verbs"
urlpatterns = [
    path("", views.VerbListView.as_view(), name="list"),
]
