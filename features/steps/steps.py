from behave import given, when, then
import time


@given(u'an anonymous user')
def step_impl(context):
    pass


@given(u'I log in to the admin interface')
def step_impl(context):
    context.execute_steps(u'''
        When I visit "login/"
        And I fill in "username" with "$username"
        And I fill in "password" with "$password"
        And I press "Submit"
    ''')


@when(u'I wait for 1 second')
def step_impl(context):
    time.sleep(1)


@when(u'I add a new resource called Two Scoops')
def step_impl(context):
    context.execute_steps(u'''
        When I click the link with text that contains "Add a new tip"
        And I fill in "name" with "Two Scoops"
        And I fill in "tip" with "Read Two Scoops of Django"
        And I press "Submit"
    ''')


@when(u'I add a new resource called Enki')
def step_impl(context):
    context.execute_steps(u'''
        When I click the link with text that contains "Add a new tip"
        And I fill in "name" with "Enki"
        And I fill in "tip" with "Download the Enki app"
        And I press "Submit"
    ''')

# Check 5th column (td) of last row (tr) in html, see if it says tester
# @step(u'the last tip should have a created by value')
# def step_impl(context):
#     ???

# @step(u'I add a new resource called "{name}"')  # Communal code for posting tips
# def step_impl(context, name):
#
#     # if name not in context.tips:
#     #     context.tips[name] = Tip()
#     context.tips = context.tips[name]
#     single_browser = hasattr(context, 'single_browser')
#     if hasattr(context, 'browser'):
#         if single_browser and hasattr(context, 'is_connected'):
#             return
#     context.execute_steps('Add resource "%s"' % name)
#     if single_browser:
#         context.is_connected = True
#
#
# @step(u'Add resource "{name}"')
# def step_impl(context, name):
#     context.execute_steps(u'''
#         When I click the link with text that contains "Add a new tip"
#         And I fill in "name" with "$tip_name"
#         And I fill in "tip" with "$tip"
#         And I press "Submit"
#     ''')
#
