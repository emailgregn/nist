import requests
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE
import binascii
from struct import *
import tempfile
import os

class NistRecord(object):
    '''
      Sample XML
      <record>
        <version>Version 1.0</version>
        <frequency>60</frequency>
        <timeStamp>1419683040</timeStamp>
        <seedValue>F39935ABD1522D43732E9A1CBA079EDC472094A81B63D03B8D837AE0826ADB0D7FF79EF3899F226F81A5394C51CEC3A1923083298D339C62EE86F06818AC53BC</seedValue>
        <previousOutputValue>A0D21B6954FF33B5BD164F6039F2E0878E749FEE8C2DAD481BF9B38DF4D9CCD0A1BD8BCAD3D497FB934B52C39B24F54E6B961758A3D5C4606F87C163E86326D7</previousOutputValue>
        <signatureValue>A33B1C710362FCD49F64E7EE2DE5DAA47CEC5B319B058A05D159F852C7715FE19AADDECEC5C578DAA934C7A6A9771CE4709D9C68592B6699A224A28E17895632B0FB749B279F9BC9AEF9E3B0F4001589D3FE705CE9AD6B5159A11D46F0252BD2851FE933183D00FC0D8DB7179C4AF73D4E6FA51CB7DF4E2D3666ACC9984D28E408BB44387DF41320C70ABD537754AC705D6425A5B22489B53779EF9B2E2CAE71FF5069F98BD2CB07B13E3C367EBDC4B5F12B61142930965AE9A7C4356E978D9C1DF8FE6F1FCC277382537F812F8B3BE773F74816DB5D2E139280ED7CD9235C32E8BB299C65ED4C6B6BBA05C08DECFC8A5E1DE5498337158C6D7D1ED5E59A1572</signatureValue>
        <outputValue>6CFE1FAD91DD7B505897CFAA855C595D48F10F92647311C744427CA6F3068F9E33042810C248862B124E52FB80C12DDD96DCA99B51D4CEA92BB4B404E8A1767E</outputValue>
        <statusCode>0</statusCode>
      </record>
    '''

    def __init__(self, xmlString, certificate = None):
        '''
          ## Version number (ascii text)
          ## Update frequency (4 bytes)
          ## Time Stamp (8 bytes)
          ## The HW RNG seedValue (64 bytes)
          ## The previous output value, does the chaining (64 bytes)
          ## Status code (4 bytes)endian
        '''
        root = ET.fromstring(xmlString)

        self.version        = root.find('version').text
        self.frequency      = int(root.find('frequency').text)
        self.timestamp      = int(root.find('timeStamp').text)
        self.seed           = long(root.find('seedValue').text, 16)
        self.previousOutput = long(root.find('previousOutputValue').text, 16)
        # reverse it and change from little to big endian. Store it as bin, liek the file
        self.signature      = binascii.unhexlify(self._msByteSwap(root.find('signatureValue').text))
        self.statusCode     = int(root.find('statusCode').text)
        self.randomNumber   = long(root.find('outputValue').text,16)
        #if not self.isVerified():
        #  raise ValueError
        self.certificate = certificate
        
    def _msByteSwap(self, nistSignature):
        """ 
        reverse the whole string and then change the bytes from little to big endian
        """
        revSignature = nistSignature[::-1]
        size = 2
        return ''.join(revSignature[pos:pos + size][::-1] for pos in xrange(0, len(revSignature), size))

    def _binify(self, l):
        """
        because we can't struct.pack a long. Thanks http://stackoverflow.com/a/4670889
        """
        h = hex(l)[2:].rstrip('L')
        return binascii.unhexlify('0'*(32-len(h))+h)

    
    def toBinary(self):
        return self.version \
            + pack('>1I1Q64s64s1I',
                self.frequency,
                self.timestamp,
                binascii.unhexlify((hex(self.seed)[2:]).rstrip('L')),
                binascii.unhexlify((hex(self.previousOutput)[2:]).rstrip('L')),
                self.statusCode )
            

    def isVerified(self):
        '''
        Checks the signatures and hashes and blah
        #Thanks: http://hackaday.com/2014/12/19/nist-randomness-beacon/
        /usr/bin/openssl x509 -pubkey -noout -in beaconistRecordn.cer &gt; beaconpubkey.pem
        ## Test signature / key on packed data
        /usr/bin/openssl dgst -sha512 -verify beaconpubkey.pem -signature beacon.sig beacon.bin

        #Thanks: http://stackoverflow.com/questions/7659972/how-can-i-verify-an-x509-certificate-in-python-including-a-crl-check
        p1 = Popen(["openssl", "verify", "from -CApath", capath, "-crl_check_all"],
                  stdin = PIPE, stdout = PIPE, stderr = PIPE)
        message, error = p1.communicate(certificate)
        verified = ("OK" in message and not "error" in message)
        return verified
        '''
        sig = self.signature
        bbin =  self.toBinary()
        
        #stuff data into temp files
        cer_fd, cer_filename   = tempfile.mkstemp( suffix='.cer', text=True )
        pem_fd, pem_filename   = tempfile.mkstemp( suffix='.pem', text=True )
        sig_fd, sig_filename   = tempfile.mkstemp( suffix='.sig', text=True )
        bbin_fd, bbin_filename = tempfile.mkstemp( suffix='.bin', text=False)
        try:
            os.write(cer_fd, self.certificate)
            os.close(cer_fd)

            p1 = Popen(["openssl", "x509", "-pubkey",  "-noout", "-in", cer_filename], stdin = PIPE, stdout = PIPE, stderr = PIPE)       
            # grab the stdout
            pem, error = p1.communicate()
        
            os.write(pem_fd, pem)
            os.close(pem_fd)
            os.write(sig_fd, sig)
            os.close(sig_fd)
            os.write(bbin_fd, bbin)
            os.close(bbin_fd)            
            # ...run the subprocess and wait for it to complete...
            p2 = Popen(["openssl", "dgst", "-sha512", "-verify", pem_filename, "-signature", sig_filename, bbin_filename], stdin = PIPE, stdout = PIPE, stderr = PIPE)
            message, error = p2.communicate()
            verified = ("OK" in message and not "error" in message)
            return verified
            #return message
            
        finally:
            os.remove(cer_filename)
            os.remove(pem_filename)
            os.remove(sig_filename)
            os.remove(bbin_filename)


