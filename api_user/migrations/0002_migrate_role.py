# Generated by Django 4.1 on 2022-09-11 06:45

from django.db import migrations

from api_user.statics import RoleData


def initial_role_data(apps, schema_editor):
    role_model = apps.get_model("api_user", "Role")

    roles = []

    for role in RoleData:
        roles.append(role_model(id=role.value['id'], name=role.value['name'], scope_text=role.value['scope_text'],
                                description=role.value['description']))

    role_model.objects.bulk_create(roles)


def delete_all_data(apps, schema_editor):
    role_model = apps.get_model("api_account", "Role")
    role_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api_user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_role_data, delete_all_data)
    ]
