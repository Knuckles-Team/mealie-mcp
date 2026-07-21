#!/usr/bin/env python
from typing import Any
from urllib.parse import urljoin

import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)


class BaseApiClient:
    def __init__(
        self,
        base_url: str | None,
        token: str | None = None,
        tls_profile: ResolvedTLSProfile | None = None,
        debug: bool = False,
    ):
        self.base_url = base_url
        self.token = token
        self.debug = debug
        self.tls_profile = tls_profile or resolve_configured_tls_profile("mealie")
        self._session = self.tls_profile.configure_requests_session(requests.Session())

        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None,
        files: dict | None = None,
    ) -> Any:
        url = urljoin(self.base_url or "", endpoint)

        response = self._session.request(
            method=method,
            url=url,
            params=params,
            json=data,
            files=files,
        )

        if response.status_code >= 400:
            raise Exception(f"API error: {response.status_code}")

        if response.status_code == 204:
            return {"status": "success"}

        try:
            return response.json()
        except Exception:
            return {"status": "success", "text": response.text}

    def close(self) -> None:
        """Release transport resources and runtime-only TLS material."""
        self._session.close()
        self.tls_profile.cleanup()
