from django.urls import path, include
from .views import *
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout')
]
