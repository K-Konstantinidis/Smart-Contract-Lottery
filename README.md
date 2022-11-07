# Smart Contract Lottery

## Purpose
Create a **100% random** smart contract lottery in a python environment.

## Lottery.sol
- The contract owner will choose when the lottery starts
- Users can enter the lottery with ETH based on a USD fee (10$)
- The contract owner will choose when the lottery is over
- The lottery will select a truly random winner

## Development Environment
[Contracts for our mocks!](https://github.com/K-Konstantinidis/Smart-Contract-Lottery/tree/master/contracts/test)

## Deploy_lottery.py
A python script to:

- Connect to a Blockchain `(Testnet, Mainnet)`
- Get an account safely
  - From a local or a forked local blockchain environment
  - A real one via the config & .env file
- Pass the `price feed`, `vrf coordinator`, `link_token` & `keyhash` addresses plus the `fee` to our contract
  - Real ones if we are on a real network
  - Mock ones if we are on a local blockchain environment
- Deploy our contract
- Start the lottery (Only the contract owner)
- Enter the lottery (with our account)
- End the lottery (Only the contract owner)
  - Fund the contract to get a random number
  - End the lottery
  - Sleep for a minute to make sure there was a response from fulfillRandomness
  - Show the winner

## Essential_scripts.py
- Get an account safely
  - From a local or a forked local blockchain environment
  - A real one via the config & .env file
- Get contract addresses. Either mock ones or real ones
- Deploy mocks
- Fund the contract with link (To use the fulfillRandomness method)

## Tests
#### There are 2 types of tests in this project.
#### - unit tests, which run on a local blockchain.
#### - integration tests, which run on a testnet

### Unit
- Test to make sure the entrance fee is okay
- Test to make sure the lottery is open if we try to enter
- Test to make sure we can start and enter the lottery
- Test to make sure we can end the lottery
- Test to make sure the winner was chosen randomly and got all the money

### Integration 
- Make sure the whole program works fine

## Help with the project
To run the code there are some requirements. You must install: 

### pipx 
Install _pipx_ by running the following on the command line: `python -m pip install --user pipx` then `python3 -m pipx ensurepath`

For more information check: <a href="https://pypa.github.io/pipx/">Install pipx</a>

### Brownie
Install _Brownie_ by running the following on the command line: `pip install eth-brownie`

For more information check: <a href="https://pypi.org/project/eth-brownie/">Install Brownie</a>

This is the Lesson 7 of the <a href="https://www.youtube.com/c/Freecodecamp">freeCodeCamp.org</a> tutorial: https://www.youtube.com/watch?v=M576WGiDBdQ with more comments.

