#  python workshop utils for agile central / rally
#  utilities general catchall file
#

import configparser
import logging
from datetime import date, datetime


def get_limit(args):
    if args.limit:
        try:
            limit = int(args.limit)
        except ValueError:
            limit = 10
    return limit


def get_project(args):
    if args.rally_project:
        project = args.rally_project
    return project


def get_sitename(args):
    if args.sitename:
        sitename = args.sitename
    return sitename


def get_test(args):
    test = False
    if args.test:
        test = True
    return test


def get_workspace(args):
    if args.rally_workspace:
        workspace = args.rally_workspace
    return workspace


def get_runtime_limit(args, config, logger):
    if args.limit:
        limit = get_limit(args)
        logger.info(':::     limit value ' + str(limit) + ' from args')
    elif config['default']['limit']:
        limit = int(config['default']['limit'])
        logger.info(':::     limit value ' + str(limit) + ' from config')
    else:
        logger.info(':::     limit value not found, default set')
        limit = 88
    return limit


def get_runtime_test(args, config, logger):
    test = False

    if args.test:
        test = args.test
        logger.info(':::     test value ' + str(test) + ' from args')
    elif config['default']['test']:
        test = str(config['default']['test'])
        logger.info(':::     test value ' + str(test) + ' from config')
    else:
        logger.info(':::     test value not found, default set')
        test = True
    return test


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def config_load():
    config = configparser.ConfigParser()
    config['default'] = {}
    configfile = 'workshop.ini'

    try:
        config.read(configfile)
    except FileNotFoundError:
        config['default'] = {
            "api": "",
            "limit": "99",
            "test": "True",
        }
    return config