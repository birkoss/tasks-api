from django.contrib.auth import login, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User, Group, GroupUser

from .serializers import GroupUserSerializer, UserSerializer


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


class userData(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        groups = GroupUser.objects.filter(user=request.user)

        serializer = GroupUserSerializer(groups, many=True)

        return Response({
            'groups': serializer.data,
            'rewards': request.user.rewards,
        }, status=status.HTTP_200_OK)


class userLogin(APIView):
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


class userRegister(APIView):
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
