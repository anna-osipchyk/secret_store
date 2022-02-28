from django.urls import path
from .views import (
    MyProjects,
    MyViewedProjects,
    MySharedProjects,
    MyProjectVariables,
)

urlpatterns = [
    path("my_projects/", MyProjects.as_view(), name="my_projects"),
    path("my_projects/<int:pk>/", MyProjects.as_view(), name="my_projects_put"),
    path("my_viewed_projects/", MyViewedProjects.as_view(), name="viewed_projects"),
    path("my_shared_projects/", MySharedProjects.as_view(), name="shared_projects"),
    path("<int:pk>/variables/", MyProjectVariables.as_view(), name="variables"),
    path(
        "<int:fk>/variables/<int:pk>/",
        MyProjectVariables.as_view(),
        name="variables_put",
    ),
]
