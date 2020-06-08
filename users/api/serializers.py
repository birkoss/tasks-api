from rest_framework import serializers

from users.models import Group, GroupUser, User


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname']


class GroupSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(many=False, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'user']


class GroupUserSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False, read_only=True)

    class Meta:
        model = GroupUser
        fields = ['is_children', 'group']


class UserSerializer(serializers.ModelSerializer):
    groups = GroupUserSerializer(source='groupuser_set', many=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'rewards', 'groups']
