from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from . import serializers, models


class OwnerQuerysetMixin:
    """I should go first!!"""
    def get_queryset(self):
        return models.Task.objects.filter(owner=self.request.user)


class TaskListCreateApi(OwnerQuerysetMixin, ListCreateAPIView):
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDeleteApi(OwnerQuerysetMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.TaskUpdateSerializer
