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

from .serializers import ProjectSerializer, VariableSerializer
from rest_framework.views import APIView

from .models import ProjectModel, VariableModel
from .forms import NewProjectForm, VariableForm
from django.db import transaction


class MyProjects(APIView):
    def get(self, request):
        my_projects = ProjectModel.objects.filter(owner__id=request.user.id)
        print(my_projects)
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


class MySharedProjects(APIView):
    def get(self, request):
        user_id = request.user.id
        shared_projects = ProjectModel.objects.prefetch_related("shared").filter(
            shared__id=user_id
        )
        serializer = ProjectSerializer(shared_projects, many=True)
        return Response({"shared_projects": serializer.data})


class MyViewedProjects(APIView):
    def get(self, request):
        user_id = request.user.id
        viewed_projects = ProjectModel.objects.prefetch_related("viewers").filter(
            Q(viewers__id=user_id) & ~Q(shared__id=user_id)
        )
        serializer = ProjectSerializer(viewed_projects, many=True)
        return Response({"viewed_projects": serializer.data})


class MyProjectVariables(APIView):
    def get(self, request, pk):
        project = get_object_or_404(ProjectModel, pk=pk)
        variables_of_project = VariableModel.objects.filter(project__id=project.id)
        serializer = VariableSerializer(variables_of_project, many=True)
        return Response({"variables": serializer.data})

    def post(self, request, fk):
        project = get_object_or_404(ProjectModel, pk=fk)
        variables_of_project = request.data.get("my_variables")
        serializer = VariableSerializer(data=variables_of_project)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"OK": "Created"})

    def put(self, request, fk, pk):

        my_project = get_object_or_404(ProjectModel, pk=fk)
        data = request.data.get("my_variable")
        variable = get_object_or_404(VariableModel, pk=pk)
        serializer = VariableSerializer(instance=variable, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"variables": serializer.data})

    def delete(self, request, fk, pk):
        my_project = get_object_or_404(ProjectModel, pk=fk)
        variable = get_object_or_404(VariableModel, pk=pk)
        variable.delete()
        return Response({"OK": "Deleted"})


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
