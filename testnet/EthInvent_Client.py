# @author ausernamewastaken

import hashlib
import hexbytes
from web3 import Web3


web3_endpoint = 'https://ropsten.infura.io/v3/211f7bc921be4ccdac857047379b3a23'

contract_address = '0x9067fefd6a12ddd3f15fb58448fd701baa9a39ad'


abi = \
    """
    [{"name":"HashSubmitted","inputs":[{"type":"uint256","name":"submissionCount","indexed":false},{"type":"bytes32","name":"hashOfContent","indexed":false}],"anonymous":false,"type":"event"},{"outputs":[],"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"name":"submitHash","outputs":[{"type":"bool","name":""}],"inputs":[{"type":"bytes32","name":"_hashOfContent"}],"stateMutability":"nonpayable","type":"function","gas":74914},{"name":"currentSubmissionCount","outputs":[{"type":"uint256","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1091}]
    """


w3 = Web3(Web3.HTTPProvider(web3_endpoint))
contract = w3.eth.contract(address=contract_address, abi=abi)


def submit_invention(text_description: bytes, wallet: hexbytes.main.HexBytes, gas: int = None) -> bool:
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

    

if __name__ == '__main__':
    import json
    
    keystore_path = "testerwallet.keystore"
    keystore = json.load(open(keystore_path, "r"))
    pw = input("Please Enter Wallet Password: ")
    prvk = (w3.eth.account.decrypt(keystore, pw))
