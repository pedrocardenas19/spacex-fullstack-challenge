import json
import logging
from typing import Any, Dict, Optional

from .spacex_client import fetch_launches, SpaceXAPIError
from .models import LaunchRecord
from .dynamo_repository import upsert_launch, DynamoRepositoryError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _parse_dry_run(event: Dict[str, Any]) -> bool:
    """
    Determina si la ejecución es dry_run leyendo:
    - event["dry_run"] directamente (invocación manual)
    - event["queryStringParameters"]["dry_run"] si viene por API Gateway
    """
    # Invocación directa desde Lambda test o SDK
    if isinstance(event.get("dry_run"), bool):
        return event["dry_run"]

    if isinstance(event.get("dry_run"), str):
        return event["dry_run"].lower() in ("true", "1", "yes")

    # Invocación vía API Gateway (REST/HTTP)
    qsp = event.get("queryStringParameters") or {}
    dry_param: Optional[str] = qsp.get("dry_run")
    if dry_param is not None:
        return dry_param.lower() in ("true", "1", "yes")

    return False


def sync_launches(dry_run: bool = False) -> Dict[str, Any]:
    """
    Sincroniza todos los lanzamientos de SpaceX a DynamoDB.

    Args:
        dry_run: si es True, no escribe en Dynamo, solo cuenta.

    Returns:
        dict: resumen de la operación.
    """
    logger.info("Starting launches sync (dry_run=%s)", dry_run)

    raw_launches = fetch_launches()
    total = len(raw_launches)
    inserted = 0
    updated = 0

    logger.info("Fetched %d launches from SpaceX API", total)

    for raw in raw_launches:
        record = LaunchRecord.from_v4_dict(raw)
        item = record.to_dynamo_item()

        if dry_run:
            # Solo contamos, no escribimos en Dynamo
            continue

        result = upsert_launch(item)
        if result == "inserted":
            inserted += 1
        else:
            updated += 1

    summary = {
        "total_fetched": total,
        "inserted": inserted,
        "updated": updated,
        "dry_run": dry_run,
    }

    logger.info("Sync summary: %s", summary)
    return summary


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda entrypoint.

    Puede ser invocada:
    - Por EventBridge (cron cada 6h) -> event será casi vacío.
    - Manualmente (test en consola Lambda) pasando {"dry_run": true}.
    - Vía API Gateway, leyendo query param ?dry_run=true.
    """
    logger.info("Received event: %s", json.dumps(event))

    dry_run = _parse_dry_run(event)

    try:
        summary = sync_launches(dry_run=dry_run)
        status_code = 200
        body = {
            "message": "Launches sync completed",
            "summary": summary,
        }
    except SpaceXAPIError as exc:
        logger.exception("SpaceX API error")
        status_code = 502
        body = {
            "message": "Failed to fetch launches from SpaceX API",
            "error": str(exc),
        }
    except DynamoRepositoryError as exc:
        logger.exception("DynamoDB repository error")
        status_code = 500
        body = {
            "message": "Failed to write launches to DynamoDB",
            "error": str(exc),
        }
    except Exception as exc:  # fallback
        logger.exception("Unexpected error")
        status_code = 500
        body = {
            "message": "Unexpected error during launches sync",
            "error": str(exc),
        }

    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
