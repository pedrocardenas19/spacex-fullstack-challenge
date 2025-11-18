from src.models import LaunchRecord


def test_launch_record_from_v4_dict_success():
    raw = {
        "id": "abc123",
        "name": "Test Mission",
        "rocket": "rocket123",
        "date_utc": "2020-01-01T00:00:00.000Z",
        "date_unix": 1577836800,
        "success": True,
        "upcoming": False,
        "launchpad": "pad42",
        "details": "Some details",
        "links": {
            "article": "https://example.com/article",
            "wikipedia": "https://wikipedia.org/wiki/Test",
            "webcast": "https://youtube.com/watch?v=xyz",
        },
    }

    record = LaunchRecord.from_v4_dict(raw)

    assert record.launch_id == "abc123"
    assert record.mission_name == "Test Mission"
    assert record.rocket_id == "rocket123"
    assert record.launch_date_utc == "2020-01-01T00:00:00.000Z"
    assert record.launch_date_unix == 1577836800
    assert record.status == "success"
    assert record.launchpad_id == "pad42"
    assert record.details == "Some details"
    assert record.article_link.endswith("article")


def test_launch_record_to_dynamo_item():
    record = LaunchRecord(
        launch_id="abc123",
        mission_name="Test Mission",
        rocket_id="rocket123",
        launch_date_utc="2020-01-01T00:00:00.000Z",
        launch_date_unix=1577836800,
        status="upcoming",
        launchpad_id="pad42",
        details="Some details",
        article_link=None,
        wikipedia=None,
        video_link=None,
    )

    item = record.to_dynamo_item()

    assert item["launch_id"] == "abc123"
    assert item["mission_name"] == "Test Mission"
    assert item["rocket_id"] == "rocket123"
    assert item["launch_date_unix"] == 1577836800
    assert item["status"] == "upcoming"
    assert "updated_at" in item  # timestamp
