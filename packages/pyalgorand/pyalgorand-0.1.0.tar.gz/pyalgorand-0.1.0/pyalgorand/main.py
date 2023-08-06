# Create connection
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from pyalgorand.connector import PureStakeConnector
from pyalgorand.account import Account
from pyalgorand.account_manager import AccountManager
from pyalgorand.transactor import Transactor

credentials = './tmp/.purestake'

con = PureStakeConnector(network='testnet')
con.connect()
client = con.algod_client

# check that the client is working with
client.status()

# Create accounts
alice_account = Account(name='Alice')
alice_account.create()
alice_account.save_pickle(filename='../tmp/alice_account.pkl')

bob_account = Account(name='Bob')
bob_account.create()
bob_account.save_pickle(filename='../tmp/bob_account.pkl')

# once you have created your accounts and saved them, you can just load them
alice_account = Account.from_pickle('../tmp/alice_account.pkl')
bob_account = Account.from_pickle('../tmp/bob_account.pkl')

account_manager = AccountManager('../tmp/account_manager.yml')
account_manager.add_account(alice_account)
account_manager.add_account(bob_account)

# Make transaction
transaction_date = datetime.now() + timedelta(seconds=2)
now = datetime.now()
tor = Transactor(
    client,
    sender_private_key=alice_account.private_key,
    sender_address=alice_account.public_address,
    receiver_address=bob_account.public_address,
    amount=100000,
    transaction_date=transaction_date)

# Start the scheduler
sched = BackgroundScheduler()
sched.start()
# Store the job in a variable in case we want to cancel it
job = sched.add_job(tor.transact, trigger='date', run_date=tor.transaction_date)
