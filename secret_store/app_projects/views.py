from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import ProjectModel, VariableModel
from .forms import NewProjectForm, NewVariableForm
from django.db import transaction


class MyProjects(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    template_name = "app_projects/my_projects_list.html"
    context_object_name = "my_projects"

    def get_queryset(self):
        return ProjectModel.objects.filter(owner__id=self.request.user.id)


# Create your views here.


class AllProjects(ListView):
    model = ProjectModel
    template_name = "app_projects/all_projects_list.html"
    context_object_name = "projects"
    queryset = ProjectModel.objects.all()


class MyProject(LoginRequiredMixin, DetailView):
    model = ProjectModel
    template_name = "app_projects/my_project_detail.html"
    context_object_name = "my_project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get("pk")
        context["variables"] = VariableModel.objects.filter(project__id=project_id)
        return context


class CreateProject(LoginRequiredMixin, CreateView):
    form_class = NewProjectForm
    context_object_name = "project"
    success_url = reverse_lazy("my_projects")
    template_name = "app_projects/my_project_create.html"

    def form_valid(self, form):
        self.project = form.save(commit=False)
        self.project.owner = self.request.user
        self.project.save()
        return HttpResponseRedirect(self.success_url)


class DeleteProject(DeleteView):
    template_name = "app_projects/my_project_delete.html"
    success_url = reverse_lazy("my_projects")
    model = ProjectModel
    context_object_name = "my_project"

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            my_project = self.get_object(queryset=None)
            variables = VariableModel.objects.filter(project__id=my_project.id)
            for variable in variables:
                variable.delete()
            my_project.delete()
            return HttpResponseRedirect(self.success_url)


class AddVariable(LoginRequiredMixin, CreateView):
    form_class = NewVariableForm
    context_object_name = "variable"
    success_url = reverse_lazy("my_projects")
    template_name = "app_projects/variable_add.html"


class DeleteVariable(LoginRequiredMixin, DeleteView):
    template_name = "app_projects/variable_delete.html"
    success_url = reverse_lazy("my_projects")
    model = VariableModel
    context_object_name = "variable"
    # def form_valid(self, form):
    #     self.variable = form.save(commit=True)
    #     project_id = self.kwargs.get("pk")
    #     project = ProjectModel.objects.get(id=project_id)
    #     project.variables.set([self.variable])
    #     project.save()
    #     return HttpResponseRedirect(self.success_url)
