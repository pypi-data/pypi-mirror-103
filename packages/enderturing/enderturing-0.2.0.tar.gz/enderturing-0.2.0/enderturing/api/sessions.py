from datetime import date, datetime
from typing import List, TypedDict, Union

from enderturing import Config
from enderturing.api.api_utils import _to_date_range
from enderturing.http_client import HttpClient


SessionsList = TypedDict(
    "SessionsList",
    {
        "total": int,
        "items": List[dict],
    },
)


class Sessions:
    def __init__(self, config: Config, client: HttpClient):
        """
        Args:
            config (Config): configuration to use.
            client (HttpClient): HTTP client instance to use for requests
        """
        self._config = config
        self._http_client = client

    def get_session(self, session_id: str):
        return self._http_client.get(f"/sessions/{session_id}/data/")

    def list(
        self,
        *,
        skip: int = 0,
        max_results: int = 50,
        from_date: Union[str, datetime, date] = None,
        to_date: Union[str, datetime, date] = None,
        caller_id: str = None,
        language: str = None,
    ) -> SessionsList:
        params = {
            "date_range": _to_date_range(from_date, to_date),
            "caller_id": caller_id,
            "language": language,
            "skip": skip,
            "limit": max_results,
        }
        return self._http_client.get("/sessions/", params=params)

    def update(self, session_id: str, session_data: dict):
        return self._http_client.put(f"/sessions/{session_id}/data/", json=session_data)
