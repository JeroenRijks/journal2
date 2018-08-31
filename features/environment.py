from selenium import webdriver
from behaving import environment as benv
from behaving.web.steps import *
from behaving.mail.steps import *
from behaving.personas.steps import *
import os

PERSONAS = {
    'admin': dict(username='admin', password='admin',),
    'tester': dict(username='tester', password='password',),
}

# Communal code for posting tips
# TIPS = {
#     'two_scoops': dict(tip_name='Two Scoops', tip='Read Two Scoops of Django'),
#     'enki': dict(tip_name='enki', tip='Download the Enki app'),
# }

# override with -Dkey=value
config = {
    'base_url': 'http://localhost:8000',
    'headless': False,
    'remote': False,
}


def before_all(context):
    config.update(context.config.userdata)

    context.default_browser = 'chrome'
    context.single_browser = True

    context.base_url = config['base_url']
    benv.before_all(context)


def after_all(context):

    # Explicitly quits the browser, otherwise it won't once tests are done
    # context.browser.quit()
    pass


def before_feature(context, feature):
    benv.before_feature(context, feature)


def after_feature(context, feature):
    benv.after_feature(context, feature)


def before_scenario(context, scenario):
    benv.before_scenario(context, scenario)
    context.personas = PERSONAS
    # context.tips = TIPS       Communal code for posting tips
    context.execute_steps(u'''
       Given a browser
    ''')


def after_scenario(context, scenario):
    benv.after_scenario(context, scenario)
