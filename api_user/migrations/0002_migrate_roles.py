# Generated by Django 4.1 on 2022-09-02 10:28
import json

from django.db import migrations


def initial_role_data(apps, schema_editor):
    role_model = apps.get_model("api_user", "Role")
    with open('api_user/statics/roles.json', 'r') as f:
        role_data = json.load(f)
        roles = []

        for role in role_data:
            roles.append(
                role_model(
                    name=role.get('name'),
                    scope_text=role.get('scope_text'),
                    description=role.get('description'),
                    is_default=role.get('is_default')
                )
            )

        role_model.objects.bulk_create(roles)


def delete_all_roles(apps, schema_editor):
    role_model = apps.get_model("api_account", "Role")
    role_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_role_data, delete_all_roles),
    ]
