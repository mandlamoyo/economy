from constants import UNEMPLOYED, FIRST, MINIMUM_WAGE
from jobMarket import JobMarket
from random import random, randint, shuffle

class Workers:
    workers = []

    @staticmethod
    def addWorker( worker ):
        Workers.workers.append( worker )
    
    @staticmethod
    def buildWorkers( amount ):
        for i in range( amount ):
            Workers.addWorker( Worker() )
    
    @staticmethod
    def update():
        #print ''
        dec = []
        unemployed = 0
        shuffle( Workers.workers )
        for w in Workers.workers:
            dec.append( w.update() )
            if w.status == UNEMPLOYED: unemployed += 1
            
        return unemployed/float( len( Workers.workers ))    
        #print "Workers who decreased wages: ", filter( lambda x: x != None, dec ) 
            
    @staticmethod
    def getTotalIncome():
        return sum( [w.firm.wage for w in Workers.workers if w.firm] )
    
    @staticmethod
    def getAverageWage():
        wages = [w.firm.wage for w in Workers.workers if w.firm]
        if wages: return sum(wages)/float(len(wages))
        return 0
    
    @staticmethod
    def getWageRange():
        wages = [w.firm.wage for w in Workers.workers if w.firm]
        if wages: return [min(wages),max(wages)]
        return [0,0]
        
    @staticmethod
    def printDetails():
        Workers.workers.sort( key=lambda w: w.productivity, reverse=True )
        print "Productivity,\tWID,\tStat,\tSaved,\tWage,\tWage(m),\tJob Offers"
        
        for w in Workers.workers:
            wage = 0
            if w.firm: wage = w.firm.wage
            print "%.5f\t\t%d\t%d\t%d\t%d\t%d\t\t%d" % ( w.productivity, w.wid, w.status, w.savings, wage, w.wageLimit, w.lastJobOffers)
    
    '''
    @staticmethod
    def hire( fid ):
        available = filter( lambda x: x.status == UNEMPLOYED, Workers.workers )
        if available:
            available[FIRST].status = fid
            return available[FIRST]
        return None
    '''
    
    
class Worker:
    wids = 0
    def __init__( self ):
        self.wid = Worker.wids
        Worker.wids += 1
        
        self.wageLimit = randint( MINIMUM_WAGE, MINIMUM_WAGE + MINIMUM_WAGE/2 )
        self.jobOffers = []
        self.productivity = random() + random()
        self.status = UNEMPLOYED
        self.savings = 0
        self.firm = None
        self.lastJobOffers = 0
        self.delay = 0
        self.waitingTime = randint(2,10)
        self.incLim = 3 #randint(2,5)
        
    def pay( self, salary ):
        self.savings += salary
        
    def fire( self, forced=True ):
        #if forced: print "Worker %d\twas fired from firm %d" % (self.wid, self.firm.fid)
        self.status = UNEMPLOYED
        self.firm = None
        
    def offerJob( self, job ):
        self.jobOffers.append( job )
        
    def acceptJob( self, job ):
        if self.firm:
            #print "Worker %d\tleft firm %d\t\t\t[wage:%d]" % (self.wid, self.firm.fid, self.firm.wage)
            self.firm.quit( self )
            
        self.jobOffers = []
        self.status = job.firm.fid
        job.firm.hire( self, job.jid )
        JobMarket.unapply( self )
        self.firm = job.firm
        
    def update( self ):
        dec = None
        JobMarket.unapply( self )
        if self.status == UNEMPLOYED:
            if len( self.jobOffers ) == 0:
                self.delay += 1
                if self.delay > self.waitingTime and self.wageLimit > MINIMUM_WAGE:
                    self.delay = 0
                    self.wageLimit -= 1
                    #print "Worker %d\tdecreased wage limit to %d\t[wait:%d]" % (self.wid, self.wageLimit, self.waitingTime)
                    dec = self.wid
                    
            else:
                self.delay = 0
            
            wl = self.wageLimit
        else:
            wl = self.firm.wage
            
        self.savings += 10
        offers = sorted( self.jobOffers, key=lambda job: job.wage, reverse=True )
        if offers:
            if len( offers ) > self.incLim: 
                self.wageLimit += 1
                #print "Worker %d\tincreased wage limit to %d\t[offers:%d]" % (self.wid, self.wageLimit, len(offers))
            
            else:
                self.acceptJob( offers[0] )
                #print "Worker %d\taccepted job %d\tat firm %d\t[wage:%d]" % (self.wid, offers[0].jid, offers[0].firm.fid, offers[0].firm.wage)
        
        else:
            for jid in JobMarket.jobs:
                job = JobMarket.jobs[jid]
                if job.wage > self.wageLimit and ( not self.firm or job.firm != self.firm ):
                    JobMarket.applyForJob(jid, self)
            
        self.lastJobOffers = len( self.jobOffers )
        self.jobOffers = []
        return dec