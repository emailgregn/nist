import binascii
from lettuce import world, steps
from nose.tools import *
#

from nistrecord import *
from nistfetcher import *


@steps
class NistFetcherSteps(object):
    """Methods in exclude or starting with _ will not be considered as step"""

    exclude = ['set_something']

    def __init__(self, environs):
        self.environs = environs
        self.nist = None
        self.nistRecord = None



    def _set_number(self, value):
        self.environs.number = int(value)

    def _get_number(self):
        return self.environs.number

    def _set_timestamp(self, value):
        self.environs.timestamp = int(value)

    def _get_timestamp(self):
        return self.environs.timestamp

    def _set_xmlString(self, value):
        self.environs.xmlString = value

    def _get_xmlString(self):
        return self.environs.xmlString



    def the_timestamp_is(self, step, timestamp):
        '''the timestamp is (\d+)'''
        self._set_timestamp(timestamp)

    def fetching_the_current_random_number(self):
        '''fetching the current random number'''
        self._set_number(nist.currentRecord(self.environs.timestamp).randomNumber)


    def fetching_the_previous_random_number(self):
        '''fetching the previous random number'''
        self._set_number(nist.previousRecord(self.environs.timestamp).randomNumber)
        
    def fetching_the_next_random_number(self):
        '''fetching the next random number'''
        self._set_number(nist.nextRecord(self.environs.timestamp).randomNumber)

    def yyy(self):
        self._set_number(nist.currentRecord(self.environs.timestamp).randomNumber)

    def fetching_the_start_of_the_chain(self):
        '''fetching the start of the chain'''
        self._set_number(nist.startChainRecord(self.environs.timestamp).randomNumber)

    def xml_string(self,step, xml):
        '''Given XML string (.+)'''
        self._set_xmlString(xml)
        
    def xml_string_from_file(self,step, filename):
        '''Given XML file (.+)'''
        with open(filename, mode='r') as file:
            self._set_xmlString(file.read())

    def the_nistrecord_is_constructed(self, step):
        '''When the nistRecord is constructed'''
        self.nistRecord = NistRecord(self._get_xmlString())

    def then_the_randomnumber_is(self, step, expected):
        '''Then the randomNumber is (\d+)'''
        assert_equals(expected, self.nistRecord.randomNumber)

    @raises(Exception)
    def then_creating_the_nistrecord_throws_an_exception(self, step):
        '''Then creating the NistRecord throws an exception'''
        self.nistRecord = NistRecord(self._get_xmlString())

    def then_the_tobinary_matches_file(self, step, filename):
        '''Then the toBinary matches file (.+)'''
        with open(filename, mode='rb') as file:
            bincontent = file.read()        
            assert_equals( binascii.hexlify(self.nistRecord.toBinary()), binascii.hexlify(bincontent) )

    def then_the_isverified_is_bool(self, step, verified):
        '''Then the isVerified is (.+)'''
        assert_equals( self.nistRecord.isVerified(), bool(verified) )





# Important!
# Steps are added only when you instanciate the "@steps" decorated class
# Internally decorator "@steps" build a closure with __init__

NistFetcherSteps(world)
