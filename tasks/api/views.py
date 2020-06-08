from django.contrib.auth import login, authenticate
from django.db.models import F
from django.core import serializers

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Task, TaskUser
from users.models import Group, GroupUser

from .serializers import TaskSerializer


class tasksSelect(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):

        task = Task.objects.filter(pk=pk).first()

        # Task doesnt exist
        if task is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        group_user = GroupUser.objects.filter(
            group=task.group, user=request.user).first()

        # User not in the task group
        if group_user is None:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                'message': "You are not allowed to do this",
            }, status=status.HTTP_401_UNAUTHORIZED)

        task_user = TaskUser.objects.filter(task=task).first()

        # Task already selected by another user
        if task_user is not None:
            return Response({
                "status": status.HTTP_403_FORBIDDEN,
                'message': "Already selected by another user",
            }, status=status.HTTP_403_FORBIDDEN)

        # Link it to this user
        task_user = TaskUser(user=request.user, task=task)
        task_user.save()

        return Response({
            'status': status.HTTP_200_OK
        })


class tasksUnselect(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, format=None):

        task = Task.objects.filter(pk=pk).first()

        # Task doesnt exist
        if task is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        group_user = GroupUser.objects.filter(
            group=task.group, user=request.user).first()

        # User not in the task group
        if group_user is None:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                'message': "You are not allowed to do this",
            }, status=status.HTTP_401_UNAUTHORIZED)

        task_user = TaskUser.objects.filter(task=task).first()

        # Task already selected by another user
        if task_user is None:
            return Response({
                "status": status.HTTP_403_FORBIDDEN,
                'message': "This task is not selected by you",
            }, status=status.HTTP_403_FORBIDDEN)

        # Unlink it
        task_user.delete()

        return Response({
            'status': status.HTTP_200_OK
        })


class tasksDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, format=None):
        task = Task.objects.filter(id=pk).first()

        if task is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not your task"
            }, status.HTTP_404_NOT_FOUND)

        group = GroupUser.objects.filter(
            group=task.group, user=request.user, is_children=False).first()

        if group is None:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "This is not your task"
            }, status.HTTP_401_UNAUTHORIZED)

        if request.method == 'DELETE':
            task.delete()
            return Response({
                "status": status.HTTP_200_OK
            })

    def get(self, request, pk, format=None):
        task = Task.objects.filter(id=pk).first()

        if task is None:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "message": "This is not your task"
            }, status.HTTP_404_NOT_FOUND)

        group = GroupUser.objects.filter(
            group=task.group, user=request.user, is_children=False).first()

        if group is None:
            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": "This is not your task"
            }, status.HTTP_401_UNAUTHORIZED)

        serializer = TaskSerializer(instance=task, many=False)

        return Response({
            'status': status.HTTP_200_OK,
            'task': serializer.data
        }, status=status.HTTP_200_OK)


class tasksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        tasks = Task.objects.filter(group__groupuser__user=request.user)
        serializer = TaskSerializer(instance=tasks, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'tasks': serializer.data
        }, status=status.HTTP_200_OK)
