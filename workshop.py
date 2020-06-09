#  messing around with python utilities for agile central / rally
#  use this file as a default main runner
#

import argparse
import chardet
import getpass
import logging
import pyral
import requests
import subprocess
import sys

from logging.config import fileConfig
from RallyClient import RallyClient, RALLY_ITEM_TYPES


def display_rally_releases(session):
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally releases')
    response = session.get('Release', fetch="Project,Name,ReleaseStartDate,ReleaseDate",
                         order="ReleaseDate")
    for release in response:
        rlsStart = release.ReleaseStartDate.split('T')[0]   # just need the date part
    rlsDate = release.ReleaseDate.split('T')[0]             # ditto
    logger.info('Project,Name,ReleaseStartDate,ReleaseDate')
    logger.info(release.Project.Name, release.Name, rlsStart, rlsDate)
    pass


def display_rally_test_cases(session):
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally test cases')
    pass


def display_rally_test_sets(session):
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally test sets')
    pass


def display_rally_user_stories(session):
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally user stories')
    stories = session.get_allowed_values('UserStory')
    for story in stories:
        # storyDetails = story.details()

        name = story.Name
        formatted_id = story.FormattedID
        try:
            iteration = story.Iteration.Name
        except:
            iteration = 'None'
        schedule_state = story.ScheduleState

        logstring = '::::: '+str(formatted_id).ljust(8)\
                    + ' :: '+str(schedule_state).ljust(12)\
                    + ' :: '+str(iteration).ljust(14)\
                    + ' :: '+str(name)
        logger.info(logstring)
    pass

def initialize_rally_client(rally_auth, args):
    logger = logging.getLogger('workshop')
    logger.info('--- initializing rally client')

    session = []
    session = RallyClient(rally_auth, ' '.join(args.rally_project), logger, args.test)
    return session


def parse_args():
    parser = argparse.ArgumentParser(description='Query and Update Rally project data')
    parser.add_argument('--rally_project', '-rp', nargs='+', help="Target Rally project")

    # Optional arguments
    parser.add_argument('--lastpass-rally-site-name', '-lpr',
                        help='Use LastPass site entry name with Rally credentials')
    parser.add_argument('--test', '-t',
                        help='Show prospective changes without making updates to Rally',
                        action='store_true', default=False)

    args = parser.parse_args()
    return args


def main():
    print('(workshop) main::::::')
    print()

    #   TODO: user options input
    #

    logger = initialize_logger()

    logger.info('::: ')
    logger.info('::: starting workshop session :::')
    logger.info('::: ')

    logger.info('::: ')
    logger.info('::: parse workshop session arguments :::')
    args = parse_args()
    logger.debug(args)
    logger.info('::: ')

    if args.lastpass_rally_site_name:
        rally_auth = get_basic_auth_from_lastpass(args.lastpass_rally_site_name)
    else:
        rally_auth = prompt_for_auth('Rally')

    rally_client = RallyClient(rally_auth, ' '.join(args.rally_project), logger, args.test)

    session = initialize_rally_client(rally_auth, args)
    logger.debug(session)

    # display_rally_releases(session)
    # display_rally_user_story_sample(session,387227494600)
    display_rally_user_stories(session)
    display_rally_test_cases(session)
    display_rally_test_sets(session)

    logger.info('::: ')
    logger.info('::: ending workshop session   :::')
    logger.info('=================================')

    print()
    print('(workshop) end:::::::')

    return 0

def initialize_logger():

#   TODO: switch to logging config file
#   fileConfig('logging_config.ini')
#   logger = logging.getLogger()

    logger = logging.getLogger('workshop')
    logger.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler('workshop.log', encoding='utf8')
    consoleHandler = logging.StreamHandler()
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger

def get_basic_auth_from_lastpass(site_name):
    """Use the lastpass cli to yield the username and password from the provided site name

    The lastpass-python lib is sketchy and not feature complete, so use the lastpass cli instead
    """
    basic_auth = []
    for field_name in ['username', 'password']:
        command = "lpass show {site_name} --{field_name}".format(site_name=site_name, field_name=field_name)
        output = subprocess.check_output(command, shell=True)
        if field_name == 'username':
            output = output.lower()
        basic_auth.append(output.decode().strip())

    return tuple(basic_auth)

def prompt_for_auth(system):
    """Prompt for a username and password"""
    username = input(f"Please enter your {system} username:")
    password = getpass.getpass(f"Please enter your {system} password or API Token:")
    basic_auth = (username, password)
    return basic_auth

# ----------------------------------------
if __name__ == '__main__':
    result = main()
    sys.exit(0)
