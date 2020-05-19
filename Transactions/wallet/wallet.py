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
#from web3.gas_strategies.time_based import medium_gas_price_strategy
from eth_account import Account

import bit
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

from pathlib import Path
from getpass import getpass

# set w3 connection
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# set gas price strategy to built-in "medium" algorithm (est ~5min per tx)
# see https://web3py.readthedocs.io/en/stable/gas_price.html?highlight=gas
# see https://ethgasstation.info/ API for a more accurate strategy
w3.eth.setGasPriceStrategy(fast_gas_price_strategy)

# Create a function to link private key of a child key to bit or web3 for transactions
## The two cryptos return different objects 
### The variable, secret, passes 'privkey' string from a child key
def priv_key_to_account(coin, priv_key):
#    print(coin)
#    print(priv_key)
    if coin == ETH:
        account = Account.privateKeyToAccount(priv_key)
        return account
    if coin == BTCTEST:
        account = PrivateKeyTestnet(priv_key)
        return account

# Define the first bitcoin testnet account
btc_0 = priv_key_to_account(BTCTEST, child_key('btc-test',0,'privkey'))
btc0 = {'btc_0': btc_0, 'btc_0.address': btc_0.address}
print(btc0)

# Define the second bitcoin testnet account
btc_1 = priv_key_to_account(BTCTEST, child_key('btc-test',1,'privkey'))
btc1 = {'btc_1': btc_1, 'btc_1.address': btc_1.address}
print(btc1)

# Define the first ethereum account
eth_0 = priv_key_to_account(ETH, child_key('eth',0,'privkey'))
eth0 = {'eth_0': eth_0, 'eth_0.address': eth_0.address}
print(eth0)

# Define the second ethereum account
eth_1 = priv_key_to_account(ETH, child_key('eth',1,'privkey'))
eth1 = {'eth_1': eth_1, 'eth_1.address': eth_1.address}
print(eth1)

# *************************************
# GENERATE TRANSACTIONS VIA FUNCTIONS!
# *************************************

# Connect localhost to web3
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
    )
        tx = {
            "from": account.address,
            "to": to,
            "value": amount,
            "gasPrice": w3.eth.generateGasPrice(),
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainId": w3.net.chainId
    }
        return tx

    if coin == BTCTEST:
        tx = PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
        return tx

# Initiate a transaction of 0.0001 satoshi on bitcoin testnet
create_tx(BTCTEST, btc_0, btc_1.address, 0.0001)
    
def send_tx(coin, account, to, amount):
    if coin == ETH:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.signTransaction(raw_tx)
        result = w3.eth.sendRawTransaction(signed.rawTransaction)
        print(signed)
        return result
    
    if coin == BTCTEST:
        raw_tx = create_tx(coin, account, to, amount)
        signed = account.sign_transaction(raw_tx)
        result = NetworkAPI.broadcast_tx_testnet(signed)
        print(signed)
        return result

# Send a transaction of 0.0001 satoshi on bitcoin testnet 
send_tx(BTCTEST, btc_0, btc_1.address, 0.0001)
