from django.db import models

from app_auth.models import User


class ProjectModel(models.Model):
    owner = models.ForeignKey(User, related_name="projects", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    viewers = models.ManyToManyField(
        User, related_name="project_viewers", null=True, blank=True
    )
    shared = models.ManyToManyField(
        User, related_name="project_shared", null=True, blank=True
    )

    class Meta:
        unique_together = ("name", "owner_id")
        permissions = (
            ("can_view", "Может просматривать"),
            ("can_edit", "Может редактировать"),
            ("can_add", "Может добавлять"),
            ("can_delete", "Может удалять"),
        )

    def __str__(self):
        return f"{self.name}, {self.id}"


class VariableModel(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    project = models.ForeignKey(
        ProjectModel, related_name="variable", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("name", "project")

    def __str__(self):
        return f"{self.name}, {self.id}"
