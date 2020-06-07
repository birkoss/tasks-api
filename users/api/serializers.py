from rest_framework import serializers

from users.models import Group, GroupUser, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class GroupSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'user']


class GroupUserSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False, read_only=True)

    class Meta:
        model = GroupUser
        fields = ['group']
