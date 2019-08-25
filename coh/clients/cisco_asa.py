#!/usr/bin/env python3

from coh.clients.base_client import BaseClient
from logging import getLogger
from typing import TYPE_CHECKING
from urllib.parse import quote_plus


if TYPE_CHECKING:
    from typing import Dict, Optional


logger = getLogger(__name__)


class CiscoASA(BaseClient):
    """
    Client for interacting with a Cisco ASA
    """

    base_url = "https://{0}:{1}/admin/exec/"

    def __init__(
        self,
        ip: str,
        port: int,
        username: str,
        password: str,
        verify: bool = True,
        proxies: "Optional[Dict[str, str]]" = None,
    ) -> None:
        """
        Wrapper for raw requests.Session object, provides a custom User-Agent and Proxy handling if needed.

        :param ip: IP address of the ASA we're connecting to
        :param port: TCP Port for management on the ASA
        :param username: Username for authentication on the ASA
        :param password: Password for authentication on the ASA
        :param verify: Should we verify SSL certs (Default is True, DO verify certs.)
        :param proxies: Dict of proxy information to pass to Requests if needed,
            example: {"https": "socks5://127.0.0.1:9999"}
        :return:
        """
        super().__init__(verify=verify, proxies=proxies)

        self.auth = (username, password)

        self.url = self.base_url.format(ip, port)

        # Cisco ASA's above 9.12 require specific user-agent headers, updating with ASDM for the default
        self.headers.update({"User-Agent": "ASDM"})

    def send_command(self, command: str) -> "Optional[str]":
        """
        Pass the provided string to the ASA and return the output.
        :param command:
        :return:
        """

        try:
            response = self.get(url=self.url + quote_plus(command))
        except Exception as e:
            logger.error("exception reaching ASA: ", e)
            return None

        if response.ok:
            return response.text
        else:
            return None
