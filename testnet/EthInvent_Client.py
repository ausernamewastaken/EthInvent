# @author ausernamewastaken

import hashlib
from hexbytes.main import HexBytes
from web3 import Web3


web3_endpoint = 'https://ropsten.infura.io/v3/211f7bc921be4ccdac857047379b3a23'

contract_address = '0xFcc69d39377E2190Fe72FBc84FE234cfB783Ae46'


abi = \
    """
    [{"name": "HashSubmitted", "inputs": [{"type": "bytes32", "name": "hashOfContent", "indexed": false}], "anonymous": false, "type": "event"}, {"name": "submitHash", "outputs": [{"type": "bool", "name": ""}], "inputs": [{"type": "bytes32", "name": "_hashOfContent"}], "stateMutability": "nonpayable", "type": "function", "gas": 37744}, {"name": "submissions", "outputs": [{"type": "bytes32", "name": ""}], "inputs": [{"type": "bytes32", "name": "arg0"}], "stateMutability": "view", "type": "function", "gas": 1206}]
    """


w3 = Web3(Web3.HTTPProvider(web3_endpoint))
contract = w3.eth.contract(address=contract_address, abi=abi)


def submit_invention(text_description: bytes, wallet: HexBytes, gas: int = None) -> HexBytes:
    """
    Submits an invention by writing its SHA3_256 hash to the blockchain
    """
    
    account_nonce = w3.eth.getTransactionCount(w3.eth.account.privateKeyToAccount(wallet).address)
    
    _hashOfContent = hashlib.sha3_256(text_description).digest()

    fn_call = contract.functions.submitHash(_hashOfContent)

    gas = int(fn_call.estimateGas() * 1.2) if (gas == None) else gas
    print(f"Gas used: {gas}")

    tx = fn_call.buildTransaction({'nonce': account_nonce, 'gas': gas})

    signed_tx = w3.eth.account.signTransaction(tx, private_key=wallet)

    txhash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    print(f"Hash {_hashOfContent} submitted at txhash {txhash}")
    
    return txhash

    
def verify_proof(text_description: bytes, return_timestamp: bool = False) -> (bool or int):
    """
    Verifies a proof by checking its SHA3_256 hash aginst the record on blockchain
    
    Returns:
        True if the proof is sucessfully verified and return_timestamp is False;
        The timestamp at which the hash was written onto the blockchain if the proof is sucessfully verified
        and return_timestamp is True;
    """

    _hashOfContent = hashlib.sha3_256(text_description).digest()
    
    recorded_timestamp = contract.functions.submissions(_hashOfContent).call()

    return recorded_timestamp if return_timestamp else (recorded_timestamp == 0)

    
    
if __name__ == '__main__':
    import json
    
    keystore_path = "testerwallet.keystore"
    keystore = json.load(open(keystore_path, "r"))
    pw = input("Please Enter Wallet Password: ")
    prvk = (w3.eth.account.decrypt(keystore, pw))
