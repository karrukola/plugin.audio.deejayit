Feature: List of programs

Scenario: A show without speakers
  Given show ABC has no speakers announced
  When I open the list of programs
  Then show ABC is presented

Scenario: There are no shows
  Given the list of programs is empty
  When I open the list of programs
  Then error message TBD_#1 is shown

Scenario: Network connectivity issue
  Given there is a connectivity issue
  When I open the list of programs
  Then error message TBD_#2 is shown

Scenario: HTTP connectivity issue
  Given The backend returns error code <err_code>
  When I open the list of programs
  Then error message TBD_#3 is shown

  Examples:
  | err_code |
  | 400      |
  | 401      |
  | 404      |
  | 500      |
  | 501      |

Scenario: Parsing error
  Given the list of programs is not empty
  When the list of programs cannot be parsed
  Then error message TBD_#4 is shown
