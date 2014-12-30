import binascii
from lettuce import world, steps, step
from nose.tools import *
#

from nistrecord import *
from nistfetcher import *


@steps
class NistFetcherSteps(object):

    def __init__(self, environs):
        self.e = environs
        self.e.nistRecord = None
        self.e.nistFetcher = NistFetcher()

    """Methods in exclude or starting with _ will not be considered as step"""
    exclude = ['set_something']

    def _set_number(self, value):
        self.e.number = int(value)

    def _get_number(self):
        return self.e.number

    def _set_timestamp(self, value):
        self.e.timestamp = value

    def _get_timestamp(self):
        return self.e.timestamp



    def the_timestamp_is(self, step, timestamp):
        '''the timestamp is set to (\d+)'''
        self._set_timestamp(timestamp)

    def fetching_the_current_random_number(self, step):
        '''fetching the current random number'''
        self.e.nistRecord = self.e.nistFetcher.currentRecord(self.e.timestamp)

    def fetching_the_previous_random_number(self, step):
        '''fetching the previous random number'''
        self.e.nistRecord = self.e.nistFetcher.previousRecord(self.e.timestamp)
        
    def fetching_the_next_random_number(self, step):
        '''fetching the next random number'''
        self.e.nistRecord = self.e.nistFetcher.nextRecord(self.e.timestamp)
        
    def then_the_random_number_is(self, step, expected):
        '''the random number is (\d+)'''
        assert_equals(long(expected), self.e.nistRecord.randomNumber)

    def then_the_previous_number_is(self, step, expected):
        '''the previous number is (\d+)'''
        assert_equals(long(expected), self.e.nistRecord.previousOutput)

    def then_the_seed_value_is(self, step, expected):
        '''the seed value is (\d+)'''
        assert_equals(long(expected), self.e.nistRecord.seed)

    def then_the_timestamp_is(self, step, expected):
        '''the timestamp is (\d+)'''
        assert_equals(int(expected), self.e.nistRecord.timestamp)

    def yyy(self, step):
        '''asdfasdf'''
        self._set_number(nistFetcher.currentRecord(self.e.timestamp).randomNumber)

    def fetching_the_start_of_the_chain(self, step):
        '''fetching the start of the chain'''
        self._set_number(self.e.nistFetcher.startChainRecord(self.e.timestamp).randomNumber)
        
    def the_signature_matches_file(self, step, filename):
        '''the signature matches file (.+)'''
        with open(filename, mode='rb') as file:
            sigcontent = file.read()        
            assert_equals( binascii.hexlify(self.e.nistRecord.signature), binascii.hexlify(sigcontent) )



# Important!
# Steps are added only when you instanciate the "@steps" decorated class
# Internally decorator "@steps" build a closure with __init__

NistFetcherSteps(world)
