from django.contrib import admin
from .models import ProjectModel, VariableModel

# Register your models here.
admin.site.register(ProjectModel)
admin.site.register(VariableModel)
