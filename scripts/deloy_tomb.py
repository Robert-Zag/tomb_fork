# 2 more contracts that are involved in tomb finance are, solidity for this contract is not available
# TOMB-WFTM LP: 0x2A651563C9d3Af67aE0388a5c8F89b867038089e
# Link: https://ftmscan.com/address/0x2A651563C9d3Af67aE0388a5c8F89b867038089e
# TSHARE-WFTM LP: 0x4733bc45eF91cF7CcEcaeeDb794727075fB209F2
# Link: https://ftmscan.com/address/0x4733bc45eF91cF7CcEcaeeDb794727075fB209F2
# spooky swap is just a fork of uniswap v2
from brownie import (
    network,
    Tomb,
    TaxOffice,
    TBond,
    TShare,
    TombGenesisRewardPool,
    TombRewardPool,
    TShareRewardPool,
    Oracle,
    Masonry,
    Treasury,
    interface,
    accounts,
    network,
    config,
)
import time
from datetime import datetime, timedelta
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet_fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# THIS NEEDS TO BE INCORPORATED IN THE GET ACCOUNT FUNCTION, IT WILL NOT WORK ON LOCAL AND FORKED NETWORKS
# KNOWN WALLETS: deployer, dao_wallet, dev_wallet, airdrop_wallet
# community_fund, dev_fund (arguments for TShare), tax collector address (argument for Tomb contract)
# farming_incentive_fund (argument for TShares distribute rewared function)

# argument for TombGenesisRewardPool.sol constructor method
shiba_fantom_token_address = "0x9Ba3e4F84a34DF4e08C112e1a0FF148b81655615"

# these are some of my extra addresses that will be used as protocol wallets
address2 = "0xB30323944F23e1a7DB4b4E5e6e29CC5A4F8f8d4A"
address3 = "0x5457195c8614460D03e0df36B6C4eBEAc759C36C"
address4 = "0x3c70d082e2ffB60573fF0e264fc34F7E1e910e87"
address5 = "0xb1f7881F0cD6B892fFeAb479EDCcd6F3b5D89B80"
address6 = "0x9C741ef0619A0eF5d5F86988e6Ad31CD5D4cE75c"
my_other_wallets = [address2, address3, address4, address5, address6]

string_to_contract = {}
string_to_contract["tomb"] = Tomb
string_to_contract["tshare"] = TShare
string_to_contract["tbond"] = TBond
string_to_contract["genesis_reward_pool"] = TombGenesisRewardPool
string_to_contract["tomb_reward_pool"] = TombRewardPool
string_to_contract["tshare_reward_pool"] = TShareRewardPool
string_to_contract["tax_office"] = TaxOffice
string_to_contract["oracle"] = Oracle
string_to_contract["masonry"] = Masonry
string_to_contract["treasury"] = Treasury

called_distribute_rewards_tomb = True
called_distribute_rewards_tshare = True

has_approved_tomb = True
has_approved_tshare = True

has_approved_weth = True
has_approved_weth_2 = True

added_tomb_liquidity = True
added_tshare_liquidity = True

WETH_AMOUNT = 0.2
MINIMUM_WETH_BALANCE = Web3.toWei(0.2, "ether")


def get_weth():
    acct = accounts.add(
        config["wallets"]["from_key"]
    )  # add your keystore ID as an argument to this call
    weth = interface.WethInterface(
        config["networks"][network.show_active()]["weth"])
    tx = weth.deposit(
        {"from": acct, "value": Web3.toWei(WETH_AMOUNT, "ether")})
    print(f"Received {WETH_AMOUNT} WETH")
    return tx


def get_account(index=None):
    if network.show_active() in (
        LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[index]
    if index == 0:
        return accounts.add(config["wallets"]["from_key"])
    else:
        return my_other_wallets[index - 1]


def get_contract(contract_str, *args):
    contract = string_to_contract[contract_str]
    if len(contract) >= 1:
        print(
            f"-- {contract_str} has been deployed previously at: {contract[-1].address}")
        return contract[-1]
    return contract.deploy(*args)


def deploy_contracts():
    # deployer account used to deploy all the contracts
    account = get_account(index=0)
    # setting the tax rate to 50% and the tax collector address to current address
    tomb_contract = get_contract(
        "tomb", 5000, get_account(index=1), {"from": account})
    print("### - Tomb contract has been deployed successfully!\n")

    # a timestamp 12hours from now, used in smart contract constructors
    start_time = int(datetime.timestamp(datetime.now() + timedelta(hours=12)))

    tshare_contract = get_contract(
        "tshare",
        start_time,
        get_account(index=2),
        get_account(index=3),
        {"from": account},
    )
    print("### - TShare contract has been deployed successfully!\n")

    tbond_contract = get_contract("tbond", {"from": account})
    print("### - TBond contract has been deployed successfully!\n")

    genesis_reward_pool_contract = get_contract(
        "genesis_reward_pool",
        tomb_contract.address,
        shiba_fantom_token_address,
        start_time,
        {"from": account},
    )
    print("### - Genenesis reward pool contract has been deployed successfully!\n")

    tomb_reward_pool_contract = get_contract(
        "tomb_reward_pool", tomb_contract.address, start_time, {
            "from": account}
    )
    print("### - Tomb reward pool contract has been deployed successfully!\n")

    # It has to be set manually that this function has been called already
    if not called_distribute_rewards_tomb or not network.show_active() == "rinkeby":
        tx = tomb_contract.distributeReward(
            genesis_reward_pool_contract.address,
            tomb_reward_pool_contract.address,
            get_account(index=4),
            {"from": account},
        )
        # must wait after the last smart contract, function call
        tx.wait(1)
        print("### - Called distribute rewards on Tomb\n")
    else:
        print("Omitting Tomb distribute rewards as it has been done previously")

    tshare_reward_pool_contract = get_contract(
        "tshare_reward_pool", tshare_contract.address, start_time, {
            "from": account}
    )
    print("### - TShare reward pool contract has been deployed successfully!\n")

    # It has to be set manually that this function has been called already
    if not called_distribute_rewards_tshare or not network.show_active() == "rinkeby":
        tx = tshare_contract.distributeReward(
            get_account(index=5), {"from": account})
        tx.wait(1)
        print("### - Called distribute rewards on TShare\n")
    else:
        print("Omitting TShare distribute rewards as it has been done previously")

    uniswap_router_address = config["networks"][network.show_active(
    )]["uniswap_router"]
    uniswap_router = interface.IUniswapV2Router02(uniswap_router_address)

    # will add TOMB token liquidity to UniswapV2Router02
    # after tomb token will be approved with Router as spender
    # amount 1 was 99999000000000000000000
    # for second approval the amount was 99999000000000000000000
    # there were also 2 WFTM approvals inbetween the 2 tomb approvals
    # both had the same spender and amount as the tomb token approvals
    if not has_approved_tomb or not network.show_active() == "rinkeby":
        amount = 99999000000000000000000
        tx = tomb_contract.approve(
            uniswap_router.address, amount, {"from": account})
        tx.wait(1)
        print("Succesfully approved Tomb to uniswap router---\n")
    else:
        print("Omitting Tomb token approval as it has been done previously")

    amount_token_desired = 10000000000000000
    print(
        f'Amount Token Desired {Web3.fromWei(amount_token_desired, "ether")}')
    amount_token_min = 10000000000000000
    print(f'Amount Token Min {Web3.fromWei(amount_token_min, "ether")}')
    amount_eth_min = 100000000000000000
    print(f'Amount Eth Min {Web3.fromWei(amount_eth_min, "ether")}')
    # Amount Token Desired 0.01
    # Amount Token Min 0.01
    # Amount Eth Min 0.1

    print(
        f"The balance of the deployer wallet is {Web3.fromWei(account.balance(), 'ether')}")

    # if WETH balance is less than 0.2, will get 0.2 weth
    weth = interface.WethInterface(
        config["networks"][network.show_active()]["weth"])
    weth_balance = weth.balanceOf(account.address)
    print(
        f"Current wETH balance {Web3.fromWei(weth_balance, 'ether')}wETH"
    )
    if weth_balance < MINIMUM_WETH_BALANCE:
        print("Getting wETH")
        get_weth()
        print(
            f"Now the contract has {Web3.fromWei(weth.balanceOf(account.address), 'ether')}wETH"
        )

    if not has_approved_weth or not network.show_active() == "rinkeby":
        amount = 99999000000000000000000
        tx = tomb_contract.approve(
            uniswap_router.address, amount, {"from": account})
        tx.wait(1)
        print("Succesfully approved wETH to uniswap router---\n")
    else:
        print("Omitting wETH token approval as it has been done previously")

    if not has_approved_weth_2 or not network.show_active() == "rinkeby":
        amount = 99999000000000000000000
        print(f'Approval amount is {Web3.fromWei(amount, "ether")}')
        tx = tomb_contract.approve(
            uniswap_router.address, amount, {"from": account})
        tx.wait(1)
        print("Succesfully approved wETH to uniswap router---\n")
    else:
        print("Omitting wETH token approval as it has been done previously")

    # deadline has been 20 minutes into the future
    deadline = int(datetime.timestamp(datetime.now() + timedelta(minutes=20)))

    # adding liquidity to tomb
    if not added_tomb_liquidity or not network.show_active() == "rinkeby":
        # THIS FUNCTION CALL HAS BEEN PAYABLE WITH 0.1 FTM
        tx = uniswap_router.addLiquidityETH(
            tomb_contract.address,
            amount_token_desired,
            amount_token_min,
            amount_eth_min,
            account,
            deadline,
            {"from": account, "value": Web3.toWei(0.1, 'ether')},
        )
        tx.wait(1)
        print("Successfully added liquidity to Tomb pool")
    else:
        print("Omitting adding liquidity to Tomb token pool")

    # adding TSHARE token liquidity
    # for non address contracts using exact arguments
    # first it is needed to approve the tokens with the router address as the spender
    # however the amount for the argument for this function call was seemingly arbitrarily large
    if not has_approved_tshare or not network.show_active() == "rinkeby":
        arbitrarily_large_number = 115792089237316195423570985008687907853269984665640564039457584007913129639935
        tx = tshare_contract.approve(
            uniswap_router.address, arbitrarily_large_number, {"from": account}
        )
        tx.wait(1)
        print("Succesfully approved TShare---\n")
    else:
        print("Omitting TShare approval as it has been done previously")

    amount_token_desired = 10000000000000000
    amount_token_min = 10000000000000000
    amount_eth_min = 200000000000000000

    if not added_tshare_liquidity or not network.show_active() == "rinkeby":
        tx = uniswap_router.addLiquidityETH(
            tshare_contract.address,
            amount_token_desired,
            amount_token_min,
            amount_eth_min,
            account,
            deadline,
            {"from": account, "value": Web3.toWei(0.1, 'ether')},
        )
        tx.wait(1)
        print("Successfully added liquidity to Tshare pool")
    else:
        print("Omitting adding liquidity to Tshare token pool")


def main():
    deploy_contracts()
