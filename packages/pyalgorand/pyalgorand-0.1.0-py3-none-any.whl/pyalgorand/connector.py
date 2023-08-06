from typing import Union
from pathlib import Path
from algosdk.v2client import algod


class Connector:
    def __init__(
        self,
        network: str = 'testnet',
        credentials: Union[Path, str] = None,
        token: str = None
    ):
        self.network = network
        self.credentials = credentials
        self.token = token or self._get_token_from_credentials_file()
        self.headers = {'X-Api-key': self.token}

    def _get_token_from_credentials_file(self):
        """Credentials file is a 1-line file with only the token
        """
        with open(self.credentials) as h:
            return h.readline().strip()

    def connect(self):
        self.algod_client = algod.AlgodClient(self.token, self.algod_address, headers=self.headers)


class SandboxConnector(Connector):
    def __init__(
        self,
        token: str = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        url: str = 'localhost',
        port: int = 4001
    ):
        super().__init__(network='sandbox', token=token)
        self.algod_address = f'http://{url}:{port}'


class PureStakeConnector(Connector):
    def __init__(
        self,
        network: str = 'testnet',
        credentials: str = '../tmp/.purestake',
        algod_version: str = 'v2'
    ):
        super().__init__(network=network, credentials=credentials)
        self.algod_version = algod_version
        self.algod_address = f'https://{self.network}-algorand.api.purestake.io/ps2'
