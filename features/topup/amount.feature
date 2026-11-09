@topup @regression @real
Feature: مبلغ شارژ - مقدار مرزی

  Background:
    Given I am logged in
    And I open the top-up page
    And the form is filled up to the amount step

  Scenario Outline: TC-05 Amounts outside the allowed range cannot continue
    When I type the "<case>" amount
    Then I should not be able to continue

    Examples:
      | case      |
      | below_min |
      | above_max |

  Scenario: TC-12 The bonus charge can be turned on
    When I turn on the bonus charge
    And I press continue
    Then I should reach the confirmation page
    And the confirmation shows the bonus charge

  Scenario Outline: TC-06 Amounts exactly on the limits are accepted
    When I type the "<case>" amount
    And I press continue
    Then I should reach the confirmation page

    Examples:
      | case |
      | min  |
      | max  |
