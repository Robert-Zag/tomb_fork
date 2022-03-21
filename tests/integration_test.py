# unit tests are not needed since we're forking a working protocol
from brownie import network
from scripts.deloy_tomb import (
    deploy_contracts,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
)
import pytest


def test_can_deploy_protocol():
    # integration test must be carried out on a testnets
    if network.show_active in (
        LOCAL_BLOCKCHAIN_ENVIRONMENTS + FORKED_LOCAL_ENVIRONMENTS
    ):
        pytest.skip()
    # arrange
    # act
    deploy_contracts()
    # assert
