Feature: List of episodes

Scenario: A show without speakers
  Given show ABC has no speakers announced
  When I play any episode of show ABC
  Then Radio Deejay is used as speaker
