import subprocess
import json
from dotenv import load_dotenv
from constants import *
import os
from web3 import Account, middleware, Web3
from web3.middleware import geth_poa_middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy


# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

 
# Create a function called `derive_wallets`
def derive_wallets(mnemonic_p=mnemonic,coin,format):
    command = # YOUR CODE HERE
    command =f'php ./derive -g --mnemonic="{mnemonic_p}" --cols=all --coin={coin} --numderive={depth} --format={format}'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {
    ETH: derive_wallets(coin=ETH),
    BTCTEST: derive_wallets(coin=BTCTEST)
}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == 'BTCTEST':
        return bit.PrivateKeyTestnet(priv_key) 
    elif coin == 'ETH':
        return Account.privateKeyToAccount(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, 
             "to": to, 
             "value": amount
            })
        return {"from": account.address, 
                "to": to, 
                "value": amount, 
                "gasPrice": w3.eth.gasPrice, 
                "gas": gasEstimate, 
                "nonce": w3.eth.getTransactionCount(account.address), 
                "chainID": w3.eth.chain_id}
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTCTEST)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(raw_tx)
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    if coin == BTCTEST:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)