@topup @mocked
Feature: رفتار برنامه هنگام خطای سرور (پاسخ API جعلی است؛ تراکنش واقعی ساخته نمی‌شود)

  Background:
    Given I am logged in
    And I open the top-up page

  Scenario Outline: TC-09 A failing order API shows an error and never opens the bank
    Given the order API fails with status "<status>"
    And a valid top-up form
    When I submit the order
    Then I should see an error message
    And I should not be on the bank page

    Examples:
      | status |
      | 400    |
      | 500    |
      | 503    |

  Scenario: TC-10 A network failure shows an error and never opens the bank
    Given the order API connection fails
    And a valid top-up form
    When I submit the order
    Then I should see an error message
    And I should not be on the bank page

  Scenario: TC-11 Double-clicking pay does not send the order twice
    Given the order API is slow and fails with status "500" after "3000" ms
    And a valid top-up form
    When I double-click the pay button
    Then the order API should be called at most 1 time
