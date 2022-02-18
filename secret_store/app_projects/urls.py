from django.urls import path
from .views import MyProjects, AllProjects

urlpatterns = [
    path("myprojects/", MyProjects.as_view(), name="my projects"),
    path("feed/", AllProjects.as_view(), name="feed"),
]
