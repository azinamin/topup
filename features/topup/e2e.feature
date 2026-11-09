@topup @e2e @real @smoke
Feature: خرید شارژ - سناریوی اصلی (اجباری)

  Scenario: Cancel the payment at the bank and see a failed receipt
    Given I am logged in
    When I open the top-up page
    And I type the "valid" mobile number
    Then the operator of my number should be selected
    When I press the buy button
    And I choose the "credit" sim type
    And I type the "default" amount
    And I press continue
    Then I should reach the confirmation page
    And the confirmation shows my mobile, the "default" amount and the "credit" sim type
    When I choose the internet gateway and pay
    Then I should be on the bank page
    When I cancel on the bank page
    Then I should be back in DigiPay
    And I should see the failed receipt with the "default" amount and a tracking code
