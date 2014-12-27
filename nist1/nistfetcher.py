import requests

class NistFetcher(object):
    def currentRecord(self, timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/' + timestamp)
        if r.status_code == 200:
            return NistRecord(r.content)
        else:
            raise IOError

    def previousRecord(self,timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/previous/' + timestamp)
        if r.status_code == 200:
            return NistRecord(r.content)
        else:
            #print r.status_code
            #print r.headers
            #print r.content
            raise IOError

    def nextRecord(self,timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/next/' + timestamp)
        if r.status_code == 200:
            return NistRecord(r.content)
        else:
            raise IOError

    def lastRecord(self):
        r = requests.get('https://beacon.nist.gov/rest/record/last')
        if r.status_code == 200:
            return NistRecord(r.content)
        else:
            raise IOError

    def startChainRecord(self, timestamp):
        r = requests.get('https://beacon.nist.gov/rest/record/start-chain/' + timestamp)
        if r.status_code == 200:
            return NistRecord(r.content)
        else:
            raise IOError
