#  messing around with python utilities for agile central / rally
#  use this file as a default main runner
#

import argparse
from datetime import date, datetime
from json import dumps

import chardet
import getpass
import logging
import pyral
import requests
import subprocess
import sys

from logging.config import fileConfig
from RallyClient import RallyClient, RALLY_ITEM_TYPES


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def create_sample_test_case(session):
    logger = logging.getLogger('workshop')
    logger.info('--- creating test case')
    workspace = session.client.getWorkspace()
    project = session.client.getProject()
    item_data = {"Name": "SAMPLE_TEST_CASE",
                 "Method": "Automated",
                 "Type": "Regression",
                 "Workspace": workspace.ref,
                 "Project": project.ref,
                 }
    new_test_case = session.create_test_case(item_data)
    return new_test_case


def create_sample_test_case_result(session, testcase_sample):
    logger = logging.getLogger('workshop')
    logger.info('--- creating test case result')
    workspace = session.client.getWorkspace()
    project = session.client.getProject()
    build_tested = "2021.00.00"
    #   date_sample = "2021-01-01 00:00:00"
    test_verdict = "Pass"

    build = build_tested
    run_date = dumps(datetime.now(), default=json_serial)
    #    run_date = date.today()
    verdict = test_verdict

    item_data = {"Workspace": workspace.ref,
                 "TestCase": testcase_sample.ref,
                 "Build": build_tested,
                 "Date": run_date,
                 "Verdict": verdict,
                 }
    new_test_case_result = session.create_test_case_result(item_data)


def create_sample_user_story(session):
    logger = logging.getLogger('workshop')
    logger.info('--- creating user story')
    item_data = {"Name": "SAMPLE_STORY"}
    new_story = session.create_user_story(item_data)


def display_rally_defects(session, limit):
    """

    :param session:
    :param limit:
    """
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally defects')
    defects = session.get_allowed_defects()

    if len(defects) == 0:
        logger.info('::: ')
        logger.info('::: ** NO Defects found ** ')
        logger.info('::: ')
    else:
        for index, defect in zip(range(limit), defects):
            name = defect.Name
            formatted_id = defect.FormattedID

            if defect.Iteration and defect.Iteration.Name:
                iteration = defect.Iteration.Name
            else:
                iteration = 'None'

            schedule_state = defect.ScheduleState

            logstring = '::::: ' + str(formatted_id).ljust(8) \
                        + ' :: ' + str(schedule_state).ljust(12) \
                        + ' :: ' + str(iteration).ljust(14) \
                        + ' :: ' + str(name)
            logger.info(logstring)


def display_rally_releases(session, limit):
    """

    :param session:
    """
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally releases')
    releases = session.get_allowed_releases()

    if len(releases) == 0:
        logger.info('::: ')
        logger.info('::: ** NO Releases found ** ')
        logger.info('::: ')
    else:
        for index, release in zip(range(limit), releases):
            # for story in stories:
            # storyDetails = story.details()

            name = release.Name
            formatted_id = release.FormattedID

            logstring = '::::: ' + str(formatted_id).ljust(8) \
                        + ' :: ' + str(name)
            logger.info(logstring)


def display_rally_projects(session, limit):
    """

    :param session:
    """
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally projects')
    projects = session.get_allowed_projects()

    if len(projects) == 0:
        logger.info('::: ')
        logger.info('::: ** NO Projects found ** ')
        logger.info('::: ')
    else:
        for index, project in zip(range(limit), projects):
            # for story in stories:
            # storyDetails = story.details()

            name = project.Name
            state = project.State

            logstring = '::::: ' + str(state).ljust(8) \
                        + ' :: ' + str(name)
            logger.info(logstring)


def display_rally_test_cases(session, limit):
    """

    :param session:
    :param limit:
    """
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally test cases')
    test_cases = session.get_allowed_test_cases()

    if len(test_cases) == 0:
        logger.info('::: ')
        logger.info('::: ** NO Test Cases found ** ')
        logger.info('::: ')
    else:
        for index, test_case in zip(range(limit), test_cases):
            name = test_case.Name
            formatted_id = test_case.FormattedID

            if test_case.TestFolder and test_case.TestFolder.Name:
                test_folder = test_case.TestFolder.Name
            else:
                test_folder = 'None'

            test_case_type = test_case.Type

            logstring = '::::: ' + str(formatted_id).ljust(8) \
                        + ' :: ' + str(test_case_type).ljust(12) \
                        + ' :: ' + str(test_folder).ljust(14) \
                        + ' :: ' + str(name)
            logger.info(logstring)


def display_rally_test_sets(session, limit):
    """

    :param session:
    :param limit:
    """
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally test sets')
    test_sets = session.get_allowed_test_sets()

    if len(test_sets) == 0:
        logger.info('::: ')
        logger.info('::: ** NO Test Sets found ** ')
        logger.info('::: ')
    else:
        for index, test_set in zip(range(limit), test_sets):
            name = test_set.Name
            formatted_id = test_set.FormattedID

            if test_set.Iteration.Name:
                iteration = test_set.Iteration.Name
            else:
                iteration = 'None'

            schedule_state = test_set.ScheduleState

            logstring = '::::: ' + str(formatted_id).ljust(8) \
                        + ' :: ' + str(schedule_state).ljust(12) \
                        + ' :: ' + str(iteration).ljust(14) \
                        + ' :: ' + str(name)
            logger.info(logstring)


def display_rally_user_stories(session, limit):
    """
    :param session:
    :param limit:
    """
    logger = logging.getLogger('workshop')
    logger.info('--- displaying rally user stories')
    stories = session.get_allowed_user_stories()

    if len(stories) == 0:
        logger.info('::: ')
        logger.info('::: ** NO User Stories found ** ')
        logger.info('::: ')
    else:
        for index, story in zip(range(limit), stories):
            # for story in stories:
            # storyDetails = story.details()

            name = story.Name
            formatted_id = story.FormattedID

            if story.Iteration and story.Iteration.Name:
                iteration = story.Iteration.Name
            else:
                iteration = 'None'

            schedule_state = story.ScheduleState

            logstring = '::::: ' + str(formatted_id).ljust(8) \
                        + ' :: ' + str(schedule_state).ljust(12) \
                        + ' :: ' + str(iteration).ljust(14) \
                        + ' :: ' + str(name)
            logger.info(logstring)


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


def initialize_logger():
    """

    :return:
    """
    #   TODO: switch to logging config file
    #   fileConfig('logging_config.ini')
    #   logger = logging.getLogger()

    logger = logging.getLogger('workshop')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('workshop.log', encoding='utf8')
    console_handler = logging.StreamHandler()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def initialize_rally_client(rally_auth, use_api, args):
    """

    :param rally_auth: will be either a dict of user creds or an api key depending on the use_api flag
    :param use_api: differentiate between the auth types
    :param args:
    :return:
    """
    logger = logging.getLogger('workshop')
    logger.info('::: initializing rally client')
    logger.info('::: use_api: ' + str(use_api))

    if args.rally_workspace:
        rally_workspace = args.rally_workspace
        logger.info('::: rally_workspace: ' + str(rally_workspace))
    else:
        rally_workspace = '2020'

    if args.rally_project:
        rally_project = args.rally_project
        logger.info('::: rally_project: ' + str(rally_project))
    else:
        rally_project = 'Project Sample'

    if use_api:
        # logger.info('::: *** CHECKING A HARDCODED API KEY? PLACE HERE ***')
        api_key = rally_auth
        # make sure we don't pass any api key value to the user creds
        rally_auth = None
    else:
        # rally_auth is the user creds
        # pass nothing for the api_key
        api_key = None
        rally_auth = rally_auth

    session = []
    session = RallyClient(rally_auth, api_key, ' '.join(rally_project), rally_workspace, logger, args.test)
    return session


def parse_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description='Query and Update Rally project data')
    parser.add_argument('--rally_project', '-rp', nargs='+', help="Target Rally project")

    # Optional arguments
    parser.add_argument('--api', '-api', help='access Rally via api key')
    parser.add_argument('--lastpass-rally-site-name', '-lpr',
                        help='Use LastPass site entry name with Rally credentials')
    parser.add_argument('--limit', '-l', help="Optional maximum limit of results")
    parser.add_argument('--rally_workspace', '-rw', nargs='+', help="Target Rally workspace")
    parser.add_argument('--test', '-t',
                        help='Show prospective changes without making updates to Rally',
                        action='store_true', default=False)

    args = parser.parse_args()
    return args


def prompt_for_auth(system):
    """Prompt for a username and password"""
    username = input(f"Please enter your {system} username:")
    password = getpass.getpass(f"Please enter your {system} password or API Token:")
    basic_auth = (username, password)
    return basic_auth


def get_limit(args):
    if args.limit:
        try:
            limit = int(args.limit)
        except:
            limit = 10
    return limit


def main():
    """

    :return:
    """
    # TODO: get settings from workshop.ini
    # TODO: write workshop.ini if it doesn't exist

    limit = 10
    logger = initialize_logger()

    logger.info('::: ')
    logger.info('::: starting workshop session :::')
    logger.info('::: ')

    logger.info('::: ')
    logger.info('::: parse workshop session arguments :::')
    args = parse_args()
    # logger.debug(args)
    logger.info('::: ')

    limit = get_limit(args)

    if args.api:
        # use an api key if supplied
        logger.info('::: args api found')
        use_api = True
        api_key = args.api
        # logger.info('::: ')
        # logger.info('::: api_key: '+str(api_key))
        session = initialize_rally_client(api_key, use_api, args)
    else:
        logger.info('::: args api NOT found, checking for creds')
        use_api = False
        if args.lastpass_rally_site_name:
            rally_auth = get_basic_auth_from_lastpass(args.lastpass_rally_site_name)
        else:
            rally_auth = prompt_for_auth('Rally')

        # logger.info('::: ')
        # logger.info('::: rally_auth: '+str(rally_auth))
        session = initialize_rally_client(rally_auth, use_api, args)

    logger.info('::: ')
    logger.info('::: Rally client object: ' + str(session))

    #   create_sample_user_story(session)
    #   testcase_sample = create_sample_test_case(session)
    #   create_sample_test_case_result(session, testcase_sample)

    display_rally_defects(session, limit)
    display_rally_projects(session, limit)
    display_rally_releases(session, limit)
    display_rally_test_cases(session, limit)
    display_rally_test_sets(session, limit)
    display_rally_user_stories(session, limit)
    # display_rally_user_story_sample(session,387227494600)

    item_data = {}

    logger.info('::: ')
    logger.info('::: ending workshop session   :::')
    logger.info('=================================')

    return 0


# ----------------------------------------
if __name__ == '__main__':
    result = main()
    sys.exit(0)
