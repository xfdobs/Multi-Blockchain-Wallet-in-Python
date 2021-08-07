import subprocess
import json
from dotenv import load_dotenv
from constants import *
import os
from web3 import Account, middleware, Web3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from constants import *
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account

from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Running the local chain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = f'php ./derive -g --mnemonic="{mnemonic}" --coin={coin} --numderive={numderive} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(mnemonic, ETH, 3),
    BTCTEST: derive_wallets(mnemonic, BTCTEST, 3),
    BTC: derive_wallets(mnemonic, BTC, 3)
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin is BTCTEST:
        return PrivateKeyTestnet(priv_key)
    elif coin is ETH:
        return Account.privateKeyToAccount(priv_key)
    

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin is BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    elif coin is ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, 
             "to": to, 
             "value": amount}
        )
        return {
            'chainId': 888,
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin is BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed_tx)
    elif coin is ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)