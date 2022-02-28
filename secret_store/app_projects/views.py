from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from rest_framework import permissions


from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ProjectSerializer, VariableSerializer
from rest_framework.views import APIView

from .models import ProjectModel, VariableModel


class ViewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        import pdb

        pdb.set_trace()
        user_id = request.user.id
        project_id = request.data["my_projects"]["project"]
        project = ProjectModel.objects.get(id=project_id)
        is_viewer = project.viewers.contains(user_id)
        return is_viewer


class MyProjects(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated, ViewPermission]

    def get(self, request):
        user_id = request.user.id
        shared_projects = ProjectModel.objects.prefetch_related("shared").filter(
            shared__id=user_id
        )
        serializer = ProjectSerializer(shared_projects, many=True)
        return Response({"shared_projects": serializer.data})


class MyViewedProjects(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        viewed_projects = ProjectModel.objects.prefetch_related("viewers").filter(
            Q(viewers__id=user_id) & ~Q(shared__id=user_id)
        )
        serializer = ProjectSerializer(viewed_projects, many=True)
        return Response({"viewed_projects": serializer.data})


class MyProjectVariables(APIView):
    permission_classes = [ViewPermission, IsAuthenticated]

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


class MySharedProjectsVariables(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fk):
        project = get_object_or_404(ProjectModel, pk=fk)
        variables_of_project = VariableModel.objects.filter(project__id=project.id)
        serializer = VariableSerializer(variables_of_project, many=True)
        return Response({"variables": serializer.data})

    def post(self, request, fk):
        project = get_object_or_404(ProjectModel, pk=fk)
        variables_of_project = request.data.get("shared_variables")
        serializer = VariableSerializer(data=variables_of_project)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"OK": "Created"})


class MyViewedProjectsVariables(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, fk):
        project = get_object_or_404(ProjectModel, pk=fk)
        variables_of_project = VariableModel.objects.filter(project__id=project.id)
        serializer = VariableSerializer(variables_of_project, many=True)
        return Response({"variables": serializer.data})
