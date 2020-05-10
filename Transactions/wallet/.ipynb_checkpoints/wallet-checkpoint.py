# Import BTC, ETH and BTCTEST
from constants import *

# For subprocess
import subprocess
import json
import os, sys

# Define a function to print json output neatly
def pretty_print(response):
    print(json.dumps(response, indent=4, sort_keys=True))
      
# ********************************* 
# DERIVE CRYPTO ADDRESSES AND KEYS
# *********************************    

# Generate mnemonic phrases from https://iancoleman.io/bip39/#english
mnemonic = os.getenv('MNEMONIC', 'type culture spray hip century brisk sing zero upper plastic token young')

def derive_wallets(coin, children=3, mnemonic=mnemonic):
    command =f'./derive -g --mnemonic="{mnemonic}" --coin={coin} --numderive={children} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

# Define coins
coins = {'btc-test': derive_wallets(coin=BTCTEST), 
         'eth': derive_wallets(coin=ETH)}   

# Print out keys
pretty_print(coins)

# Select child account private key by calling the following function
def child_key(coin, index, secret):
    child_account_key = coins[coin][index][secret]
    return child_account_key

# Test print the third key generated
child_key(ETH,2,'privkey')
# Alternatively
child_key('eth',2,'privkey')

# **************************************
# LINK TO TRANSACTION SIGNING LIBRARIES
# **************************************

from web3 import Web3, Account, middleware
from web3.middleware import geth_poa_middleware
# Transaction mined within 60 seconds for fast_gas_strategy
from web3.gas_strategies.time_based import fast_gas_price_strategy
from eth_account import Account

import bit
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

from pathlib import Path
from getpass import getpass

# Create a function to link private key of a child key to bit or web3 for transactions
## The two cryptos return different objects 
### The variable, secret, passes 'privkey' string from a child key
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        account_eth = Account.privateKeyToAccount(priv_key)
        return account_eth
    if coin == BTCTEST:
        account_btctest = PrivateKeyTestnet(priv_key)
        return account_btctest

# Connect localhost to web3
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
    )
        tx_eth = {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.generateGasPrice(),
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainId": w3.net.chainId
    }
        return tx_eth

    if coin == BTCTEST:
        tx_btctest = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
        return tx_btctest
    
def send_tx(coin, account, to, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(raw_tx)
        result = w3.eth.sendRawTransaction(signed.rawTransaction)
        return result
    if coin == BTCTEST:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(raw_tx)
        result = NetworkAPI.broadcast_tx_testnet(signed)
        return result
    
 