# Could Python Take Care of Coins in Your Crypto Wallet?

## _**How to talk to a computer terminal, asking python to sent different crypto coins in our wallet?**_

### **Wallet**

A crypto wallet is created using python in the file:
[wallet.py](Transactions/wallet/wallet.py)
and
[Jupyter notebook version of wallet.py](Transactions/wallet/wallet.ipynb).

To run wallet.py:
* Open a terminal window on the wallet folder
```
code .
```
* Access functions in wallet.py interactively, run on the terminal window:
```
from wallet import * 
```

However, it is in trouble-shooting stage. A bitcoin transaction is generated via this 
["get_balance"](Transactions/wallet/get_balance.ipynb) notebook file.

Screenshots of the transaction confirmation is provided here:

<details><summary>
BTCTEST transaction
</summary>

![BTCTEST Transaction](Transactions/images/btc_tx.png)

</details>

_**BTCTEST transaction confirmation**_

![BTCTEST Transaction Confirmation](Transactions/images/btc_tx_confirm.png)


<details><summary>
BTCTEST transaction on testnet3
</summary>

![BTCTEST testnet3](Transactions/images/testnet3.png)

</details>

For crypto transaction on localhost
_**http://127.0.0.1:8545**_


_**Ethereum transaction confirmation**_

Mining is initiated on ethereum proof-of-authority testnet called `txs`. It is placed under zbank node in MyCrypto Wallet. Please see details below.

<details><summay>
Mining
</summary>

![Mining](Transactions/images/mining.png)

</details>

<details><summay>

View in MyCrypto Wallet 

</summary>

![MyCrypto](Transactions/images/mycrypto.png)

</details>

### **Wallet Folder Structure**

_**In Mac Terminal**_

* Create a wallet  by `mkdir wallet`
* `touch wallet.py` to generate a python file for crypto transaction functions
* Install `hd-wallet-derive` by typing
```
ln -s hd-wallet-derive/hd-wallet-derive.php
```
<details><summary>
Create files in wallet folder
</summary>

![Wallet Structure](Transactions/images/terminal.png)

</details>

* Set up environment requirements in a file by
```
touch requirements.txt
```
<details><summary>
Nano environment
</summary>

![requirements](Transactions/images/requirements.png)

</details>

* Set up constants.py file for `BTCTEST`, `ETH` and `BTC` by typing
```
nano constants.py
```
<details><summary>
Nano environment
</summary>

![requirements](Transactions/images/constants.png)

</details>

---
### _**Further exploration should there be more time**_

- Add support for `BTC`.

- Add support for `LTC` using the sister library, [`lit`](https://github.com/blockterms/lit).

- Add a function to track transaction status by `txid`.
---

# Files

[Wallet](wallet)

[Images](images)

# References

* CU Gitlab Repository
* https://web3py.readthedocs.io/en/latest/overview.html#Web3.toHex
* https://web3py.readthedocs.io/en/latest/web3.eth.account.html#web3.account.Account.signTransaction
* https://live.blockcypher.com/btc-testnet
* https://github.com/blockterms/lit
* https://coinfaucet.eu/en/btc-testnet/
* https://iancoleman.io/bip39/#english
* https://tbtc.bitaps.com