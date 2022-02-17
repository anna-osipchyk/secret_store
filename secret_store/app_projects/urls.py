from django.urls import path, include
from .views import *
urlpatterns = [
    path('myprojects/', MyProjects.as_view(), name='my projects'),
    path('feed/', AllProjects.as_view(), name='feed')
]
