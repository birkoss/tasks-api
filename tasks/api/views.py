from django.contrib.auth import login, authenticate
from django.db.models import F
from django.core import serializers

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Task
from users.models import Group, GroupUser

from .serializers import TaskSerializer


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


class asas(APIView):

    def post(self, request, group_pk, format=None):
        group = Group.objects.filter(
            id=group_pk, groupuser__user=request.user).first()

        if group is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=group, user=request.user)

            return Response({
                'task': serializer.data,
                'status': status.HTTP_200_OK
            })
        else:
            return Response({
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)
