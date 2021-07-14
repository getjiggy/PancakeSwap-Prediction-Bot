from brownie import *

import time
import os
from brownie.network.gas.strategies import LinearScalingStrategy

pkey = os.getenv('privateKey')
prediction = Contract.from_explorer('0x516ffd7D1e0Ca40b1879935B2De87cb20Fc1124b')

accounts.add(pkey)
accounts.load()
# this project has several flaws. to my knowledge it is impossible to guarentee that the odds that trigger the bot to place
# a bet will still be present once the bets are are locked. This is because other bots/traders can change the odders by
# placing their own bets. This bot sends its transaction a few blocks before the contract locks.


gasStrat = LinearScalingStrategy(int(6e9), int(20e9), 1.3,5)


def get_current():
    block1 = web3.eth.get_block_number()
    return block1
print(get_current())
def get_bal():
    bal = accounts[0].balance()
    return bal
def get_epoch():
    epoch1 = prediction.currentEpoch({'from': accounts[0]})
    return epoch1
def get_info(epoch):
    roundinfo1 = prediction.rounds(epoch, {'from': accounts[0]})

    return roundinfo1

def pause():
    pause = prediction.paused({'from': accounts[0]})
    return pause




def get_bets(epoch):
    pause1 = pause()
    if pause1 == True:
        time.sleep(200)
        return
    # if bull == 0:
    #     time.sleep(3)
    #     get_bets()
    # if bear == 0:
    #     time.sleep(3)
    #     get_bets()
    bal = get_bal()
    bet = bal / 40
    info = get_info(epoch)
    if info[1] == 0:

        time.sleep(60)


        get_bets(epoch)
    if bet > 1e18:
        bet = 1e18

    try:
        new = get_current()
        ratio = [info[8] / info[7],  info[7] / info[8]]
        if ratio[0] >= 3.5 and info[2] - 5 <= new:

            prediction.betBull({'from': accounts[0], 'amount': bet, 'gas_price': 8e9})
            time.sleep(20)
        if ratio[1] >= 3.5 and info[2] - 5 <= new:
            prediction.betBear({'from': accounts[0], 'amount': bet, 'gas_price': 8e9})
            time.sleep(20)


    except (ZeroDivisionError, ValueError):

        time.sleep(20)
        pass

    else:
        time.sleep(.25)




def main():
    get_bal()
    get_current()
    i = 0
    while i < 1:
        epoch = get_epoch()
        get_bets(epoch)