from algosdk import account, mnemonic
import pickle
from typing import ByteString, Optional
from pathlib import Path
from nacl.public import PrivateKey, Box


class Account(object):
    """This class allows to create an Algorand account.
    """
    def __init__(
        self,
        name,
        mode: Optional[str] = 'test'
    ):
        self.name = name
        self.mode = mode

    def create(self):
        private_key, public_address = account.generate_account()
        secret_words = mnemonic.from_private_key(private_key)
        if self.mode == 'test':
            print(
                f'Base64 Private Key: {private_key}\n'
                f'Public Algorand Address: {public_address}\n'
                f'my secret words: {secret_words}'
            )
        self.private_key = private_key
        self.public_address = public_address
        self.secret_words = secret_words

    @staticmethod
    def from_pickle(filename: str or Path):
        return pickle.load(open(filename, 'rb'))

    def save_pickle(self, filename: str or Path):
        pickle.dump(self, open(filename, 'wb'))

    def create_encryption_nacl_keys(self):
        self.nacl_encryption_keys = PrivateKey.generate()
        return self.nacl_encryption_keys

    def encrypt_file_with_nacl(
        self,
        filepath: Path,
        external_public_key: ByteString,
        to_file: Path = None
    ):
        """ Encrypt file with the NaCl encryption system invented by Daniel J. Bernstein.
        """
        # Bob wishes to send Alice an encrypted message so Bob must make a Box with
        #   his private key and Alice's public key
        if not hasattr(self, 'nacl_encryption_keys'):
            self.create_encryption_nacl_keys()
        box = Box(self.nacl_encryption_keys, external_public_key)
        with open(filepath, 'rb') as f:
            encrypted = box.encrypt(f.read())
        if to_file:
            with open(to_file, 'wb') as h:
                h.write(encrypted)
            return
        return encrypted

    def decrypt_file_with_nacl(
        self,
        filepath: Path,
        external_public_key: ByteString
    ):
        """Decrypt file with the NaCl encryption system invented by Daniel J. Bernstein.
        """
        box = Box(self.nacl_encryption_keys, external_public_key)
        with open(filepath, 'rb') as f:
            decrypted = box.decrypt(f.read())
        return decrypted
