#!/usr/bin/env python3

from abc import ABCMeta, abstractmethod
from coh import __version__
from logging import getLogger
from requests import Session
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Dict, Optional


logger = getLogger(__name__)


class BaseClient(Session, metaclass=ABCMeta):
    """
    Base class for all of the client wrappers.
    """

    def __init__(self, verify: bool = True, proxies: "Optional[Dict[str, str]]" = None) -> None:
        """
        Wrapper for raw requests.Session object, provides a custom User-Agent and Proxy handling if needed.

        :param verify: Should we verify SSL certs (Default is True, DO verify certs.)
        :param proxies: Dict of proxy information to pass to Requests if needed,
            example: {"https": "socks5://127.0.0.1:9999"}
        :return:
        """
        super().__init__()

        # Setup our User-Agent
        self.headers.update({"User-Agent": "python-coh/{}".format(__version__)})

        # Check for proxies and plumb them up if there were any provided
        if proxies is not None:
            logger.debug("Proxy dict provided to COH, adding to underlying Requests Session object")
            self.proxies = proxies

        # Setup Verification (or not)
        if not verify:
            logger.warning("Disabling SSL verification, I hope you know what you're doing...")
            self.verify = False

    @abstractmethod
    def send_command(self, command: str) -> str:
        pass
