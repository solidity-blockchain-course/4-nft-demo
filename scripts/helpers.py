from brownie import network, accounts, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3
import requests
from pathlib import Path

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache", "mainnet-fork"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print("Deploying mocks ...")
        if len(contract_type) == 0:
            deploy_mocks()
        return contract_type[-1]
    else:
        print(f"No mocks needed. Fetching {contract_type._name} ...")
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        return contract


def deploy_mocks(account=None):
    account = account if account else get_account()
    print("Deploying LINK contract ...")
    link_token = LinkToken.deploy({"from": account})
    print(f"LINK deployed at {link_token.address}!")

    print("Deploying VRFCoordinatorMock ...")
    vrf_coord_mock = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinatorMock deployed at {vrf_coord_mock.address}!")


def fund_with_link(sender, recipient_address, amount=Web3.toWei(0.1, "ether")):
    link = get_contract("link_token")

    transfer_tx = link.transfer(recipient_address, amount, {"from": sender})
    transfer_tx.wait(1)
    print(f"{Web3.fromWei(amount, 'ether')} LINK transfered to {recipient_address}")


breeds = ["PUG", "SHIBA_INU", "ST_BERNARD"]


def get_formatted_breed(index):
    return breeds[index].replace("_", "-").lower().strip()


def upload_to_ipfs(path):
    url = "http://127.0.0.1:5001/api/v0/add"
    with open(path, "rb") as binary_file:
        files = {"file": binary_file.read()}
        response = requests.post(url, files=files)
        response.raise_for_status()
        response_data = response.json()
        print(response_data)
        file_hash = response_data["Hash"]
        img_ipfs_url = f"https://ipfs.io/ipfs/{file_hash}"
        print(f"Newply uploaded file here: {img_ipfs_url}")
        return img_ipfs_url
