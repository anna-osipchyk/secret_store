from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import ProjectSerializer
from rest_framework.views import APIView

from .models import ProjectModel, VariableModel
from .forms import NewProjectForm, VariableForm
from django.db import transaction


class MyProjects(APIView):
    def get(self, request):
        my_projects = ProjectModel.objects.filter(owner__id=request.user.id)
        serializer = ProjectSerializer(my_projects, many=True)
        return Response({"my_projects": serializer.data})

    def post(self, request):
        my_project = request.data.get("my_project")
        serializer = ProjectSerializer(data=my_project)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"OK": "Created"})

    def put(self, request, pk):
        my_project = get_object_or_404(ProjectModel, pk=pk)
        data = request.data.get("my_project")
        serializer = ProjectSerializer(instance=my_project, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"my_projects": serializer.data})

    def delete(self, request, pk):
        my_project = get_object_or_404(ProjectModel, pk=pk)
        my_project.delete()
        return Response({"OK": "Deleted"})


# class MyProjects(LoginRequiredMixin, ListView):
#     login_url = reverse_lazy("login")
#     template_name = "app_projects/my_projects_list.html"
#     context_object_name = "my_projects"
#
#     def get_queryset(self):
#         return ProjectModel.objects.filter(owner__id=self.request.user.id)


# Create your views here.


class MySharedProjects(LoginRequiredMixin, ListView):
    model = ProjectModel
    template_name = "app_projects/all_projects_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        user_id = self.request.user.id
        shared_projects = ProjectModel.objects.prefetch_related("shared").filter(
            viewers__id=user_id
        )
        return shared_projects


class MyViewedProjects(LoginRequiredMixin, ListView):
    model = ProjectModel
    template_name = "app_projects/all_projects_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        user_id = self.request.user.id
        shared_projects = ProjectModel.objects.prefetch_related("viewers").filter(
            Q(viewers__id=user_id) & ~Q(shared__id=user_id)
        )
        return shared_projects

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=None, **kwargs)
    #     user_id = self.request.user.id
    #     # projects that user has permission to view or edit
    #     visible_projects = ProjectModel.objects.prefetch_related("viewers").filter(
    #         viewers__id=user_id
    #     )
    #     shared_projects = visible_projects.prefetch_related("shared").filter(
    #         shared__id=user_id
    #     )
    #     context["visible_projects"] = visible_projects
    #     context["shared_projects"] = shared_projects
    #     return context


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
        project_name = form.cleaned_data["name"]
        self.project = form.save(commit=False)
        projects = ProjectModel.objects.filter(
            Q(owner__id=self.request.user.id) & Q(name=project_name)
        )
        if len(projects) == 0:
            self.project.owner = self.request.user
            self.project.save()
            return HttpResponseRedirect(self.success_url)

        return HttpResponse("Value with this name already exists in your project!")


class DeleteProject(LoginRequiredMixin, DeleteView):
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
    form_class = VariableForm
    context_object_name = "variable"
    success_url = reverse_lazy("my_projects")
    template_name = "app_projects/variable_add.html"

    def form_valid(self, form):
        self.variable = form.save(commit=False)
        project_id = self.kwargs.get("pk")
        variable_name = form.cleaned_data["name"]
        variables_of_project = VariableModel.objects.filter(
            Q(project__id=project_id) & Q(name=variable_name)
        )
        if len(variables_of_project) == 0:
            self.variable.project = ProjectModel.objects.get(id=project_id)
            self.variable.save()
            return HttpResponseRedirect(self.success_url)
        return HttpResponse("Value with this name already exists in your project!")


class DeleteVariable(LoginRequiredMixin, DeleteView):
    template_name = "app_projects/variable_delete.html"
    success_url = reverse_lazy("my_projects")
    model = VariableModel
    context_object_name = "variable"


class EditVariable(LoginRequiredMixin, UpdateView):
    template_name = "app_projects/variable_edit.html"
    success_url = reverse_lazy("my_projects")
    model = VariableModel
    form_class = VariableForm
    context_object_name = "variable"

    def form_valid(self, form):
        self.variable = form.save(commit=False)
        project_id = self.kwargs.get("project_id")
        variable_name = form.cleaned_data["name"]
        variables_of_project = VariableModel.objects.filter(
            Q(project__id=project_id) & Q(name=variable_name)
        )
        if len(variables_of_project) == 0:
            self.variable.project = ProjectModel.objects.get(id=project_id)
            self.variable.save()
            return HttpResponseRedirect(self.success_url)
        return HttpResponse("Value with this name already exists in your project!")
