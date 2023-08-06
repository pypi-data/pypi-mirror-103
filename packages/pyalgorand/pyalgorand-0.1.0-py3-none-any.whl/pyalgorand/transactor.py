from abc import abstractmethod
from typing import Optional
from datetime import datetime
from algosdk import transaction, template
from algosdk.v2client.algod import AlgodClient
from algosdk.transaction import AssetConfigTxn, AssetTransferTxn


class Transactor:
    _cached_params = {}

    def __init__(
        self,
        client: str,
        sender_address: str,
        sender_private_key: str,
        fee: float = None,
        first_valid_round: int = None,
        last_valid_round: int = None,
        gh: bytes = None
    ):
        self.client = client
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.fee = fee or self._get_fee()
        self.first_valid_round = first_valid_round or self._get_first_valid_round()
        self.last_valid_round = last_valid_round or self._get_last_valid_round()
        self.gh = gh or self._get_gh()

    def _params(self):
        self._cached_params = self.client.suggested_params()
        return self._cached_params

    @property
    def params(self):
        if not self._cached_params:
            self._params()
        return self._cached_params

    @abstractmethod
    def transact(self):
        pass

    def _get_fee(self):
        return self.params.fee

    def _get_first_valid_round(self):
        return self.params.first

    def _get_last_valid_round(self):
        return self.params.last

    def _get_gh(self):
        return self.params.gh

    def _wait_for_confirmation(self):
        """
        Utility function to wait until the transaction is
        confirmed before proceeding.
        """
        client = self.client
        txid = self.txid
        last_round = client.status().get('last-round')
        txinfo = client.pending_transaction_info(txid)
        while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
            print("Waiting for confirmation")
            last_round += 1
            client.status_after_block(last_round)
            txinfo = client.pending_transaction_info(txid)
        print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
        self.txinfo = txinfo
        return txinfo
        # last_round = algodclient.status().get('last-round')
        # while True:
        #    txinfo = algodclient.pending_transaction_info(txid)
        #    self.txinfo = txinfo
        #    self.asset_id = txinfo.get('asset-index')
        #    if not txinfo.get('round'):
        #        break
        #    if txinfo.get('round') and txinfo.get('round') > 0:
        #       print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('round')))
        #       break
        #    else:
        #       print("Waiting for confirmation...")
        #       print('Round:', txinfo.get('round'))
        #       last_round += 1
        #       algodclient.status_after_block(last_round)
        # self.txinfo
        # return txinfo

    def sign_transaction(self, tx):
        signed_tx = tx.sign(self.sender_private_key)
        self.txid = signed_tx.transaction.get_txid()
        return signed_tx

    def send_transaction(self, signed_tx):
        try:
            tx_confirm = self.client.send_transaction(signed_tx)
            self._wait_for_confirmation()
            return tx_confirm
        except Exception as e:
            print(e)


class AssetOptinTransactor(Transactor):

    def __init__(
        self,
        client: str,
        sender_address: str,
        sender_private_key: bytes,
        asset_id: int,
        amount: float,
        fee: float = 1000,
        first_valid_round: int = None,
        last_valid_round: int = None,
        gh: bytes = None,
        transaction_type: str = 'opt-in',
    ):
        self.asset_id = asset_id
        self.amount = amount
        self.transaction_type = transaction_type
        super().__init__(client, sender_address, sender_private_key, fee, first_valid_round, last_valid_round, gh)

    def transact(self):
        tx = AssetTransferTxn(
            sender=self.sender_address,
            fee=self._get_fee(),
            first=self._get_first_valid_round(),
            last=self._get_last_valid_round(),
            gh=self._get_gh(),
            receiver=self.sender_address,
            amt=self.amount,
            index=self.asset_id)

        signed_tx = self.sign_transaction(tx)
        confirm_tx = self.send_transaction(signed_tx)
        return confirm_tx


class AssetTransferTransactor(Transactor):

    def __init__(
        self,
        client: str,
        sender_address: str,
        sender_private_key: bytes,
        asset_id: int,
        amount: float,
        fee: float = 1000,
        first_valid_round: int = None,
        last_valid_round: int = None,
        gh: bytes = None,
        receiver_address: str = None,
        transaction_type: str = 'pay',
    ):
        self.asset_id = asset_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.receiver_address = receiver_address
        super().__init__(client, sender_address, sender_private_key, fee, first_valid_round, last_valid_round, gh)

    def transact(self):
        tx = AssetTransferTxn(
            sender=self.sender_address,
            fee=self._get_fee(),
            first=self._get_first_valid_round(),
            last=self._get_last_valid_round(),
            gh=self._get_gh(),
            receiver=self.receiver_address,
            amt=self.amount,
            index=self.asset_id)

        signed_tx = self.sign_transaction(tx)
        confirm_tx = self.send_transaction(signed_tx)
        return confirm_tx


class SwapAssetTransactor(Transactor):
    def __init__(
        self,
        client: str,
        sender_address: str,
        sender_private_key: bytes,
        asset_id: int,
        asset_amount: float,
        microalgo_amount: float,
        ratn: float,
        ratd: float,
        min_trade: float,
        max_fee: float,
        fee: float = 1000,
        first_valid_round: int = None,
        last_valid_round: int = None,
        gh: bytes = None,
    ):
        self.asset_id = asset_id
        self.asset_amount = asset_amount
        self.microalgo_amount = microalgo_amount
        self.ratn = ratn
        self.ratd = ratd
        self.min_trade = min_trade
        self.max_fee = max_fee
        super().__init__(client, sender_address, sender_private_key, fee, first_valid_round, last_valid_round, gh)

    def transact(self):
        limit = template.LimitOrder(
            owner=self.sender_address,
            asset_id=self.asset_id,
            ratn=self.ratn,
            ratd=self.ratd,
            expiry_round=self.last_valid_round,
            min_trade=self.min_trade,
            max_fee=self.max_fee)
        # addr = limit.get_address()
        program = limit.get_program()
        txns = limit.get_swap_assets_transactions(
            contract=program,
            asset_amount=self.asset_amount,
            microalgo_amount=self.microalgo_amount,
            private_key=self.sender_private_key,
            first_valid=self.first_valid_round,
            last_valid=self.last_valid_round,
            gh=self.gh,
            fee=self.fee)
        # txid = self.client.send_transactions(txns)
        _ = self.client.send_transactions(txns)


class AssetConfigTransactor(Transactor):

    def __init__(
        self,
        client: AlgodClient,
        sender_address: str,
        sender_private_key: bytes,
        total: float,
        unit_name: str,
        asset_name: str,
        fee: float = 1000,
        manager_address: str = None,
        reserve_address: str = None,
        freeze_address: str = None,
        clawback_address: str = None,
        default_frozen: bool = False,
        url: str = None,
        decimal: int = 0,
        note: str = None
    ):
        super().__init__(client, sender_address, sender_private_key)
        self.fee = fee
        self.total = total
        self.unit_name = unit_name
        self.asset_name = asset_name
        self.manager_address = manager_address
        self.reserve_address = reserve_address
        self.freeze_address = freeze_address
        self.clawback_address = clawback_address
        self.default_frozen = default_frozen
        self.url = url
        self.decimal = decimal
        self.note = note

    def transact(self):
        tx = AssetConfigTxn(
            sender=self.sender_address,
            total=self.total,
            fee=self._get_fee(),
            first=self._get_first_valid_round(),
            last=self._get_last_valid_round(),
            gh=self._get_gh(),
            default_frozen=self.default_frozen,
            unit_name=self.unit_name,
            asset_name=self.asset_name,
            manager=self.manager_address,
            reserve=self.reserve_address,
            freeze=self.freeze_address,
            clawback=self.clawback_address,
            url=self.url,
            note=self.note
        )
        signed_tx = self.sign_transaction(tx)
        confirm_tx = self.send_transaction(signed_tx)
        return confirm_tx


class PaymentTransactor(Transactor):

    def __init__(
        self,
        client: AlgodClient,
        sender_private_key: str,
        sender_address: str,
        receiver_address: str,
        amount: float,
        transaction_type: str = 'pay',
        transaction_date: Optional[datetime] = None,
        round_range: int = 1000,
        close_remainder_to_address: str = None,
        note: str = None,
        gen: str = None,
        flat_fee: str = None,
        lease: str = None,
        rekey_to_address: str = None
    ):
        super().__init__(client, sender_address, sender_private_key)
        self.amount = amount
        self.transaction_type = transaction_type
        self.transaction_date = transaction_date
        self.receiver_address = receiver_address
        self.round_range = round_range
        self.close_remainder_to_address = close_remainder_to_address
        self.note = note
        self.gen = gen
        self.flat_fee = flat_fee
        self.lease = lease
        self.rekey_to_address = rekey_to_address

    def transact(self):
        tx = transaction.PaymentTxn(
            sender=self.sender_address,
            fee=self._get_fee(),
            first=self._get_first_valid_round(),
            last=self._get_last_valid_round(),
            gh=self._get_gh(),
            receiver=self.receiver_address,
            amt=self.amount,
            close_remainder_to=self.close_remainder_to_address,
            note=self.note,
            gen=self.gen,
            flat_fee=self.flat_fee,
            lease=self.lease,
            rekey_to=self.rekey_to_address
        )
        signed_tx = self.sign_transaction(tx)
        confirm_tx = self.send_transaction(signed_tx)
        return confirm_tx
