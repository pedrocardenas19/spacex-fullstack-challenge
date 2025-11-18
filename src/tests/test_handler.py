import json
from unittest.mock import patch

from src.handler import sync_launches, lambda_handler


@patch("src.handler.upsert_launch")
@patch("src.handler.LaunchRecord")
@patch("src.handler.fetch_launches")
def test_sync_launches_persists_data(mock_fetch, mock_launch_record_cls, mock_upsert):
    # Mock SpaceX data
    mock_fetch.return_value = [
        {"id": "1", "name": "Launch 1"},
        {"id": "2", "name": "Launch 2"},
    ]

    # LaunchRecord.from_v4_dict -> instancia mock con to_dynamo_item
    mock_record_instance = mock_launch_record_cls.from_v4_dict.return_value
    mock_record_instance.to_dynamo_item.return_value = {"launch_id": "1"}

    # Primer put -> inserted, segundo -> updated
    mock_upsert.side_effect = ["inserted", "updated"]

    summary = sync_launches(dry_run=False)

    assert summary["total_fetched"] == 2
    assert summary["inserted"] == 1
    assert summary["updated"] == 1

    assert mock_fetch.called
    assert mock_launch_record_cls.from_v4_dict.call_count == 2
    assert mock_upsert.call_count == 2


@patch("src.handler.sync_launches")
def test_lambda_handler_success(mock_sync):
    mock_sync.return_value = {
        "total_fetched": 3,
        "inserted": 2,
        "updated": 1,
        "dry_run": False,
    }

    event = {"dry_run": False}
    result = lambda_handler(event, context=None)

    assert result["statusCode"] == 200

    body = json.loads(result["body"])
    assert body["message"] == "Launches sync completed"
    assert body["summary"]["total_fetched"] == 3
    mock_sync.assert_called_once_with(dry_run=False)


@patch("src.handler.sync_launches")
def test_lambda_handler_dry_run_detection(mock_sync):
    mock_sync.return_value = {
        "total_fetched": 1,
        "inserted": 0,
        "updated": 0,
        "dry_run": True,
    }

    event = {
        "queryStringParameters": {"dry_run": "true"}
    }
    result = lambda_handler(event, context=None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["summary"]["dry_run"] is True
    mock_sync.assert_called_once_with(dry_run=True)
