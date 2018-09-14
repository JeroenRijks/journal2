Feature: tag functionality
  I want to test whether I can make and edit tags.

  Background:
    Given I visit "/tag_list/"

  Scenario: Editing an existing tag
    When I click the link with text "API"
    And I fill in "name" with "Java"
    And I press "Submit"
    Then I should not see "API"
    And I should see "Java"

  Scenario: Creating a new tag
    When I click the link with text "Create a tag"
    And I fill in "name" with "NodeJS"
    And I press "Submit"
    Then I should see "NodeJS"
