from django.db import models

from core.models import TimeStampedModel
from users.models import Group, User


class Task(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')
    description = models.TextField(max_length=200, default='')

    #frequency = 

    reward = models.IntegerField(default=0)


class TaskUser(TimeStampedModel, models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date_validated = models.DateTimeField(null=True)
