"""
Base classes for python Rundeck plugin connectors.

"""

import logging
import paramiko

logger = logging.getLogger(__name__)


class BaseConnector:

    """Abstract class for connector"""

    def __init__(self, target) -> None:
        self.tearget = target

    def get_config(self, config: str):
        """Should return configuration requested in yang format
        https://www.openconfig.net/projects/models/"""
        raise NotImplementedError

    def get_status(self, status: str):
        """Should return status requested in yang format
        https://www.openconfig.net/projects/models/"""
        raise NotImplementedError


class SSHConnector(BaseConnector):

    """SSH connector"""

    def __init__(self, target) -> None:
        self.target = target
        self.client = paramiko.SSHClient()
        super().__init__(target)

    def get_config(self, config: str):
        """Should return configuration requested in yang format
        https://www.openconfig.net/projects/models/"""
        print(self.target, config)
        raise NotImplementedError

    def get_status(self, status: str):
        """Should return status requested in yang format
        https://www.openconfig.net/projects/models/"""
        print(self.target, status)
        raise NotImplementedError

    def send_command(self, command: str) -> tuple:
        """Sends a single command returns tuple with
        stdin, stdout, stderr"""
        try:
            print(self.target, command)
        finally:
            print("finally")

    def send_commands(self, commands: list) -> dict:
        """Sends multiple commands returns dict of tuples with
        command : stdin, stdout, stderr"""
        try:
            for command in commands:
                print(self.target, command)
                print(f"{command} from commands list")
        finally:
            print("finally should disconnect")


class RESTConnector(BaseConnector):
    """REST connector."""

    def __init__(self, target) -> None:
        self.target = target
        logger.warning("REST connector needs implementation")
        super().__init__(target)

    def get_url(self: str) -> dict:
        """Get specified API URL return session results"""
        print(self.target)
        raise NotImplementedError

    def get_urls(self, urls: list) -> dict:
        """Get a list of specified API URLs return sessions results"""
        print(self.target)
        print("for url in {}, get response".format(urls))
        raise NotImplementedError

    def get_config(self, config: str) -> dict:
        """Get named configuration return configuration"""
        print(self.target)
        print("get {} and return as yang".format(config))
        raise NotImplementedError

    def get_status(self, status: str):
        """Should return status requested in yang format
        https://www.openconfig.net/projects/models/"""
        print(self.target, status)
        raise NotImplementedError
