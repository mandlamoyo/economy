from random import random, randint
from farmersMarket import FarmersMarket
from tractorMarket import TractorMarket
from workers import Workers
from jobMarket import *
from constants import *

class Farm:
    fids = 0
    
    def __init__( self, money, wage=MINIMUM_WAGE, owners=1 ):
        self.fid = Farm.fids
        Farm.fids += 1
        
        self.owners = owners
        self.stored = 0
        self.produced = 0
        self.jobs = []
        self.workers = []
        self.money = money
        self.seeds = 0
        self.tractors = 0
        self.wage = wage
        
        self.cycles = 0
        self.cycleProduction = 0
        self.income = 0
        self.expenses = 0
        self.profit = 0

        self.seedThreshold = [5,MAX_SEEDS]
        self.produceThreshold = [2,5]
        self.tractorThreshold = [370,75]
        self.workerThreshold = [200,32]
        
        self.prodConst = 1 # biasedRandom(True) + biasedRandom(False)
        self.log = []
        #self.printDetails()
        
    def setThresholds( self, seed=None, tractor=None, worker=None ):
        if seed: self.seedThreshold = seed
        if tractor: self.tractorThreshold = tractor
        if worker: self.workerThreshold = worker
    
    def resetStats( self ):
        self.income = 0
        self.expenses = 0
        self.profit = 0
    
    def manageSeeds( self ):
        self.log.append( "\nBuying seeds.." )
        self.log.append( "\t[M:" + str(self.money) + ",S:" + str(self.seeds) + "]" )
        while self.seeds < self.seedThreshold[BUY] and self.money > 0:
            price = FarmersMarket.buySeeds(1)
            self.expenses += price
            self.money -= price
            self.seeds += 1
            
        self.log.append( "\t->[M:" + str(self.money) + ",S:" + str(self.seeds) + "]" )
        
    def payWorkers( self ):
        toFire = []
        workers = len(self.workers)
        self.log.append( "\nPaying " + str(len(self.workers)) + " workers $" + str(self.wage*len(self.workers)))
        self.log.append( "\t[M:" + str(self.money) + "]")
        self.workers.sort( key=lambda w: w.productivity, reverse=True )
        for w in self.workers:
            if self.money*self.prodConst - self.wage*workers < self.workerThreshold[SELL] or self.money - self.wage <= 0: # mechanism for changing wage?
                toFire.append(w)
                workers -= 1
            else:
                w.pay( self.wage )
                self.money -= self.wage
                self.expenses += self.wage
                
        self.log.append( "\t->[M:" + str(self.money) + "]")
        
        if toFire:
            self.log.append( "\nFiring " + str(len(toFire)) + " workers" )
            for w in toFire:
                self.fireWorker( w )
                
            self.log.append( str(len(self.workers)) + " workers left" )
            
    def fireWorker( self, worker, forced=True ):
        self.workerThreshold[BUY] -= len(self.workers)*15
        self.log.append( "New worker hiring threshold: $" + str( self.workerThreshold[BUY] ))
        self.workers.remove( worker )
        #self.wage -= 1
        worker.fire( forced )
    
    def quit( self, worker ):
        #self.wage += 2
        self.fireWorker( worker, False )
    
    def maintainTractors( self ):
        self.log.append( "\nPerforming tractor maintenance for $" + str(TRACTOR_MAINTENANCE*self.tractors) )
        self.log.append( "\t[M:" + str(self.money) + "]")
        for i in range(self.tractors):
            if self.money*self.prodConst - TRACTOR_MAINTENANCE*self.tractors < self.tractorThreshold[SELL] or self.money - TRACTOR_MAINTENANCE <= 0:
                price = TractorMarket.sellTractors(1)
                self.income += price
                self.money += price
                self.tractors -= 1
                self.log.append( "\t\tSold 1 tractor for $" + str(price))
            else:
                self.expenses += TRACTOR_MAINTENANCE
                self.money -= TRACTOR_MAINTENANCE
                
        self.log.append( "\t->[M:" + str(self.money) + "]")
        
    def manageTractors( self ):
        #if len( self.workers ) + self.owners <= self.tractors:
        #    return False
            
        if (self.money*self.prodConst < self.tractorThreshold[SELL] or self.tractors > len(self.workers)) and self.tractors > 0:
            price = TractorMarket.sellTractors(1)
            self.income += price
            self.money += price
            self.tractors -= 1
            self.log.append( "\t\tSold 1 tractor for $" + str(price))
            return True
            
        elif self.money*self.prodConst > self.tractorThreshold[BUY] and self.tractors < MAX_TRACTORS and self.tractors < len( self.workers ):
            price = TractorMarket.buyTractors(1)
            self.expenses += price
            self.money -= price
            self.tractors += 1
            self.log.append( "\t\tBought 1 tractor for $" + str(price))
            return True
        
        else:
            return False
            
    def manageWorkers( self ): 
        cancelledJobs = []
        offered = []
        worker = None
        
        self.log.append( "\t\tPending jobs:" )
        for jid in self.jobs:
            job = JobMarket.getJob( jid )
            self.log.append( "\t\t\tJob " + str( jid ) + " - " + str( len( job.applicants )) + " Applicants" )
            
        self.log.append( "" )
        
        for i in range(len(self.jobs)):
            if self.money*self.prodConst - self.wage*(len(self.workers)+i+1) < self.workerThreshold[SELL]: # mechanism for changing wage?
                cancelledJobs.append( self.jobs[i] )
            else:
                job = JobMarket.getJob( self.jobs[i] )
                if len(job.applicants) > 0 and len(job.applicants) > len(offered):
                    job.applicants.sort( key=lambda w: w.productivity, reverse=True )
                    for w in job.applicants:
                        if w not in offered:
                            w.offerJob( job )
                            offered.append( w )
                            self.log.append( "\t\tOffering job " + str( job.jid ) + " to worker " + str( w.wid ))
                            break
                    
                elif self.money*self.prodConst - (self.wage+1)*(len(self.workers)+i+1) > self.workerThreshold[SELL]:
                    self.log.append( "\t\tNo applicants for job " + str( job.jid ) + ". Raising wage" )
                    self.wage += 1
                
                else:
                    self.log.append( "\t\tWage too high, lowering.." )
                    self.wage -= 1
                    
        for jid in cancelledJobs:
            self.jobs.remove( jid )
            JobMarket.removeJob( jid )
    
        if self.money*self.prodConst > self.workerThreshold[BUY] and len(self.workers) < MAX_WORKERS:
            job = Job( self.wage, self )
            JobMarket.addJob( job )
            self.jobs.append( job.jid )
            
        self.updateJobs()    
        return False
        
    def hire( self, worker, jid ):
        self.log.append( "\t\tHiring a new worker" )
        #self.wage += 1
        worker.wage = self.wage
        
        self.jobs.remove( jid )
        JobMarket.removeJob( jid )
        self.workers.append( worker )
        self.workerThreshold[BUY] += len(self.workers)*15
        self.log.append( "\t\tNew worker hiring threshold: $" + str( self.workerThreshold[BUY] ))
        
        
    def manageFinances( self ):
        self.manageSeeds()
        self.payWorkers()
        self.maintainTractors()
        
        trading = True
        self.log.append( "\nTrading..\n\t[M:" + str(self.money) + "]" )
        while trading:
            trading = self.manageTractors() or self.manageWorkers() #preference list?
            self.log.append( "\t->[M:" + str(self.money) + "]")
    
    def getOutput( self ):
        s = min(self.seeds,MAX_SEEDS)
        w = min(sum( [w.productivity for w in self.workers] )+self.owners,MAX_WORKERS)
        t = min( self.workers, self.tractors, MAX_TRACTORS ) + 1
    
        out = s + s * (t*TRACTOR_CONSTANT) * (w*WORKER_CONSTANT - (w**2)/396.)
        return int( out*self.prodConst )
        
    def sellProduce( self ):
        oldSeeds = self.seeds
        self.seeds += int( self.produced * PRODUCE_SEED_RATIO )
        
        self.log.append( "\nProduced " + str( self.produced ) + " this cycle\t\t[Str:" + str(self.stored) + "]" )
        self.log.append( "Seeds: " + str( oldSeeds ) + " -> " + str( self.seeds ) + "\t\t\t[ST:" + str(self.seedThreshold[SELL]) + "]" )

        excess = self.seeds - self.seedThreshold[SELL]
        if excess > 0:
            price = int( FarmersMarket.sellSeeds( excess ))
            self.income += price
            self.money += price
            self.seeds = self.seedThreshold[SELL]
            self.log.append( "Sold " + str( excess ) + " seeds for $" + str(price) + " [M:" + str(self.money) + "]")
            
        self.log.append( "\nSelling produce..\t\t[PT:" + str(self.produceThreshold[SELL]) + "]"  )
        '''excess = self.produced - self.produceThreshold[SELL]
        if excess > 0:
            price = FarmersMarket.sellProduce( excess )
            self.income += price
            self.money += price
            self.produced = self.produceThreshold[SELL]
            self.log.append( "\tSold " + str( excess ) + " produce for $" + str(price) + "\t[M:" + str(self.money) + ",P:" + str( self.produced ) + "]" )
            
        else:'''
        # Take produce from stores
        third = self.stored/3
        self.produced += third*2
        self.stored = third
        self.log.append( "\tStores used\t\t[P:" + str(self.produced) + ", Str:" + str(self.stored) + "]" )
        
        excess = self.produced - self.produceThreshold[SELL]
        if excess > 0:
            quart = self.produced/4
            self.stored += quart
            self.produced = quart*3
            self.log.append( "\tExcess crop stored\t[P:" + str(self.produced) + ", Str:" + str(self.stored) + "]" )
            
        else:
            self.produced += self.stored
            self.stored = 0
            self.log.append( "\tStores depleted\t\t[P:" + str(self.produced) + "]" )
            '''
            price = FarmersMarket.sellProduce( excess )
            self.income += price
            self.money += price
            self.produced = self.produceThreshold[SELL]
            self.log.append( "\tSold " + str( excess ) + " produce for $" + str(price) + "\t[M:" + str(self.money) + ",P:" + str( self.produced ) + "]" )
        
        else:
            '''
        total = self.produced
        price = FarmersMarket.sellProduce( total )
        self.income += price
        self.money += price
        self.produced = 0
        self.log.append( "\tSold " + str( total ) + " produce for $" + str(price) + "\t[M:" + str(self.money) + ",P:" + str( self.produced ) + "]" )
    
    def storeExcess( self ):
        self.stored += self.produced
        self.produced = 0
        self.log.append( "\nExcess produce stored..\t\t[P:" + str(self.produced) + ",Str:" + str(self.stored) + "]" )
    
    def updatePC( self ):
        self.prodConst += biasedRandom() * randint(-1,1)
        if self.prodConst < 0.3: self.prodConst = 0.3
        if self.prodConst > 1.7: self.prodConst = 1.7
        self.log.append( "Productivity Constant updated\t[PC: " + str(self.prodConst) + "]" )
    
    def updateJobs( self ):
        for jid in self.jobs:
            job = JobMarket.getJob(jid)
            job.wage = self.wage
    
    def updateLog( self, show, clear=True ):
        if show == ALL:
            for l in self.log: print l
            print ''
        
        if clear:
            self.log = []
    
    def printDetails( self ):
        print "--------------------------------------------------"
        print "Farm ID:\t", self.fid, ":: Cycles:\t", self.cycles, ":: Money:\t", self.money
        print "Income:\t\t", self.income, ":: Expenses:\t", self.expenses, ":: Profit:\t", self.income - self.expenses
        print "\nProduced:\t", self.cycleProduction, ":: Stored:\t", self.stored
        print "Seeds:\t\t", self.seeds, ":: Workers:\t", len(self.workers), ":: Tractors:\t", self.tractors
        print "Wage:\t\t", self.wage, ":: PC:\t", self.prodConst
        print "\n=================================================="
    
    def getInfo( self ):
        return [self.money, self.income - self.expenses, self.cycleProduction]
    
    def update( self, show=ALL ):
        self.cycles += 1
        self.resetStats()
        self.log.append( "Cycle: " + str(self.cycles))
        
        self.manageFinances()
        
        self.produced = self.getOutput()
        self.cycleProduction = self.produced
        
        self.sellProduce()
        
        #self.storeExcess()
        
        self.updatePC()
        
        self.updateLog( show )
        if show == SOME or show == ALL: self.printDetails()

        
