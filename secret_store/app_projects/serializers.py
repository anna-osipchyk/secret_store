from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import ProjectModel, VariableModel


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = ("name", "viewers", "shared", "owner")
        validators = [
            UniqueTogetherValidator(
                queryset=ProjectModel.objects.all(), fields=("name", "owner")
            )
        ]

    def create(self, validated_data):
        shared = validated_data.pop("shared")
        viewers = validated_data.pop("viewers")
        project = ProjectModel.objects.create(**validated_data)
        project.viewers.set(viewers)
        project.shared.set(shared)
        project.save()
        return project

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        viewers = validated_data.get("viewers", instance.viewers)
        shared = validated_data.get("shared", instance.shared)
        instance.viewers.set(viewers)
        instance.shared.set(shared)
        instance.save()
        return instance
