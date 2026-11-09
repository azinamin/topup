@topup @regression @real
Feature: فرم خرید شارژ - شماره، اپراتور و نوع سیم‌کارت

  Background:
    Given I am logged in
    And I open the top-up page

  Scenario Outline: TC-01 Operator is selected from the mobile prefix
    When I type my number with prefix "<prefix>"
    Then the operator "<operator>" should be selected

    Examples:
      | prefix | operator |
      | 0912   | mci      |
      | 0935   | mtn      |
      | 0921   | rightel  |

  Scenario Outline: TC-02 Invalid mobile numbers keep the buy button disabled
    When I type the "<case>" mobile number
    Then the buy button should be disabled

    Examples:
      | case       |
      | short      |
      | bad_prefix |
      | letters    |
      | empty      |

  Scenario: TC-03 A valid mobile number enables the buy button
    When I type the "valid" mobile number
    Then the buy button should be enabled

  Scenario: TC-04 The sim type sheet offers permanent, credit and data
    When I type the "valid" mobile number
    And I press the buy button
    Then I should see the sim types
