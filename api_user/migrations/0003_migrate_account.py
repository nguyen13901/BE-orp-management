# Generated by Django 4.1 on 2022-09-11 06:59
import os

from django.contrib.auth.hashers import make_password
from django.db import migrations

from api_user.statics import RoleData


def init_account_data(apps, schema_editor):
    account_model = apps.get_model("api_user", "Account")
    role_model = apps.get_model("api_user", "Role")
    profile_model = apps.get_model("api_user", "Profile")
    admin_role = role_model.objects.filter(id=RoleData.ADMIN.value.get('id')).first()
    admin_account = account_model()
    admin_account.email = (
        os.getenv("DEFAULT_ADMIN_EMAIL")
    )
    admin_account.password = make_password(
        os.getenv("DEFAULT_ADMIN_PASSWORD"), salt=os.getenv("SECRET_KEY")
    )  # Todo: Get the value from environment vairable

    admin_account.active = True
    admin_account.save()
    # add role admin and profile
    admin_account.roles.add(admin_role)
    admin_account.save()
    profile = profile_model.objects.create(
        account=admin_account,
        name="Super Administrator",
        gender=3
    )


class Migration(migrations.Migration):

    dependencies = [
        ('api_user', '0004_alter_account'),
    ]

    operations = [
        migrations.RunPython(init_account_data, migrations.RunPython.noop),
    ]
