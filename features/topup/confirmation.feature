@topup @regression @real
Feature: صفحه‌ی تأیید

  Background:
    Given I am logged in
    And I open the top-up page

  Scenario Outline: TC-07 The confirmation page shows mobile, amount and sim type
    When I type the "valid" mobile number
    And I press the buy button
    And I choose the "<sim>" sim type
    And I type the "default" amount
    And I press continue
    Then I should reach the confirmation page
    And the confirmation shows my mobile, the "default" amount and the "<sim>" sim type

    Examples:
      | sim       |
      | credit    |
      | permanent |
