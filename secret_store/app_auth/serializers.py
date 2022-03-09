from rest_framework import serializers
from django.contrib.auth import authenticate, login
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализация регистрации пользователя и создания нового."""

    password = serializers.CharField(max_length=128, min_length=4, write_only=True)

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User

        fields = ["email", "username", "password", "token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        if username is None:
            raise serializers.ValidationError("A username is required to log in.")

        if password is None:
            raise serializers.ValidationError("A password is required to log in.")
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this username and password was not found."
            )

        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {"email": user.email, "username": user.username, "token": user.token}


class UserSerializer(serializers.ModelSerializer):
    """Ощуществляет сериализацию и десериализацию объектов User."""

    password = serializers.CharField(max_length=128, min_length=4, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "token",
        )
        read_only_fields = ("token",)

    def update(self, instance, validated_data):
        """Выполняет обновление User."""
        password = validated_data.pop("password", None)

        for key, value in validated_data.items():

            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
