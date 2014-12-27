Feature: XML from NIST is parsed into a nist1.nistRecord
  In order to accept data from NIST
  As a developer
  nist1 can parse XML into a NistRecord class
  
  Scenario: Well formed XML
    Given XML string <?xml version="1.0" encoding="UTF-8" standalone="yes"?><record><version>Version 1.0</version><frequency>60</frequency><timeStamp>1419683040</timeStamp><seedValue>F39935ABD1522D43732E9A1CBA079EDC472094A81B63D03B8D837AE0826ADB0D7FF79EF3899F226F81A5394C51CEC3A1923083298D339C62EE86F06818AC53BC</seedValue><previousOutputValue>A0D21B6954FF33B5BD164F6039F2E0878E749FEE8C2DAD481BF9B38DF4D9CCD0A1BD8BCAD3D497FB934B52C39B24F54E6B961758A3D5C4606F87C163E86326D7</previousOutputValue><signatureValue>A33B1C710362FCD49F64E7EE2DE5DAA47CEC5B319B058A05D159F852C7715FE19AADDECEC5C578DAA934C7A6A9771CE4709D9C68592B6699A224A28E17895632B0FB749B279F9BC9AEF9E3B0F4001589D3FE705CE9AD6B5159A11D46F0252BD2851FE933183D00FC0D8DB7179C4AF73D4E6FA51CB7DF4E2D3666ACC9984D28E408BB44387DF41320C70ABD537754AC705D6425A5B22489B53779EF9B2E2CAE71FF5069F98BD2CB07B13E3C367EBDC4B5F12B61142930965AE9A7C4356E978D9C1DF8FE6F1FCC277382537F812F8B3BE773F74816DB5D2E139280ED7CD9235C32E8BB299C65ED4C6B6BBA05C08DECFC8A5E1DE5498337158C6D7D1ED5E59A1572</signatureValue><outputValue>6CFE1FAD91DD7B505897CFAA855C595D48F10F92647311C744427CA6F3068F9E33042810C248862B124E52FB80C12DDD96DCA99B51D4CEA92BB4B404E8A1767E</outputValue><statusCode>0</statusCode></record>
    When the NistRecord is constructed
    Then the randomNumber is 30783643464531464144393144443742353035383937434641413835354335393544343846313046393236343733313143373434343237434136463330363846394533333034323831304332343838363242313234453532464238304331324444443936444341393942353144344345413932424234423430344538413137363745
  
  Scenario: Badly formed XML
    Given XML string <?xml version="1.0" encoding="UTF-8" standalone="yes"?><record>
    Then creating the NistRecord throws an exception
    
  Scenario: XML that doesn't match the DTD
    Given XML string <?xml version="1.0" encoding="UTF-8" standalone="yes"?><record><a>A</a><b>B</b><c>C</c></record>
    Then creating the NistRecord throws an exception
    
  Scenario: toBinary matches required format
    Given XML file /home/greg/Projects/nist/src/nist1/tests/hadnist/rec.xml
    When the NistRecord is constructed
    Then the toBinary matches file /home/greg/Projects/nist/src/nist1/tests/hadnist/beacon.bin
    
  Scenario: XML that is verified by signature
    Given XML file /home/greg/Projects/nist/src/nist1/tests/hadnist/rec.xml
    When the NistRecord is constructed
    Then the isVerified is True

  Scenario: XML that is verified by signature
    Given XML file /home/greg/Projects/nist/src/nist1/tests/hadnist/rec.xml
    When the NistRecord is constructed
	And the NistRecord is altered
    Then the isVerified is False
