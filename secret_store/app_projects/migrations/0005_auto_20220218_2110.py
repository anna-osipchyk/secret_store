# Generated by Django 3.2.10 on 2022-02-18 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_projects", "0004_auto_20220218_2109"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projectmodel",
            name="variables",
        ),
        migrations.AddField(
            model_name="projectmodel",
            name="variables",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="project",
                to="app_projects.VariableModel",
            ),
        ),
    ]
