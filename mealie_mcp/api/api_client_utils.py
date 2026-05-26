#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def download_file(self, token: Any | None = None) -> Any:
        """Download File"""
        params: dict[str, Any] = {}
        if token is not None:
            params["token"] = token
        return self.request("GET", "/api/utils/download", params=params, data=None)
