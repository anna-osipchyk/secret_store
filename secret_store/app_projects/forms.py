from django.forms import ModelForm
from .models import ProjectModel, VariableModel


class NewProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        fields = ("name",)


class VariableForm(ModelForm):
    class Meta:
        model = VariableModel
        fields = (
            "name",
            "value",
        )
