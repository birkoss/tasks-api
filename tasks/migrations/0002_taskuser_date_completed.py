# Generated by Django 3.0.7 on 2020-06-07 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskuser',
            name='date_completed',
            field=models.DateTimeField(null=True),
        ),
    ]
