#!/usr/bin/env python
from typing import Any

from mealie_mcp.api.api_client_base import BaseApiClient


class Api(BaseApiClient):
    def get_startup_info(self) -> Any:
        """Get Startup Info"""
        params = None
        return self.request(
            "GET", "/api/app/about/startup-info", params=params, data=None
        )

    def get_app_theme(self) -> Any:
        """Get App Theme"""
        params = None
        return self.request("GET", "/api/app/about/theme", params=params, data=None)
