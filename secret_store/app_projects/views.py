from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from rest_framework import permissions

from rest_framework.generics import (
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import ProjectSerializer, VariableSerializer
from rest_framework.views import APIView

from .models import ProjectModel, VariableModel


class ViewPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        is_viewer = obj.viewers.filter(id=user_id).exists()
        return is_viewer


class EditPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        is_shared = obj.shared.filter(id=user_id).exists()
        return is_shared


class OwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = request.user.id
        print(obj)
        is_owner = obj.owner.id == user_id
        return is_owner


class MyProjects(APIView):
    permission_classes = [IsAuthenticated, OwnerPermission]

    def get(self, request):
        my_projects = ProjectModel.objects.filter(owner__id=request.user.id)
        print(my_projects)
        serializer = ProjectSerializer(my_projects, many=True)
        return Response({"my_projects": serializer.data})

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"OK": "Created"})

    def put(self, request, pk):
        my_project = get_object_or_404(ProjectModel, pk=pk)
        self.check_object_permissions(self.request, my_project)
        serializer = ProjectSerializer(
            instance=my_project, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"my_projects": serializer.data})

    def delete(self, request, pk):
        my_project = get_object_or_404(ProjectModel, pk=pk)
        my_project.delete()
        return Response({"OK": "Deleted"})


class MySharedProjects(APIView):
    permission_classes = [IsAuthenticated]

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


class ProjectVariables(ViewSet):
    def _setattrs(self):
        method = getattr(self, "create")
        setattr(self, "post", method)
        method = getattr(self, "retrieve")
        setattr(self, "get", method)
        method = getattr(self, "update")
        setattr(self, "patch", method)
        method = getattr(self, "destroy")
        setattr(self, "delete", method)

    def get_permissions(self):
        self._setattrs()
        print(self.action)
        if self.request.method == "GET":
            return [IsAuthenticated(), ViewPermission()]
        if self.request.method == "POST":
            return [IsAuthenticated(), EditPermission()]
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated(), OwnerPermission()]

    def get_project(self, fk):

        project = get_object_or_404(ProjectModel, pk=fk)
        self.check_object_permissions(self.request, project)
        return project

    def get_variable(self, pk):
        variable = get_object_or_404(VariableModel, pk=pk)
        return variable

    def retrieve(self, request, fk, pk):
        project = self.get_project(fk)
        variable = self.get_variable(pk)
        serializer = VariableSerializer(variable)
        return Response(serializer.data)

    def create(self, request, fk):
        project = self.get_project(fk)
        print(project)
        serializer = VariableSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"OK": "Created"})

    def update(self, request, fk, pk):

        project = self.get_project(fk)
        variable = self.get_variable(pk)
        serializer = VariableSerializer(
            instance=variable, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    def destroy(self, request, fk, pk):

        project = self.get_project(fk)
        variable = self.get_variable(pk)
        variable.delete()
        return Response({"OK": "DELETED"})
