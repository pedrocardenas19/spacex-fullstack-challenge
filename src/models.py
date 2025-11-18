from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class LaunchRecord:
    """Minimal launch representation for DynamoDB."""
    launch_id: str
    mission_name: str
    rocket_id: str
    launch_date_utc: str
    launch_date_unix: int
    status: str  # "success" | "failed" | "upcoming"
    launchpad_id: Optional[str] = None
    details: Optional[str] = None
    article_link: Optional[str] = None
    wikipedia: Optional[str] = None
    video_link: Optional[str] = None

    @classmethod
    def from_v4_dict(cls, data: Dict[str, Any]) -> "LaunchRecord":
        # status derivado de success + upcoming
        upcoming = data.get("upcoming", False)
        success = data.get("success")
        if upcoming:
            status = "upcoming"
        elif success is True:
            status = "success"
        else:
            status = "failed"

        links = data.get("links", {}) or {}
        return cls(
            launch_id=data.get("id", ""),
            mission_name=data.get("name", "Unknown"),
            rocket_id=data.get("rocket", ""),
            launch_date_utc=data.get("date_utc", ""),
            launch_date_unix=data.get("date_unix", 0),
            status=status,
            launchpad_id=data.get("launchpad"),
            details=data.get("details"),
            article_link=links.get("article"),
            wikipedia=links.get("wikipedia"),
            video_link=links.get("webcast"),
        )

    def to_dynamo_item(self) -> Dict[str, Any]:
        """Dict listo para PutItem en Dynamo."""
        return {
            "launch_id": self.launch_id,          # PK principal
            "mission_name": self.mission_name,
            "rocket_id": self.rocket_id,
            "launch_date_utc": self.launch_date_utc,
            "launch_date_unix": self.launch_date_unix,
            "status": self.status,
            "launchpad_id": self.launchpad_id,
            "details": self.details,
            "article_link": self.article_link,
            "wikipedia": self.wikipedia,
            "video_link": self.video_link,
            "updated_at": datetime.utcnow().isoformat(),
        }
