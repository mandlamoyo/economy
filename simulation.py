from workers import Workers
from jobMarket import JobMarket
from farm import Farm
from random import shuffle
from constants import NONE, SOME, ALL, STATS

Workers.buildWorkers(75)
fs = [Farm(200) for i in range(20)]

def updateAll( show, n=1 ):
    dead = []
    print "Unemp,\tGDI,\tWage[L:A:H]\tProd,\tProf,\tCap,\tNet Val,\tRich,\t\tAvg,\t\tPoor"
    
    for r in range(n):
        production = 0
        netProfit = 0
        capital = 0
        allMoney = []

        shuffle(fs)
        for f in fs:
            f.update(show)
            [money,profit,prod] = f.getInfo()
            netProfit += profit
            production += prod
            capital += f.tractors
            allMoney.append(money)
            
            if f.money <= 0: dead.append(f)
            
        for f in dead: fs.remove(f)
        unemployment = Workers.update()
        gdi = Workers.getTotalIncome()
        [lw,hw] = Workers.getWageRange()
        aw = Workers.getAverageWage()
        netValue = sum(allMoney)
        avm = netValue/len(allMoney)
        richest = max(allMoney)
        poorest = min(allMoney)
        
        if show == STATS:
            print "%.2f%%,\t$%d,\t[$%d:$%d:$%d],\t%d,\t$%d,\t%d\t$%d,\t\t$%d,\t\t$%d,\t\t$%d" % (unemployment, gdi, lw, aw, hw, production, netProfit, capital, netValue, richest, avm, poorest)
    
