import sys

from pyral import Rally

RALLY_SERVER = 'rally1.rallydev.com'
RALLY_WORKSPACE = '2020'

RALLY_ITEM_TYPES = {
    'Defect': 'Defect',
    'UserStory': 'UserStory',
    'Task': 'Task'
}
RALLY_DEFECT_STATES = {
    'SUBMITTED': 'Submitted',
    'OPEN': 'Open',
    'FIXED': 'Fixed',
    'CLOSED': 'Closed'
}
RALLY_TASK_STATES = {
    'DEFINED': 'Defined',
    'IN_PROGRESS': 'In-Progress',
    'COMPLETED': 'Completed'
}
RALLY_SCHEDULED_STATES = {
    'DEFINED': 'Defined',
    'IN_PROGRESS': 'In-Progress',
    'COMPLETED': 'Completed',
    'ACCEPTED': 'Accepted'
}

class RallyClient:
    def __init__(self, basic_auth, project, logger, is_testing):
        """Instantiate and return a Rally client pointed at https://rally1.rallydev.com."""
        self.client = Rally(RALLY_SERVER, basic_auth[0], basic_auth[1], workspace=RALLY_WORKSPACE, project=project)
        self.log = logger
        self.is_testing = is_testing

    @staticmethod
    def get_value_from_response(entity, response):
        if response.errors:
            errors = "\n".join(response.errors)
            raise Exception(f'Error getting {entity}: {errors}')

        return response.next()

    @staticmethod
    def get_id(item):
        return getattr(item, 'FormattedID', None)

#


