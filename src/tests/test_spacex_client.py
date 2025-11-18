import json
from unittest.mock import patch, MagicMock

import pytest

from src.spacex_client import (
    fetch_launches,
    fetch_upcoming_launches,
    SpaceXAPIError,
)


@patch("src.spacex_client.requests.get")
def test_fetch_launches_success(mock_get):
    # Arrange
    fake_data = [{"id": "abc123", "name": "Test Launch"}]
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_data
    mock_get.return_value = mock_response

    # Act
    result = fetch_launches()

    # Assert
    assert result == fake_data
    mock_get.assert_called_once()
    assert "/launches" in mock_get.call_args[0][0]


@patch("src.spacex_client.requests.get")
def test_fetch_launches_error_status(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Error"
    mock_get.return_value = mock_response

    with pytest.raises(SpaceXAPIError) as exc:
        fetch_launches()

    assert "Failed to fetch launches" in str(exc.value)


@patch("src.spacex_client.requests.get")
def test_fetch_upcoming_success(mock_get):
    fake_data = [{"id": "upcoming1", "name": "Future Launch"}]
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_data
    mock_get.return_value = mock_response

    result = fetch_upcoming_launches()

    assert result == fake_data
    mock_get.assert_called_once()
    assert "/launches/upcoming" in mock_get.call_args[0][0]
