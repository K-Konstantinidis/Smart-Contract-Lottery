// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players; // Lotery players
    uint256 public usdEntryFee; // Fee to enter the lottery
    AggregatorV3Interface internal ethUsdPriceFeed; // ETH->USD price feed
    address payable public recentWinner; // Last winner of the lottery
    uint256 public randomness; // Last random number

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state; // Current lottery state
    uint256 public fee; // Associated with the link token needed to pay for the randomness request
    bytes32 public keyHash; // Uniquely identify the chain link VRF node

    event RequestedRandomness(bytes32 requestID);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _linkToken,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _linkToken) {
        usdEntryFee = 10 * (10**18); // 10$ minimum fee
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED; // Start with closed lottery
        fee = _fee;
        keyHash = _keyHash;
    }

    // Enter the lottery
    function enter() public payable {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery is not open. You cannot enter!"
        );
        // 10$ minimum
        require(
            msg.value >= getEntranceFee(),
            "You need more ETH to enter the lottery!"
        );
        players.push(payable(msg.sender));
    }

    // Get the entrance fee from the player
    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData(); // Price is in gwei
        uint256 fixedPrice = uint256(price) * 10**10; // Make price in wei
        return (usdEntryFee * 10**18) / fixedPrice;
    }

    // Start the lottery
    // Only if the owner says so
    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    // End the lottery
    // Only if the owner says so
    function endLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.OPEN, "Can't end the lottery");
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;

        // * Don't do this *
        // uint256(
        //     keccack256(
        //         abi.encodePacked(
        //             nonce, // nonce is preditable (aka, transaction number)
        //             msg.sender, // msg.sender is predictable
        //             block.difficulty, // can actually be manipulated by the miners!
        //             block.timestamp // timestamp is predictable
        //         )
        //     )
        // ) % players.length;

        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId); // Emit the event
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Can't calculate winner"
        );
        require(_randomness > 0, "random-not-found"); // Make sure we got a random number
        recentWinner = players[(_randomness % players.length)]; // Get a winner
        recentWinner.transfer(address(this).balance); // Give them the money
        players = new address payable[](0); // Reset players array
        lottery_state = LOTTERY_STATE.CLOSED; // Close the lottery
        randomness = _randomness; // Keep the last random number
    }
}
