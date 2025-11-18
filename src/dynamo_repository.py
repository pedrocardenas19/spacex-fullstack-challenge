"""
DynamoDB repository for SpaceX launches.
"""

import os
from typing import Any, Dict, List, Optional, Tuple

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class DynamoRepositoryError(Exception):
    """Custom exception for DynamoDB repository errors."""
    pass


def _get_table():
    """
    Returns a DynamoDB Table resource using the table name from env vars.

    Env:
        LAUNCHES_TABLE_NAME: name of the DynamoDB table.
    """
    table_name = os.environ.get("LAUNCHES_TABLE_NAME", "spacex_launches")
    if not table_name:
        raise DynamoRepositoryError("LAUNCHES_TABLE_NAME env var is not set.")

    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)


def upsert_launch(item: Dict[str, Any]) -> str:
    """
    Insert or update a launch item in DynamoDB.

    Uses PutItem with ReturnValues='ALL_OLD' to detect if the item existed.

    Args:
        item: dict with at least 'launch_id' as primary key.

    Returns:
        str: "inserted" if new item, "updated" if it replaced an existing item.

    Raises:
        DynamoRepositoryError: on DynamoDB errors or invalid input.
    """
    if "launch_id" not in item:
        raise DynamoRepositoryError("Item must contain 'launch_id' as primary key.")

    table = _get_table()

    try:
        response = table.put_item(
            Item=item,
            ReturnValues="ALL_OLD",  # if existed, returns old item
        )
    except (BotoCoreError, ClientError) as exc:
        raise DynamoRepositoryError(f"Error writing item to DynamoDB: {exc}")

    if "Attributes" in response:
        return "updated"
    return "inserted"


def get_launch(launch_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single launch by its launch_id.

    Args:
        launch_id: primary key.

    Returns:
        dict | None
    """
    table = _get_table()

    try:
        response = table.get_item(Key={"launch_id": launch_id})
    except (BotoCoreError, ClientError) as exc:
        raise DynamoRepositoryError(f"Error reading item from DynamoDB: {exc}")

    return response.get("Item")


def list_launches(
    limit: int = 100,
    last_evaluated_key: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Scan launches table (paginated).

    Args:
        limit: max items to return.
        last_evaluated_key: key from previous scan for pagination.

    Returns:
        (items, next_key)
    """
    table = _get_table()

    scan_kwargs: Dict[str, Any] = {"Limit": limit}
    if last_evaluated_key:
        scan_kwargs["ExclusiveStartKey"] = last_evaluated_key

    try:
        response = table.scan(**scan_kwargs)
    except (BotoCoreError, ClientError) as exc:
        raise DynamoRepositoryError(f"Error scanning DynamoDB: {exc}")

    items = response.get("Items", [])
    next_key = response.get("LastEvaluatedKey")
    return items, next_key
