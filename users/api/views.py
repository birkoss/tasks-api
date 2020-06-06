from django.contrib.auth import login, authenticate

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User

from .serializers import UserSerializer


class userRewards(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):


        return Response({
            'rewards': request.user.rewards,
        }, status=status.HTTP_200_OK)


class userLogin(APIView):
    def post(self, request, format=None):

        user = authenticate(request, email=request.data['email'], password=request.data['password'])
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
