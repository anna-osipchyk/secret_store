from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from .views import (
    MyProjects,
    MyViewedProjects,
    MySharedProjects,
    ProjectVariables,
)

router = routers.DefaultRouter()
# router.register("{fk}/variables/{pk}", ProjectVariables, basename="variables")
# router.register("{fk}/variables/", ProjectVariables,basename="new_variable")
urlpatterns = [
    path("projects/", MyProjects.as_view(), name="my_projects"),
    path("projects/<int:pk>/", MyProjects.as_view(), name="my_projects_put"),
    path("viewed_projects/", MyViewedProjects.as_view(), name="viewed_projects"),
    path("shared_projects/", MySharedProjects.as_view(), name="shared_projects"),
    url(r"^(?P<fk>\d+)/variables/$", ProjectVariables.as_view({"post": "create"})),
    url(
        r"^(?P<fk>\d+)/variables/(?P<pk>\d+)/$",
        ProjectVariables.as_view({"get": "retrieve"}),
    ),
    url(
        r"^(?P<fk>\d+)/variables/(?P<pk>\d+)/$",
        ProjectVariables.as_view({"patch": "update"}),
    ),
    url(
        r"^(?P<fk>\d+)/variables/(?P<pk>\d+)/$",
        ProjectVariables.as_view({"delete": "destroy"}),
    )
    # path("projects/<int:pk>/variables/", MyProjectVariables.as_view(), name="variables"),
]
