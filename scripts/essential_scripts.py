from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
    interface,
)

FORKED_LOCAL_ENVIRONMENTS = [
    "mainnet-fork",
    "mainnet-fork-development",
    "mainnet-fork-dev",
]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["ganache-local", "development"]

DECIMALS = 8
STARTING_PRICE = 200000000000

# If 1: Return an account we chose from brownie accounts
# If 2: Return a personal account from the brownie accounts list
# If 3: Return a brownie account
# General: Return a personal account from the .env file
def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


# Map eth_usd_price_feed to a Mock
# Map vrf_coordinator to a Mock
# Map link_token to a Mock
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


# This function will grab the contract addresses from
# the brownie config if defined, otherwise it will deploy
# a mock version of that contract and return it.
#    Args:
#        contract_name (string): The refered name in the config.
#    Returns:
#        brownie.network.contract.ProjectContract: The most
#        recently deployed version of this contract.
def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()  # If the contract_type does not already have a mock create one
        contract = contract_type[-1]  # Get the latest created mock
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


# Deploy a mock
def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    account = get_account()
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mocks Deployed!")


# contract_address: Who are we gonna fund with link
# account: An account (We set a default as none)
# link_token: A link_token (We set a default as none)
# amount: Default amount = 0.1 Link
def fund_with_link(contract_address, account=None, link_token=None, amount=10**17):
    # If you pass an account use it else call get_account
    account = account if account else get_account()
    # Same for the token
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # These 2 lines do the same as the on above with the use of an interface, so we
    # don't need to compile down to the abi ourselves. Brownie does that for us.
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract Funded with link token!")
    return tx
