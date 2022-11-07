from brownie import network
import pytest
from scripts.deploy_lottery import deploy_lottery
import time
from scripts.essential_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
)


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account, "value": lottery.getEntraceFee()})
    lottery.enter({"from": account, "value": lottery.getEntraceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(60)  # Sleep to get response from fulfillRandomness
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
