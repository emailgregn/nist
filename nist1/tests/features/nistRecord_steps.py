import binascii
from lettuce import world, steps
from nose.tools import *
#

from nistrecord import *
from nistfetcher import *


@steps
class NistRecordSteps(object):
    """Methods in exclude or starting with _ will not be considered as step"""

    exclude = ['set_something']

    def __init__(self, environs):
        self.e = environs
        self.e.nistRecord = None
        self.e.nistFetcher = NistFetcher()
        
    def _set_xmlString(self, value):
        self.e.xmlString = value

    def _get_xmlString(self):
        return self.e.xmlString        



    def xml_string(self, step, xml):
        '''Given XML string (.+)'''
        self._set_xmlString(xml)

    def xml_string_from_file(self,step, filename):
        '''Given XML file (.+)'''
        with open(filename, mode='r') as file:
            self._set_xmlString(file.read())

    def the_nistrecord_is_constructed(self, step):
        '''When the nistRecord is constructed'''
        self.e.nistRecord = NistRecord(self._get_xmlString(), self.e.nistFetcher.certificate )

    @raises(Exception)
    def then_creating_the_nistrecord_throws_an_exception(self, step):
        '''Then creating the NistRecord throws an exception'''
        self.e.nistRecord = NistRecord(self._get_xmlString(), self.e.nistFetcher.certificate )

    def then_the_tobinary_matches_file(self, step, filename):
        '''Then the toBinary matches file (.+)'''
        with open(filename, mode='rb') as file:
            bincontent = file.read()        
            assert_equals( binascii.hexlify(self.e.nistRecord.toBinary()), binascii.hexlify(bincontent) )

    def then_the_isverified_is_bool(self, step, verified):
        '''Then the isVerified is (.+)'''
        assert_equals( self.e.nistRecord.isVerified(), bool(verified.upper() == 'TRUE') )


# Important!
# Steps are added only when you instanciate the "@steps" decorated class
# 

NistRecordSteps(world)
