// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract DogCollectable is ERC721, VRFConsumerBase {
    uint256 public tokenIdCounter;
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    bytes32 internal keyHash;
    uint256 internal fee;

    uint256 public randomness;
    mapping(bytes32 => address) public requestIdToUser;
    mapping(uint256 => address) public tokenToOwner;
    mapping(uint256 => Breed) public tokenIdToBreed;

    event creationRequested(address indexed userId, bytes32 requestId);
    event requestFulfilled(address owner, uint256 indexed tokenId);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        ERC721("Doggie", "DOG")
        VRFConsumerBase(_vrfCoordinator, _linkToken)
    {
        tokenIdCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public {
        require(
            LINK.balanceOf(address(this)) >= fee,
            "Not enough LINK - fill contract with faucet"
        );
        bytes32 requestId = requestRandomness(keyHash, fee);

        requestIdToUser[requestId] = msg.sender;
        emit creationRequested(msg.sender, requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        randomness = _randomness;
        address owner = requestIdToUser[_requestId];

        Breed breed = Breed(_randomness % 3);
        tokenIdToBreed[tokenIdCounter] = breed;
        emit breedAssigned(tokenIdCounter, breed);

        _safeMint(owner, tokenIdCounter);
        tokenToOwner[tokenIdCounter] = owner;
        tokenIdCounter += 1;
        emit requestFulfilled(owner, tokenIdCounter);
    }

    function setTokenUri(uint256 _tokenId, string memory _tokenUri) public {
        require(_isApprovedOrOwner(msg.sender, _tokenId));
        _setTokenURI(_tokenId, _tokenUri);
    }
}
