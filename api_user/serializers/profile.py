from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from api_user.models import Account
from api_user.models.profile import Profile


class ProfileDetailSerializer(ModelSerializer):
    roles = serializers.SerializerMethodField(read_only=True, required=False)
    avatar = serializers.CharField(source='account.avatar', required=False, read_only=True)
    email = serializers.CharField(source='account.email', required=False, read_only=True)
    name = serializers.CharField(required=False)

    class Meta:
        model = Profile
        exclude = ['account']
        ordering = ('created_at', 'updated_at')

    def get_roles(self, obj):
        if obj.account:
            role = obj.account.roles.all().first()
            return {"id": role.id, "name": role.name, "levels": role.levels}
        return {}


class ProfileSerializer(ModelSerializer):
    email = serializers.EmailField(source='account.email')
    password = serializers.CharField(min_length=8, source="account.password")
    avatar = serializers.CharField(source='account.avatar', required=False)

    def validate_email(self, value):
        duplicated_email = Account.objects.by_email(value)
        if duplicated_email is not None:
            raise ValidationError("Email already exists.")
        return value

    class Meta:
        model = Profile
        fields = ('id', 'name', 'gender', 'email', 'password', 'avatar')
        ordering = ('created_at', 'updated_at')


class EmployeeSerializer(ModelSerializer):
    email = serializers.EmailField(source='account.email')
    password = serializers.CharField(min_length=8, source="account.password")
    avatar = serializers.CharField(source='account.avatar', required=False)

    def validate_email(self, value):
        duplicated_email = Account.objects.by_email(value)
        if duplicated_email is not None:
            raise ValidationError("Email already exists.")
        return value

    class Meta:
        model = Profile
        fields = ('id', 'name', 'gender', 'occupation', 'address', 'phone', 'email', 'password', 'avatar')
        ordering = ('created_at', 'updated_at')


class AdopterSerializer(ModelSerializer):
    email = serializers.EmailField(source='account.email')

    class Meta:
        model = Profile
        fields = ('id', 'name', 'gender', 'occupation', 'address', 'phone', 'email')
        ordering = ('created_at', 'updated_at')
