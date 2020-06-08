from django.urls import path

from . import views as api_views


urlpatterns = [
    path('api/tasks', api_views.tasksList.as_view(), name='tasks'),
    path('api/tasks/<str:pk>', api_views.tasksDetail.as_view(), name='task'),
    path('api/tasks/<str:pk>/select',
         api_views.tasksSelect.as_view(), name='task-select'),
    path('api/tasks/<str:pk>/unselect',
         api_views.tasksUnselect.as_view(), name='task-unselect'),
]
