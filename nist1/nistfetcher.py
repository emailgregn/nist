import requests

from nistrecord import NistRecord

class NistFetcher(object):

    def __init__(self):
        self.certificate = None
        r = requests.get('https://beacon.nist.gov/certificate/beacon.cer')
        if r.status_code != 200:
            raise IOError
        else:
            self.certificate = r.content
                       
    def currentRecord(self, timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/' + str(timestamp))
        if r.status_code == 200:
            return NistRecord(r.content, self.certificate)
        else:
            raise IOError

    def previousRecord(self,timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/previous/' + str(timestamp))
        if r.status_code == 200:
            return NistRecord(r.content, self.certificate)
        else:
            #print r.status_code
            #print r.headers
            #print r.content
            raise IOError

    def nextRecord(self,timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/next/' + str(timestamp))
        if r.status_code == 200:
            return NistRecord(r.content, self.certificate)
        else:
            raise IOError

    def lastRecord(self):
        r = requests.get('https://beacon.nist.gov/rest/record/last')
        if r.status_code == 200:
            return NistRecord(r.content, self.certificate)
        else:
            raise IOError

    def startChainRecord(self, timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/start-chain/' + str(timestamp))
        if r.status_code == 200:
            return NistRecord(r.content, self.certificate)
        else:
            raise IOError
    
    def verifyChain(self, fromTimestamp):
        steps = 1
        cr = self.currentRecord(fromTimestamp)
        if not cr.isVerified:
            raise Exception('CurrentRecord %d not verified' % (cr.timestamp))
        
        sr = self.startChainRecord(fromTimestamp)
        if not sr.isVerified:
            raise Exception('StartChainRecord %d not verified' % (sr.timestamp))
        while (cr.timestamp >= sr.timestamp):
            pr = self.previousRecord(cr.timestamp)
            if not pr.isVerified:
                raise Exception('ChainRecord %d not verified' % (pr.timestamp))
            if not pr.randomNumber != cr.previousRecord:
                raise Exception('Chain broken between %d and %d' % (pr.timestamp, cr.timestamp)
            cr = pr
            steps++
        
        return steps