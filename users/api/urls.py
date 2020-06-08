from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/register', api_views.register.as_view(), name='register'),
    path('api/login', api_views.login.as_view(), name='login'),
    path('api/account', api_views.account.as_view(), name='data'),

    path('api/groups', api_views.groupsList.as_view(), name='groups'),
    path('api/groups/<str:pk>/tasks',
         api_views.groupsTasksList.as_view(), name='groups-tasks'),
    path('api/groups/<str:pk>/users',
         api_views.groupsUsersList.as_view(), name='groups-users'),

    path('api/users', api_views.usersList.as_view(), name='users'),
    path('api/users/<str:pk>/tasks',
         api_views.usersTasksList.as_view(), name='users-tasks'),

    # path('api/user/task/<str:pk>', api_views.userTask.as_view(), name = 'user-task'),
    # path('api/user/tasks', api_views.userTasks.as_view(), name='user-tasks'),

    # path('api/users/<str:group_pk>', api_views.userUsers.as_view(), name='users'),
]
