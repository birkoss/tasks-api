from rest_framework import serializers

from ..models import Task, TaskUser


class TaskSerializer(serializers.ModelSerializer):
    selected_user_id = serializers.SerializerMethodField()
    selected_user_firstname = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'reward',
                  'selected_user_id', 'selected_user_firstname']
