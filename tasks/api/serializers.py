from rest_framework import serializers

from ..models import Task, TaskUser
from users.api.serializers import UserSerializer


class TaskUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TaskUser
        fields = ['user', 'date_validated', 'date_completed']


class TaskSerializer(serializers.ModelSerializer):
    taskusers = TaskUserSerializer(source='taskuser_set', many=True)

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'reward',
                  'taskusers']
