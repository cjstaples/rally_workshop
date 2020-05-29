#  messing around with python utilities for agile central / rally
#  use this file as a default main runner
#

import argparse
import logging
import sys

from logging.config import fileConfig
from RallyClient import RallyClient, RALLY_ITEM_TYPES


def display_rally_test_cases(session):
    logger = logging.getLogger('workshop')
    logger.info('-- displaying rally test cases --')
    pass


def display_rally_test_sets(session):
    logger = logging.getLogger('workshop')
    logger.info('-- displaying rally test sets --')
    pass


def display_rally_user_stories(session):
    logger = logging.getLogger('workshop')
    logger.info('-- displaying rally user stories --')
    pass


def initialize_rally_client():
    logger = logging.getLogger('workshop')
    logger.info('-- initializing rally client --')
    session = []
    return session


def main():
    print('(workshop) main::::::')
    print()

    #   TODO: user options input
    #

    logger = initialize_logger()

    logger.info('::: ')
    logger.info('::: starting workshop session :::')
    logger.info('::: ')

    session = initialize_rally_client()

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

# ----------------------------------------
if __name__ == '__main__':
    result = main()
    sys.exit(0)
