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
        except:
            limit = 10
    return limit


def get_runtime_limit(args, config, logger):
    # limit = 77
    # logger.info('::: limit value ' + str(limit))

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

