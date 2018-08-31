Feature: homepage
  I want to test the functionality of the home page, which
  displays all of my resources. The tests are
  tag filtering, created by and last updated by (anon and auth),
  and delete

  Background:
    Given I visit "/"

  Scenario: Filtering my resources by tags.

    When I click the link with text "User authentication"
    Then I should see "hasattr"
    And I should not see "behaving"
    And I should see "authentication"
    And I should not see "Feature"

  Scenario: Checking TwoScoops created_by and last_edited_by for anonymous users
    Given an anonymous user
    When I add a new resource called Two Scoops
    Then I should see "Two Scoops"
    And I should see "Anonymous"
    And I should see "Unedited tip"
    And I should not see an element with the css selector ".created-text"

  Scenario: Checking created_by Enki and last_edited_by for authorised users
    Given "tester" as the persona
    And I log in to the admin interface
    When I add a new resource called Enki
    # TODO I want to see Enki three times
    Then I should see "Enki"
    And I should see an element with the css selector ".created-text"

  Scenario: Deleting tips
    When I press "5"
    Then I should not see "hasattr"
