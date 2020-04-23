from django.urls import path
from . import views

urlpatterns = [
    path("", views.TaskListCreateApi.as_view(), name="list_create_tasks"),
    path(
        "<int:pk>",
        views.TaskRetrieveUpdateDeleteApi.as_view(),
        name="retrieve_update_delete_task",
    ),
]
