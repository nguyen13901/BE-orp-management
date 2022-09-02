# Generated by Django 4.1 on 2022-09-02 10:42
import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


def initial_admin_data(apps, schema_editor):
    role_model = apps.get_model("api_user", "Role")
    account_model = apps.get_model("api_user", "Account")
    user_model = apps.get_model("api_user", "User")

    admin_role = role_model.objects.filter(name='admin').first()
    if admin_role:
        admin_account = account_model(
            email=os.getenv('ADMIN_EMAIL'),
            password=make_password(os.getenv('DEFAULT_ADMIN_PASSWORD')),
            avatar=os.getenv('DEFAULT_ADMIN_AVATAR'),
            role=admin_role,
        )
        admin_account.save()
        admin_user = user_model(
            first_name="Super",
            last_name="Admin",
            gender=3,
            account=admin_account,
        )
        admin_user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0002_migrate_roles'),
    ]

    operations = [
        migrations.RunPython(initial_admin_data, migrations.RunPython.noop),
    ]