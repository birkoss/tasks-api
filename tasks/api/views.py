from django.contrib.auth import login, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Task
from users.models import Group, GroupUser

from .serializers import TaskSerializer


class tasksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_pk, format=None):
        group = Group.objects.filter(
            id=group_pk, groupuser__user=request.user).first()

        if group is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.filter(group=group)

        serializer = TaskSerializer(tasks, many=True)

        return Response({
            'tasks': serializer.data,
        }, status=status.HTTP_200_OK)

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
