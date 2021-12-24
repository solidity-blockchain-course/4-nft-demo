from scripts.helpers import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
)
from brownie import DogCollectable, network, config


def deploy_and_create():
    print(f"active network: {network.show_active()}")
    account = get_account()
    key_hash = config["networks"][network.show_active()]["key_hash"]
    fee = config["networks"][network.show_active()]["fee"]

    dog_collectable = DogCollectable.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        key_hash,
        fee,
        {"from": account},
        publish_source=(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS),
    )
    print(f"DogCollectable deployed at: {dog_collectable.address}")

    fund_with_link(account, dog_collectable.address)

    tx_create = dog_collectable.createCollectible({"from": account})
    tx_create.wait(1)

    print("creation requested !")

    return dog_collectable, tx_create


def main():
    deploy_and_create()
