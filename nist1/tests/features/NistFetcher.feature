Feature: Fetch random numbers from NIST
  In order to provide random numbers
  As developers
  We'll call web fetches on NistFetcher

  Scenario: Get the current random number
    Given the timestamp is set to 1419683040
    When fetching the current random number
    Then the random number is 5708409362382606887556487548526757915362676798533230764559356382425743225661137869365947767072826198761894329396335860841221562599775642613645590814357118L

  Scenario: Get a previous random number
    Given the timestamp is set to 1419683040
    When fetching the previous random number
    Then the random number is 8422865114288817677540700038601450828556732028598506761078720325183051928690858732424231132633517530721399108497350899737262406487800549867256742267791063L
    
  Scenario: Get the next random number
    Given the timestamp is set to 1419683040
    When fetching the next random number
    Then the random number is 8437671255843816546858896428525914898674611547282423379475381474628118087595309254746131096880466843604312344321194022011551808638439846132590309389840054L
  
  Scenario: Get the last record
    Given xxx
    When yyy
    Then zzz
  
  Scenario: Get the start of a chain
    Given the timestamp is set to 1419683040
    When fetching the start of the chain
    Then the random number is 8437671255843816546858896428525914898674611547282423379475381474628118087595309254746131096880466843604312344321194022011551808638439846132590309389840054L
  
