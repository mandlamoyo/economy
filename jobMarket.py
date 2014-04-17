from constants import WORKER

class JobMarket:
    jobs = {}
    
    @staticmethod
    def addJob( job ):
        JobMarket.jobs[job.jid] = job
        
    @staticmethod
    def removeJob( jid ):
        del JobMarket.jobs[jid]
        
    @staticmethod
    def getJob( jid ):
        return JobMarket.jobs[jid]
        
    @staticmethod
    def applyForJob( jid, worker ):
        job = JobMarket.jobs[jid]
        job.apply( worker )
        
    @staticmethod
    def unapply( worker ):
        for job in JobMarket.jobs.itervalues():
            job.unapply( worker )
        
    @staticmethod
    def printDetails():
        print "JID,\tFID,\tWage,\tApplicants"
        jobs = JobMarket.jobs.values()
        jobs.sort( key=lambda j: j.wage, reverse=True )
        for job in jobs:
            print job.jid, "\t", job.firm.fid, "\t", job.wage, "\t", len(job.applicants)
        
class Job:
    jids = 0

    def __init__( self, wage, firm ):
        self.jid = Job.jids
        Job.jids += 1
        
        self.position = WORKER
        self.wage = wage
        self.firm = firm
        self.applicants = []
        
    def apply( self, worker ):
        if worker not in self.applicants:
            self.applicants.append( worker )
            
    def unapply( self, worker ):
        if worker in self.applicants:
            self.applicants.remove( worker )