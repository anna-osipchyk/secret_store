from django.contrib.auth.models import User
from django.db import models


class VariableModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'id')


class ProjectModel(models.Model):
    owner = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    variables = models.ManyToManyField(
        VariableModel, related_name="project", null=True, blank=True
    )

    class Meta:
        unique_together = ('name', 'id')
