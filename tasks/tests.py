import json
import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status  # Constantes
from . import models
from django.utils import timezone as tz



@pytest.fixture
def authenticated_user(django_user_model, client):
    UserModel = django_user_model

    user = UserModel(username="test")
    user.set_password("test")
    user.save()

    response = client.post(
        reverse("token_obtain_pair"),
        data=json.dumps({"username": "test", "password": "test"}),
        content_type="application/json",
    )

    token = response.json()["access"]
    client.defaults["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    return user


@pytest.mark.django_db
def test_create_task_201_created(client, authenticated_user):
    """Authenticated user can create tasks.

    A 201 is expected.

    """
    response = client.post(
        reverse("list_create_tasks"),
        data=json.dumps({"description": "Do this talk slides"}),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_task_check_db(client, authenticated_user):
    """Authenticated user can create tasks.

    A new row is expected in DB.

    """
    client.post(
        reverse("list_create_tasks"),
        data=json.dumps({"description": "Do this talk slides"}),
        content_type="application/json",
    )

    assert models.Task.objects.count() == 1


@pytest.mark.django_db
def test_list_owner_tasks(client, authenticated_user):
    """A user can list only his tasks."""
    baker.make("Task", owner=authenticated_user, _quantity=3)

    baker.make("Task", _quantity=3)

    response = client.get(reverse("list_create_tasks"))

    assert len(response.data["results"]) == 3


@pytest.mark.django_db
def test_retrieve_task_200(client, authenticated_user):
    """On task retrieval, a 200 is expected."""
    task = baker.make("Task", owner=authenticated_user)

    response = client.get(
        reverse("retrieve_update_delete_task", kwargs={"pk": task.pk})
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_retrieve_task_404_other_user(client, authenticated_user):
    """Cannot retrieve tasks from other users."""
    task = baker.make("Task")

    response = client.get(
        reverse("retrieve_update_delete_task", kwargs={"pk": task.pk})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_task_204(client, authenticated_user):
    """A delete returns 204."""
    task = baker.make("Task", owner=authenticated_user)

    response = client.delete(
        reverse("retrieve_update_delete_task", kwargs={"pk": task.pk})
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_task_404(client, authenticated_user):
    """Cannot delete for other users."""
    task = baker.make("Task")

    response = client.delete(
        reverse("retrieve_update_delete_task", kwargs={"pk": task.pk})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_task_no_rows(client, authenticated_user):
    """The row must be deleted from DB."""
    task = baker.make("Task", owner=authenticated_user)

    client.delete(reverse("retrieve_update_delete_task", kwargs={"pk": task.pk}))

    assert models.Task.objects.count() == 0


@pytest.mark.django_db
def test_task_set_done(client, authenticated_user):
    """Authenticated users can set tasks to done."""
    task = baker.make("Task", owner=authenticated_user, done=False)

    client.patch(
        reverse("retrieve_update_delete_task", kwargs={"pk": task.pk}),
        data=json.dumps({"done": True}),
        content_type="application/json",
    )

    task.refresh_from_db()

    assert task.done


@pytest.mark.django_db
def test_task_cannot_change_creation_dt(client, authenticated_user):
    """Users cannot update creation_dt for task."""
    task = baker.make("Task", owner=authenticated_user, done=False)

    current_creation = task.created_date

    client.patch(
        reverse("retrieve_update_delete_task", kwargs={"pk": task.pk}),
        data=json.dumps({"created_date": tz.now().isoformat()}),
        content_type="application/json",
    )

    task.refresh_from_db()

    assert task.created_date == current_creation
