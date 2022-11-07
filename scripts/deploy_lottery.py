from brownie import Lottery, config, network
from scripts.essential_scripts import get_account, get_contract, fund_with_link
import time

# Deploy the lottery contract
def deploy_lottery():
    account = get_account()  # Get an account
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed Lottery!")
    return lottery


# Start the lottery
def start_lottery():
    account = get_account()  # Get an account
    lottery = Lottery[-1]  # Get the most recent deployment
    starting_tx = lottery.startLottery({"from": account})  # Start the lottery
    starting_tx.wait(1)
    print("\nLottery Started!")


# Enter the lottery
def enter_lottery():
    account = get_account()  # Get an account
    lottery = Lottery[-1]  # Get the most recent deployment
    # Get the entrance fee plus something small to be sure
    value = lottery.getEntranceFee() + 100000000
    enter_tx = lottery.enter({"from": account, "value": value})  # Enter the lottery
    enter_tx.wait(1)
    print("\nEntered Lottery Successfully!")


# End the lottery
def end_lottery():
    account = get_account()  # Get an account
    lottery = Lottery[-1]  # Get the most recent deployment
    tx = fund_with_link(lottery.address)  # Fund the contract to get a random number
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})  # End the lottery
    ending_tx.wait(1)
    time.sleep(60)  # Sleep 1 min to make sure we got a response from fulfillRandomness
    print(f"\n{lottery.recentWinner()} is the winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
