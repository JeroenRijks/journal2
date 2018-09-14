Feature: navbar
  I want to test all the nav bar options.
  These are links to different views depending
  on whether the user is authenticated or not.


  Background:
    Given I visit "/"

  Scenario: 'Create a tip' should direct me to the tip edit page.

    Given an anonymous user
    When I click the link with text that contains "Create a tip"
    Then the browser's url should be "/tip_edit/"

  Scenario: Nav bar authentication should show correctly when I am anonymous
    Given an anonymous user
    Then I should see "Login"
    And I should see "Register"
    And I should not see "Logout"
    And I should not see "Welcome"

  Scenario: Nav bar authentication should show correctly when I am authenticated
    Given "tester" as the persona
    And I log in to the admin interface
    Then I should not see "Login"
    And I should not see "Register"
    And I should see "Logout"
    And I should see "Welcome"

#     Examples: links
#      |link         |destination|
#      |List of tips |/resources/|
#      |Create a tip |/tip_edit/ |
#      |List of tips |/tag_list/ |
#      |List of tips |/tag_edit/ |
#      |Register     |/register/ |
#      |Login        |/login/    |
#      |Logout       |/logout/   |
