import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Mock boto3 before importing app.main
with patch("boto3.resource") as mock_boto3:
    mock_dynamodb = MagicMock()
    mock_boto3.return_value = mock_dynamodb
    from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


@patch("app.main.table")
def test_list_launches(mock_table):
    # Mock DynamoDB scan response
    mock_table.scan.return_value = {
        "Items": [
            {
                "launch_id": "1",
                "mission_name": "Test Mission",
                "rocket_id": "rocket123",
                "launch_date_utc": "2020-01-01T00:00:00.000Z",
                "launch_date_unix": 1577836800,
                "status": "success",
            }
        ]
    }

    response = client.get("/launches")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["launch_id"] == "1"
    assert data[0]["status"] == "success"


@patch("app.main.table")
def test_get_launch(mock_table):
    mock_table.get_item.return_value = {
        "Item": {
            "launch_id": "1",
            "mission_name": "Test Mission",
            "rocket_id": "rocket123",
            "launch_date_utc": "2020-01-01T00:00:00.000Z",
            "launch_date_unix": 1577836800,
            "status": "success",
        }
    }

    response = client.get("/launches/1")

    assert response.status_code == 200
    data = response.json()
    assert data["launch_id"] == "1"
    assert data["status"] == "success"


@patch("app.main.table")
def test_get_launch_not_found(mock_table):
    mock_table.get_item.return_value = {}  # No Item

    response = client.get("/launches/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Launch not found"


@patch("app.main.table")
def test_stats_summary(mock_table):
    mock_table.scan.return_value = {
        "Items": [
            {
                "launch_id": "1",
                "mission_name": "Mission 1",
                "rocket_id": "r1",
                "launch_date_utc": "2020-01-01T00:00:00.000Z",
                "launch_date_unix": 1577836800,
                "status": "success",
            },
            {
                "launch_id": "2",
                "mission_name": "Mission 2",
                "rocket_id": "r2",
                "launch_date_utc": "2021-01-01T00:00:00.000Z",
                "launch_date_unix": 1609459200,
                "status": "failed",
            },
        ]
    }

    response = client.get("/stats/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["by_status"]["success"] == 1
    assert data["by_status"]["failed"] == 1
    assert data["by_year"]["2020"] == 1
    assert data["by_year"]["2021"] == 1
