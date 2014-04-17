from random import randint
from math import sqrt

UNEMPLOYED = -1
WORKER = -1

BUY = 0
SELL = 1

PRICE = 0
PRODUCT = 1

SEEDS = 0
PRODUCE = 1

TRACTORS = 0
FIRST = 0

TRACTOR_CONSTANT = 0.8
WORKER_CONSTANT = 0.2
PRODUCE_SEED_RATIO = 0.2

TRACTOR_MAINTENANCE = 74
MINIMUM_WAGE = 18

MAX_SEEDS = 20
MAX_WORKERS = 20
MAX_TRACTORS = 5

NONE = 0
SOME = 1
ALL = 2
STATS = 3

def biasedRandom( low=True ):
    res = sqrt( randint( 0,100**2 ))
    if low: res = 100 - res
    return res/100