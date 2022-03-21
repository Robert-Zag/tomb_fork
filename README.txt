Tomb deployer wallet history, first transactions of the tomb finance deployer wallet
These transactions don't seem to include erc 20s, need to fetch aggregate transactions
https://ftmscan.com/txs?a=0x12164b332d01cc694e752d7039ee21d56fe7705d

1. Received 1000FTM
2. Deployed unknown "Set Completed" contract
3. Called Set Completed
4. Deployed Tomb.sol
5. Deployed TShare.sol
    args (start time = unix timestamp for when vesting starts, community fund = UNKNOWN WALLET, dev fund = UNKNOWN WALLET)
    operator = treasury
    owner = UNKNOWN WALLET
6. Deployed TBond.sol
7. Called Set Completed
8. Deployed TombGenesisRewardPool.sol
    args (tomb address, shiba address, pool start time)
9. Called Set Completed
10. Deployed TombRewardPool.sol --OLD--
11. Called Set Completed
12. Called Distribute Reward on Tomb Token
    args: (genesis pool, tomb pool, airdrop wallet)
13. Called Set Completed
14. Deployed TShareRewardPool
15. Called Distribute Reward on TShare
    args: (farming incentive fund)
16. Called Set Completed
17. Approve wFTM
18. Approve TOMB
19. Approve wFTM
20. Approve TOMB
21. "Add Liquidity ETH" to SpookySwap Router TOMB - this is the deployment transaction for the LP pairs
22. Approve TSHARE
23. "Add Liquidity ETH" to SpookySwap Router TSHARE
24.
.
27. Called Add on Genesis Reward Pool x4
28. Called Add on --OLD-- Tomb Reward Pool
29. Called Add on TSHARE Rewards Pool
30. Called Add on TSHARE Rewards Pool 2nd time
31. Deployed Oracle.Sol
32. Called Set Tomb Oracle on Tomb Token
33. Called Set Completed
34. Deployed Treasury --UNKNOWN INSTANCE--
35. Deployed Masonry --UNKNOWN INSTANCE--
36. Called Initialize on 35.
37. Called Initialize on 34.
38. Called Set Extra Funds on 34.
39. Called Set Completed
40. Deployed Tax Office
41. Called Set Tax Office on Tomb Token
42. Called Set Completed
Called Exclude Address on Tomb Token x12
43. args TSHARE Token Address
44. args TBOND Token Address
45. args Genesis Reward Pool Address
46. args --OLD-- Tomb Reward Pool
47. args TSHARE Reward Pool
48. args Oracle
49. args Masonry --UNKNOWN INSTANCE--
50. args Treasury --UNKNOWN INSTANCE--
51. args DAO wallet
52. args DEV wallet
53. args SpookySwap Router Address
54. args SpookySwap Factory Address