# Generated by Django 3.2.10 on 2022-02-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_projects", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projectmodel",
            name="variables",
            field=models.ManyToManyField(
                null=True, related_name="project", to="app_projects.VariableModel"
            ),
        ),
    ]
