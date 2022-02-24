from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import ProjectModel, VariableModel


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = ("name", "viewers", "shared", "owner")
        # read_only_fields = ("owner", )
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


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableModel
        fields = ("name", "value", "is_active", "project")
        # read_only_fields = ("project",)
        validators = [
            UniqueTogetherValidator(
                queryset=VariableModel.objects.all(), fields=("name", "project")
            )
        ]

    def create(self, validated_data):
        variable = VariableModel.objects.create(**validated_data)
        return variable

    def update(self, instance, validated_data):
        name = validated_data.get("name", instance.name)
        value = validated_data.get("value", instance.value)
        is_active = validated_data.get("is_active", instance.is_active)
        instance.is_active = is_active
        instance.value = value
        instance.name = name
        instance.save()
        return instance
