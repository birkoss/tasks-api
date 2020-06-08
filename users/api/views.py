from django.contrib.auth import login, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task, TaskUser
from tasks.api.serializers import TaskSerializer

from ..models import User, Group, GroupUser

from .serializers import GroupSerializer, GroupUserSerializer, UserSerializer


class groupsUsersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        group = Group.objects.filter(id=pk).first()

        # Group doesnt exist
        if group is None:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        group_user = GroupUser.objects.filter(
            group=group, user=request.user).first()

        # User is not in this group?
        if group_user is None:
            return Response({
                'status': status.HTTP_403_FORBIDDEN,
                'message': "Can't access this",
            }, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.filter(groupuser__group=group)

        return Response({
            "status": status.HTTP_200_OK,
            'users': UserSerializer(users, many=True).data,
        }, status=status.HTTP_200_OK)


class groupsTasksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        group = Group.objects.filter(id=pk).first()

        # Group doesnt exist
        if group is None:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        group_user = GroupUser.objects.filter(
            group=group, user=request.user).first()

        # User is not in this group?
        if group_user is None:
            return Response({
                'status': status.HTTP_403_FORBIDDEN,
                'message': "Can't access this",
            }, status=status.HTTP_403_FORBIDDEN)

        tasks = Task.objects.filter(group=group)
        serializer = TaskSerializer(instance=tasks, many=True)

        return Response({
            "status": status.HTTP_200_OK,
            'tasks': serializer.data,
        }, status=status.HTTP_200_OK)


class groupsList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        groups = Group.objects.filter(
            groupuser__user=request.user)

        return Response({
            "status": status.HTTP_200_OK,
            'groups': GroupSerializer(groups, many=True).data,
        }, status=status.HTTP_200_OK)


class usersTasksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        user = User.objects.filter(id=pk).first()

        # User doesnt exist
        if user is None:
            return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        # Not the same user
        # @TODO If the request is made by a parent, allow it
        # if request.user != user:
        #     return Response({
        #         'status': status.HTTP_404_NOT_FOUND,
        #         'message': "You can only access your own tasks",
        #     }, status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.filter(taskuser__user=user)
        serializer = TaskSerializer(instance=tasks, many=True)

        return Response({
            "status": status.HTTP_200_OK,
            'tasks': serializer.data,
        }, status=status.HTTP_200_OK)


class usersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        users = User.objects.filter(
            groupuser__group__groupuser__user=request.user)

        return Response({
            "status": status.HTTP_200_OK,
            'users': UserSerializer(users, many=True).data,
        }, status=status.HTTP_200_OK)


class userTask(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, format=None):

        task = Task.objects.filter(pk=pk).first()

        # Task doesnt exist
        if task is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        group_user = GroupUser.objects.filter(
            group=task.group, user=request.user).first()

        # User not in the task group
        if group_user is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        task_user = TaskUser.objects.filter(
            task=task, user=request.user).first()

        # Task NOT selected by the user ?
        if task_user is None:
            return Response({
                'message': "This task is not selected by you",
            }, status=status.HTTP_404_NOT_FOUND)

        # Delete it to this user
        task_user.delete()

        return Response({
            'status': status.HTTP_200_OK
        })


class userTasks(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_pk, format=None):
        group = Group.objects.filter(
            id=group_pk, groupuser__user=request.user).first()

        if group is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        users = []
        groups = GroupUser.objects.filter(group=group)
        for group in groups:
            users.append({
                'user': UserSerializer(group.user, many=False).data,
                'is_children': group.is_children,
            })

        return Response({
            'users': users,
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):

        # Missing task_id param
        if 'task_id' not in request.data:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        task = Task.objects.filter(pk=request.data['task_id']).first()

        # Task doesnt exist
        if task is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        group_user = GroupUser.objects.filter(
            group=task.group, user=request.user).first()

        # User not in the task group
        if group_user is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        task_user = TaskUser.objects.filter(task=task).first()

        # Task already selected by another user
        if task_user is not None:
            return Response({
                'message': "Already selected by another user",
            }, status=status.HTTP_404_NOT_FOUND)

        # Link it to this user
        task_user = TaskUser(user=request.user, task=task)
        task_user.save()

        return Response({
            'status': status.HTTP_200_OK
        })


class userUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_pk, format=None):
        group = Group.objects.filter(
            id=group_pk, groupuser__user=request.user).first()

        if group is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        users = []
        groups = GroupUser.objects.filter(group=group)
        for group in groups:
            users.append({
                'user': UserSerializer(group.user, many=False).data,
                'is_children': group.is_children,
            })

        return Response({
            'users': users,
        }, status=status.HTTP_200_OK)

    def post(self, request, group_pk, format=None):
        group = Group.objects.filter(
            id=group_pk, groupuser__user=request.user).first()

        if group is None:
            return Response({
                'message': "Not found",
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.data['email'],
                request.data['password'],
                firstname=serializer.data['firstname'],
            )

            # Link the user with the group
            group_user = GroupUser(group=group, user=user)
            group_user.save()

            return Response({
                'status': status.HTTP_200_OK
            })
        else:
            return Response({
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)


class account(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        groups = GroupUser.objects.filter(user=request.user)

        serializer = GroupUserSerializer(groups, many=True)

        return Response({
            'groups': serializer.data,
            'rewards': request.user.rewards,
        }, status=status.HTTP_200_OK)


class login(APIView):
    def post(self, request, format=None):

        user = authenticate(
            request, email=request.data['email'], password=request.data['password'])
        if user is None:
            return Response({
                'message': 'Invalid information'
            }, status=status.HTTP_404_NOT_FOUND)

        login(request, user)

        token = Token.objects.get(user=user)

        return Response({
            'token': token.key,
        }, status=status.HTTP_200_OK)


class register(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.data['email'],
                request.data['password']
            )

            token = Token.objects.get(user=user)

            return Response({
                'status': status.HTTP_200_OK,
                'item': serializer.data,
                'token': token.key,
            })
        else:
            return Response({
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)
