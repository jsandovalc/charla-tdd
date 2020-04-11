import json
from django.urls import reverse
from rest_framework import status  # Constantes


def test_create_task_201_created(client):
    """Authenticated user can create tasks.

    A 201 is expected.

    """
    response = client.post(
        url=reverse("create-task"),
        data=json.dumps({"description": "Do this talk slides"}),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
