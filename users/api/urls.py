from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/register', api_views.registerUser.as_view(), name='register'),
    path('api/login', api_views.loginUser.as_view(), name='login'),
    path('api/account', api_views.account.as_view(), name='data'),

    path('api/groups', api_views.groupsList.as_view(), name='groups'),
    path('api/groups/<str:pk>/tasks',
         api_views.groupsTasksList.as_view(), name='groups-tasks'),
    path('api/groups/<str:pk>/users',
         api_views.groupsUsersList.as_view(), name='groups-users'),

    path('api/users', api_views.usersList.as_view(), name='users'),
    path('api/users/<str:pk>/tasks',
         api_views.usersTasksList.as_view(), name='users-tasks'),
]
