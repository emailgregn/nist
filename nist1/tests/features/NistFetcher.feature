Feature: Fetch random numbers from NIST
  In order to provide random numbers
  As users
  We'll implement web fetches

  Scenario: Get the current random number
    Given the timestamp is 1419683040
    When fetching the current random number
    Then the random number is 0001

  Scenario: Get a previous random number
    Given the timestamp is 1419683040
    When fetching the previous random number
    Then the random number is 0001
    
  Scenario: Get the next random number
    Given the timestamp is 1419683040
    When fetching the next random number
    Then the random number is 0001
  
  Scenario: Get the last record
    Given xxx
    When yyy
    Then zzz
  
  Scenario: Get the start of a chain
    Given the timestamp is 1419683040
    When fetching the start of the chain
    Then the random number is 0001
  
