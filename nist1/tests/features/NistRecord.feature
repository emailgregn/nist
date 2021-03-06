Feature: XML from NIST is parsed into a nist1.nistRecord
  In order to accept data from NIST
  As a developer
  nist1 can parse XML into a NistRecord class
  
  Scenario: Well formed XML
    Given XML string <?xml version="1.0" encoding="UTF-8" standalone="yes"?><record><version>Version 1.0</version><frequency>60</frequency><timeStamp>1400878200</timeStamp><seedValue>C4E0E995111B9986658709F759E57650859DB3DA5330F007CE9732BA2E30B1F8475E3882796DA835CBDBA6FD2D4F5345B4BB46A5F60AAC249C7D4E4670881E71</seedValue><previousOutputValue>D24EEBA206D05196C0ADC3DA2F56EA295CDD4D1C3E4D5265CCF762392CF8A4BCABA295DB441E6B9E661727FB1C37CE9DEC6D9465513356A13F515EC0CDB82D2C</previousOutputValue><signatureValue>AF8332249B8E7EBEDD0326740583FF2280FE788167F2E76C172A38858BFD3A346F5C87D879BC790BEE104CD96B5743B3E2C6B5E244C880C9362B85112C69B309277A1A97F970CC475864CF56A8A8430AFF61A8D89B2B9F537BC293E0944DAA054B77390A0D8E7844C25BDF8164D34D58C1E8DE503B62E55B311798072E276FE56F5C294FA76BE3A2BC47576BE5804A9AAC8307066C613C8507A459C898B25B502B975E5B17EAEF74F219C5C3C979E7188DDC473901EADA236C6127ABF72A2C258E95F90A4BF6F67EFAD8D66DC19C169B543B3F0F12A2D520A7E6489CE2509930592D50CD663961C10F1F2584BD89F79FBA0C0980F00D062F1ECC51A339E6B11F</signatureValue><outputValue>68ACCF41E370AA4AC3F83CCF7DA56AE8E87AA6EE491E68C2A92C661D1267697AA21FDFAE17D0701A49AA9EAA74016B4A4AD1DDD45D62961141E9C7C8FBD1FA6A</outputValue><statusCode>0</statusCode></record>
    When the NistRecord is constructed
    Then the random number is 5482276553960377390613834276659670067972162379661235973281894806239895664966351992125626835263870607450924277251933949060754086239032517081639650436708970
    And the previous number is 11014738531943671592440866877122142518227539251120013691465037278225055492811474730697927261222458534805709747222060342153375210166938982978255357440699692
    And the seed value is 10311367086279528437873386155395087585328990943162764605414816726771655181293766035424180550299293945559617538942619513198109005449400068500882938493673073
    And the timestamp is 1400878200
    And the signature matches file tests/hadnist/beacon.sig
    

  
  Scenario: Badly formed XML
    Given XML string <?xml version="1.0" encoding="UTF-8" standalone="yes"?><record>
    Then creating the NistRecord throws an exception
    
  Scenario: XML that doesn't match the DTD
    Given XML string <?xml version="1.0" encoding="UTF-8" standalone="yes"?><record><a>A</a><b>B</b><c>C</c></record>
    Then creating the NistRecord throws an exception
    
  Scenario: toBinary matches required format
    Given XML file tests/hadnist/rec.xml
    When the NistRecord is constructed
    Then the toBinary matches file tests/hadnist/beacon.bin

  Scenario: Signature matches required format
    Given XML file tests/hadnist/rec.xml
    When the NistRecord is constructed
    Then the signature matches file tests/hadnist/beacon.sig

   
  Scenario: XML that is verified by signature
    Given XML file tests/hadnist/rec.xml
    When the NistRecord is constructed
    Then the isVerified is True

  Scenario: XML that is not verified by signature
    Given XML string <?xml version="1.0" encoding="UTF-8" standalone="yes"?><record><version>Version 1.0</version><frequency>60</frequency><timeStamp>1400878200</timeStamp><seedValue>C4E0E995111B9986658709F759E57650859DB3DA5330F007CE9732BA2E30B1F8475E3882796DA835CBDBA6FD2D4F5345B4BB46A5F60AAC249C7D4E4670881E71</seedValue><previousOutputValue>99999999</previousOutputValue><signatureValue>AF8332249B8E7EBEDD0326740583FF2280FE788167F2E76C172A38858BFD3A346F5C87D879BC790BEE104CD96B5743B3E2C6B5E244C880C9362B85112C69B309277A1A97F970CC475864CF56A8A8430AFF61A8D89B2B9F537BC293E0944DAA054B77390A0D8E7844C25BDF8164D34D58C1E8DE503B62E55B311798072E276FE56F5C294FA76BE3A2BC47576BE5804A9AAC8307066C613C8507A459C898B25B502B975E5B17EAEF74F219C5C3C979E7188DDC473901EADA236C6127ABF72A2C258E95F90A4BF6F67EFAD8D66DC19C169B543B3F0F12A2D520A7E6489CE2509930592D50CD663961C10F1F2584BD89F79FBA0C0980F00D062F1ECC51A339E6B11F</signatureValue><outputValue>68ACCF41E370AA4AC3F83CCF7DA56AE8E87AA6EE491E68C2A92C661D1267697AA21FDFAE17D0701A49AA9EAA74016B4A4AD1DDD45D62961141E9C7C8FBD1FA6A</outputValue><statusCode>0</statusCode></record>
    When the NistRecord is constructed
    Then the isVerified is False

  Scenario: Can verify the lastRecord

  Scenario: Can verify the startChainRecord

  Scenario: Securely walk from startChainRecord to lastRecord

  Scenario: startChainRecord == lastRecord handled

  Scenario: The status code value:
            0 - Chain intact, values all good
            1 - Start of a new chain of values, previous hash value will be all zeroes
            2 - Time between values is greater than the frequency, but the chain is still intact