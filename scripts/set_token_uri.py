from models.Metadata import Metadata
from scripts.create_metadata import create_metadata
from scripts.helpers import (
    get_account,
    get_formatted_breed,
)
from brownie import DogCollectable


def set_token_uri(dog_collectable, dog_to_token_uri):
    token_count = dog_collectable.tokenIdCounter()
    for token_id in range(token_count):
        current_token_uri = dog_collectable.tokenURI(token_id).strip()
        if current_token_uri != "":
            print(f"token uri already set to /{current_token_uri}/. Skipping ...")
            continue

        breed_int = dog_collectable.tokenIdToBreed(token_id)
        breed_name = get_formatted_breed(breed_int)
        token_uri = dog_to_token_uri[breed_name]
        token_uri_create_tx = dog_collectable.setTokenUri(
            token_id, token_uri, {"from": get_account()}
        )
        token_uri_create_tx.wait(1)
        print(f"Token uri set for {token_id}")


def main():
    dog_collectable = DogCollectable[-1]
    dog_to_token_uri_mapping = create_metadata(dog_collectable)
    set_token_uri(dog_collectable, dog_to_token_uri_mapping)
