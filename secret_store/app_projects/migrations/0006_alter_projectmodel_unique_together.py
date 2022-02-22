# Generated by Django 3.2.10 on 2022-02-21 14:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app_projects", "0005_auto_20220218_2110"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="projectmodel",
            unique_together={("name", "owner_id")},
        ),
    ]