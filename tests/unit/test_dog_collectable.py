import pytest
from brownie import config, network
from scripts.deploy_and_create import deploy_and_create
from scripts.helpers import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract


def test_should_create_collectable():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for unit testing")

    dog_collectable, creation_tx = deploy_and_create()

    request_id = creation_tx.events["creationRequested"]["requestId"]
    random_number = 443
    vrf_coord_mock = get_contract("vrf_coordinator")
    vrf_coord_mock.callBackWithRandomness(
        request_id, random_number, dog_collectable.address, {"from": get_account()}
    )

    assert dog_collectable.tokenIdCounter() == 1
    assert dog_collectable.tokenIdToBreed(0) == random_number % 3
