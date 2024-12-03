import pytest
from unittest.mock import patch, MagicMock
from app.main import app

@pytest.fixture
def client():
    """Flask test client fixture"""
    with app.test_client() as client:
        yield client

def test_create_task_success(client):
    """Test successful creation of a task"""
    mock_insert_one = MagicMock()
    with patch("app.routes.tasks_collection.insert_one", mock_insert_one):
        response = client.post(
            "/tasks",
            json={"title": "Test Task", "description": "This is a test task."}
        )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Task created"
    mock_insert_one.assert_called_once()

def test_create_task_missing_data(client):
    """Test creation of a task with missing fields"""
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Title and description are required"

def test_list_tasks_success(client):
    """Test listing all tasks"""
    mock_find = MagicMock(return_value=[
        {"id": "1", "title": "Task 1", "description": "Description 1"},
        {"id": "2", "title": "Task 2", "description": "Description 2"}
    ])
    with patch("app.routes.tasks_collection.find", mock_find):
        response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_task_success(client):
    """Test retrieving a specific task"""
    mock_find_one = MagicMock(return_value={"id": "1", "title": "Task 1", "description": "Description 1"})
    with patch("app.routes.tasks_collection.find_one", mock_find_one):
        response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Task 1"

def test_get_task_not_found(client):
    """Test retrieving a non-existent task"""
    mock_find_one = MagicMock(return_value=None)
    with patch("app.routes.tasks_collection.find_one", mock_find_one):
        response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"

def test_update_task_success(client):
    """Test updating a task successfully"""
    mock_update_one = MagicMock(return_value=MagicMock(matched_count=1))
    with patch("app.routes.tasks_collection.update_one", mock_update_one):
        response = client.put(
            "/tasks/1",
            json={"title": "Updated Task"}
        )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task updated"
    mock_update_one.assert_called_once()

def test_update_task_not_found(client):
    """Test updating a non-existent task"""
    mock_update_one = MagicMock(return_value=MagicMock(matched_count=0))
    with patch("app.routes.tasks_collection.update_one", mock_update_one):
        response = client.put(
            "/tasks/999",
            json={"title": "Updated Task"}
        )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"

def test_delete_task_success(client):
    """Test deleting a task successfully"""
    mock_delete_one = MagicMock(return_value=MagicMock(deleted_count=1))
    with patch("app.routes.tasks_collection.delete_one", mock_delete_one):
        response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Task deleted"

def test_delete_task_not_found(client):
    """Test deleting a non-existent task"""
    mock_delete_one = MagicMock(return_value=MagicMock(deleted_count=0))
    with patch("app.routes.tasks_collection.delete_one", mock_delete_one):
        response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"
