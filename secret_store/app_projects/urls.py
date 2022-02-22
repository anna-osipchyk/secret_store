from django.urls import path, include
from .views import (
    MyProjects,
    AllProjects,
    MyProject,
    CreateProject,
    DeleteProject,
    AddVariable,
    DeleteVariable,
    EditVariable,
)

urlpatterns = [
    path("my_projects/", MyProjects.as_view(), name="my_projects"),
    path("feed/", AllProjects.as_view(), name="feed"),
    path("my_project/<int:pk>/", MyProject.as_view(), name="my_project"),
    path("create/", CreateProject.as_view(), name="create_project"),
    path("delete/<int:pk>/", DeleteProject.as_view(), name="delete_project"),
    path("<int:pk>/add_variable/", AddVariable.as_view(), name="add_variable"),
    path("<int:project_id>/delete_variable/<int:pk>", DeleteVariable.as_view(), name="delete_variable"),
    path("<int:project_id>/edit_variable/<int:pk>", EditVariable.as_view(), name="edit_variable")
]
