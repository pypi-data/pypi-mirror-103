import yaml
from pathlib import Path
from pyalgorand.account import Account


class AccountManager:
    def __init__(
        self,
        filename
    ):
        self.filename = filename

    def load_accounts(self):
        if Path(self.filename).exists():
            return yaml.load(open(self.filename))
        else:
            return {}

    def add_account(self, account: Account):
        accounts = self.load_accounts() or {}
        new_account = {
            account.name: {
                'name': account.name,
                'public_address': account.public_address}}
        if hasattr(account, 'nacl_encryption_keys'):
            new_account.update(
                {
                    'nacl_encrytion_public_key': self.nacl_encryption_public_keys.public_key,
                    'nacl_encrytion_private_key': self.nacl_encryption_public_keys._private_key,
                })
        accounts.update(new_account)
        yaml.dump(accounts, open(self.filename, 'w'))
