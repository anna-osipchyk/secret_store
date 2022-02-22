from django.urls import path
from .views import (
    MyProjects,
    MyViewedProjects,
    MySharedProjects,
    MyProject,
    CreateProject,
    DeleteProject,
    AddVariable,
    DeleteVariable,
    EditVariable,
)

urlpatterns = [
    path("my_projects/", MyProjects.as_view(), name="my_projects"),
    path("my_viewed_projects/", MyViewedProjects.as_view(), name="viewed_projects"),
    path("my_shared_projects/", MySharedProjects.as_view(), name="shared_projects"),
    path("my_project/<int:pk>/", MyProject.as_view(), name="my_project"),
    path("create/", CreateProject.as_view(), name="create_project"),
    path("delete/<int:pk>/", DeleteProject.as_view(), name="delete_project"),
    path("<int:pk>/add_variable/", AddVariable.as_view(), name="add_variable"),
    path(
        "<int:project_id>/delete_variable/<int:pk>",
        DeleteVariable.as_view(),
        name="delete_variable",
    ),
    path(
        "<int:project_id>/edit_variable/<int:pk>",
        EditVariable.as_view(),
        name="edit_variable",
    ),
]
