from rest_framework import serializers
from . import models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ["id", "description", "created_date", "done"]
        read_only_fields = ["id", "created_date", "done"]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ["id", "description", "created_date", "done"]
        read_only_fields = ["id", "created_date"]
