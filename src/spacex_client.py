import requests

SPACEX_BASE_URL = "https://api.spacexdata.com/v4"


class SpaceXAPIError(Exception):
    """Custom exception for SpaceX API errors."""
    pass


def fetch_launches():
    """Fetches the list of SpaceX launches from the SpaceX API."""
    url = f"{SPACEX_BASE_URL}/launches"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as exc:
        raise SpaceXAPIError(f"Error connecting to SpaceX API: {exc}")

    if response.status_code != 200:
        raise SpaceXAPIError(
            f"Failed to fetch launches: {response.status_code} - {response.text}"
        )

    try:
        return response.json()
    except ValueError:
        raise SpaceXAPIError("Failed to parse JSON from SpaceX API.")


def fetch_upcoming_launches():
    """Fetches the list of upcoming SpaceX launches."""
    url = f"{SPACEX_BASE_URL}/launches/upcoming"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as exc:
        raise SpaceXAPIError(f"Error connecting to SpaceX API: {exc}")

    if response.status_code != 200:
        raise SpaceXAPIError(
            f"Failed to fetch upcoming launches: {response.status_code} - {response.text}"
        )

    try:
        return response.json()
    except ValueError:
        raise SpaceXAPIError("Failed to parse JSON from SpaceX API.")
