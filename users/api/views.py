from django.contrib.auth import login, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from core.helpers import send_push_message

from tasks.models import Task, TaskUser
from tasks.api.serializers import TaskSerializer, TaskWriteSerializer

from ..models import User, Group, GroupUser

from .serializers import GroupSerializer, GroupUserSerializer, UserSerializer, UserWriteSerializer


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

    def post(self, request, pk, format=None):
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

        serializer = UserWriteSerializer(data=request.data)
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
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)


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

        tasks = Task.objects.filter(group=group, is_completed=False)
        serializer = TaskSerializer(instance=tasks, many=True)

        return Response({
            "status": status.HTTP_200_OK,
            'tasks': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
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
                'message': "Can't do this",
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(group=group, user=request.user)

            # Notify the Children
            users = User.objects.filter(
                groupuser__is_children=True, groupuser__group=group)
            for user in users:
                if user.expo_token != "":
                    send_push_message(user.expo_token, serializer.data['name'] +
                                      " was added by " + request.user.firstname)

            return Response({
                'task': serializer.data,
                'status': status.HTTP_200_OK
            })

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            'message': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


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

        tasks = Task.objects.filter(taskuser__user=user, is_completed=False)
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


class account(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        groups = GroupUser.objects.filter(user=request.user)

        serializer = GroupUserSerializer(groups, many=True)

        return Response({
            "status": status.HTTP_200_OK,
            'id': request.user.pk,
            'groups': serializer.data,
            'rewards': request.user.rewards,
        }, status=status.HTTP_200_OK)

    def put(self, request, format=None):

        user = User.objects.filter(pk=request.user.pk).first()
        user.expo_token = request.data['expoToken']
        user.save()

        return Response({
            "status": status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)


class loginUser(APIView):
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
            'status': status.HTTP_200_OK,
            'token': token.key,
        }, status=status.HTTP_200_OK)


class registerUser(APIView):
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
                'token': token.key,
            })
        else:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                'message': serializer.errors,
            }, status=status.HTTP_404_NOT_FOUND)
