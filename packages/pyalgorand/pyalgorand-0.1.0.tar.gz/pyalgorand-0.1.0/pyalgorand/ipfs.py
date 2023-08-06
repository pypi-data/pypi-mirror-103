import ipfshttpclient
from pathlib import Path
from typing import Union


class IPFS:
    _cached_client = None

    def __init__(
        self,
        url
    ):
        self.url = url
        self.added_on_ipfs = []

    def _connect(self):
        if not self._cached_client:
            self._cached_client = ipfshttpclient.connect(addr=self.url)
        return self._cached_client

    @property
    def client(self):
        return self._connect()

    def add(self, filepath: str, **kwargs):
        item_on_ipfs = self.client.add(filepath, **kwargs)
        self.added_on_ipfs += item_on_ipfs
        return item_on_ipfs

    def delete(self, filepath: str):
        self.client.files.rm(filepath)

    def get_links_from_hash(self, hash):
        oo = self.client.ls(hash)
        return {o['Hash']: o['Links'] for o in oo['Objects']}

    def get(self, hash, local_dir: Union[str, Path] = None, name: str = None):
        self.client.get(hash, local_dir)
        to_file = hash
        if name:
            from_file = local_dir / hash
            to_file = local_dir / name
            Path.rename(from_file, to_file)
        return to_file
