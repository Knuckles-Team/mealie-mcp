#!/usr/bin/env python
from typing import Any
from urllib.parse import urljoin

import requests
import urllib3


class BaseApiClient:
    def __init__(
        self,
        base_url: str | None,
        token: str | None = None,
        verify: bool = False,
        proxies: dict | None = None,
        debug: bool = False,
    ):
        self.base_url = base_url
        self.token = token
        self.verify = verify
        self.proxies = proxies or {}
        self.debug = debug
        self._session = requests.Session()
        self._session.verify = verify

        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
            proxies=self.proxies,
        )

        if response.status_code >= 400:
            raise Exception(f"API error: {response.status_code} - {response.text}")

        if response.status_code == 204:
            return {"status": "success"}

        try:
            return response.json()
        except Exception:
            return {"status": "success", "text": response.text}
