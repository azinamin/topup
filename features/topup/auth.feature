@topup @regression @real @no_auth
Feature: دسترسی بدون لاگین

  Scenario: TC-08 A visitor without a session is asked to log in
    Given I have no session
    When I open the DigiPay app
    Then I should see the login page
