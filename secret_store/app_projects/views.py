from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import ProjectModel


class MyProjects(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    template_name = "app_projects/my_projects_list.html"
    context_object_name = "my_projects"

    def get_queryset(self):
        return ProjectModel.objects.filter(owner__id=self.request.user.id)


# Create your views here.


class AllProjects(ListView):
    template_name = "app_projects/all_projects_list.html"
    context_object_name = "projects"
    queryset = ProjectModel.objects.all()
