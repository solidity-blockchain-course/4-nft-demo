from models.Metadata import Metadata
from scripts.helpers import get_formatted_breed, upload_to_ipfs
from brownie import DogCollectable, network
import os
import json
from pathlib import Path


def create_metadata(dog_collectable):
    dog_to_token_uri = {}
    total_created = dog_collectable.tokenIdCounter()
    print(f"{total_created} dog collectables created")

    for token_id in range(total_created):
        breed_int = dog_collectable.tokenIdToBreed(token_id)
        print(f"#{token_id} breed is {breed_int}")

        breed_name_formatted = get_formatted_breed(breed_int)

        # upload image
        local_img_path = f"./img/{breed_name_formatted}.png"
        print(local_img_path)
        ipfs_img_link = upload_to_ipfs(local_img_path)
        print(f"img link: {ipfs_img_link}")

        # create metadata
        # ./metadata/{network}/name

        new_metadata_folder = f"./metadata/{network.show_active()}"
        new_metadata_filename = f"{breed_int}-{breed_name_formatted}.json"
        metadata_full_path = os.path.join(new_metadata_folder, new_metadata_filename)
        if Path(metadata_full_path).exists():
            print(f"{metadata_full_path} file already exists, remove to override !")
        else:
            metadata = Metadata(
                breed_name_formatted,
                f"Collectible of breed {breed_name_formatted}",
                ipfs_img_link,
                [{"height": 100}, {"color": "gray"}],
            )
            if not os.path.exists(new_metadata_folder):
                os.makedirs(new_metadata_folder)

            with open(metadata_full_path, "w") as f:
                json.dump(metadata.__dict__, f)

        metadata_ipfs_link = upload_to_ipfs(metadata_full_path)
        print(f"metadata ipfs: {metadata_ipfs_link}")
        dog_to_token_uri[breed_name_formatted] = metadata_ipfs_link

    return dog_to_token_uri


def main():
    dog_collectable = DogCollectable[-1]
    mapping = create_metadata(dog_collectable)
    print(mapping)
