from scripts.helpers import fund_with_link, get_account
from brownie import DogCollectable


def create_collectable():
    account = get_account()
    collectable = DogCollectable[-1]

    fund_with_link(account, collectable.address)
    create_tx = collectable.createCollectible({"from": account})
    create_tx.wait(1)

    print("Collectable created !")


def main():
    create_collectable()
