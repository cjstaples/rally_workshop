from pyral import Rally

RALLY_SERVER = 'rally1.rallydev.com'

# Change to this for work in Production
# RALLY_WORKSPACE = '2020'

# Change this for work in the Rally Sandbox
# RALLY_WORKSPACE = 'Workspace 1'

RALLY_WORKSPACE = '2020'

RALLY_ITEM_TYPES = {
    'Defect': 'Defect',
    'TestCase': 'TestCase',
    'TestCaseResult': 'TestCaseResult',
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
    """
    Rally Client base
    """
    def __init__(self, basic_auth, api_key, project, workspace, logger, is_testing):
        """
        Instantiate and return a Rally client pointed at https://rally1.rallydev.com.
        """
        self.log = logger
        self.is_testing = is_testing
        # logger.info('::: ')
        # logger.info('::: api_key: '+str(api_key))

        if api_key:
            logger.info('::: authenticate via API key')
            self.client = Rally(RALLY_SERVER, apikey=api_key, workspace=workspace, project=project)
        else:
            logger.info('::: authenticate via user CREDS')
            self.client = Rally(RALLY_SERVER, user=basic_auth[0], password=basic_auth[1], workspace=workspace, project=project)

        # self.client = Rally(RALLY_SERVER, user=basic_auth[0], password=basic_auth[1], workspace=RALLY_WORKSPACE, project=project)

    @staticmethod
    def get_value_from_response(entity, response):
        if response.errors:
            errors = "\n".join(response.errors)
            raise Exception(f'Error getting {entity}: {errors}')

        return response.next()

    @staticmethod
    def get_id(item):
        return getattr(item, 'FormattedID', None)

    @staticmethod
    def get_oid(item):
        return getattr(item, 'ObjectID', None)

    @staticmethod
    def get_notes(item):
        return getattr(item, 'Notes', None)

    def get_item(self, item_id, item_type):
        response = self.client.get(item_type, fetch=True, query=f'FormattedID = {item_id}')
        return self.get_value_from_response(item_type, response)

    # TODO:  This probably is non-functional. Fix or remove.
    def get_iteration(self, item_id):
        return self.get_item(item_id, RALLY_ITEM_TYPES['Iteration'])

    def get_user_story(self, item_id):
        return self.get_item(item_id, RALLY_ITEM_TYPES['UserStory'])

    def get_defect(self, item_id):
        return self.get_item(item_id, RALLY_ITEM_TYPES['Defect'])

    def get_task(self, item_id):
        return self.get_item(item_id, RALLY_ITEM_TYPES['Task'])

    def get_user(self, username):
        if not username:
            return None

        user = self.client.getUserInfo(username=username)
        if isinstance(user, list):
            return user[0]
        else:
            return user

    def get_rally_link(self, item_type, item):
        rally_id = self.get_oid(item)
        return f'https://{RALLY_SERVER}/#/detail/{item_type.lower()}/{rally_id}?fdp=true'

    def get_rally_user_story_link(self, item):
        return self.get_rally_link(RALLY_ITEM_TYPES['UserStory'].lower(), item)

    def get_rally_defect_link(self, item):
        return self.get_rally_link(RALLY_ITEM_TYPES['Defect'].lower(), item)

    def get_rally_task_link(self, item):
        return self.get_rally_link(RALLY_ITEM_TYPES['Task'].lower(), item)

#   General purpose get, usable for the following values of entity:
#       Story, UserStory, Defect, DefectSuite, Task, TestCase, TestSet, PortfolioItem; Iteration, Milestone, Release, Project
    def get_allowed_values(self, entity):
        response = self.client.get(entity)
        return [item for item in response]

    def get_allowed_defects(self):
        return self.get_allowed_values('Defect')

    def get_allowed_iterations(self):
        return self.get_allowed_values('Iteration')

    def get_allowed_milestones(self):
        return self.get_allowed_values('Milestone')

    def get_allowed_releases(self):
        return self.get_allowed_values('Release')

    def get_allowed_projects(self):
        return self.get_allowed_values('Project')

    def get_allowed_test_cases(self):
        return self.get_allowed_values('TestCase')

    def get_allowed_test_sets(self):
        return self.get_allowed_values('TestSet')

    def get_allowed_user_stories(self):
        return self.get_allowed_values('UserStory')

    @staticmethod
    def set_id(item, formatted_id):
        item.update({
            'FormattedID': formatted_id
        })

    @staticmethod
    def set_name(item, name):
        item.update({
            'Name': name
        })

    @staticmethod
    def set_description(item, description):
        item.update({
            'Description': description
        })

    @staticmethod
    def set_plan_est(item, plan_est):
        item.update({
            'PlanEstimate': plan_est
        })

    @staticmethod
    def set_scheduled_state(item, scheduled_state):
        item.update({
            'ScheduleState': scheduled_state
        })

    @staticmethod
    def set_state(item, state):
        item.update({
            'State': state
        })

    @staticmethod
    def set_priority(item, priority):
        item.update({
            'Priority': priority
        })

    @staticmethod
    def set_blocked(item, is_blocked):
        item.update({
            'Blocked': is_blocked
        })

    @staticmethod
    def set_notes(item, notes):
        item.update({
            'Notes': notes
        })

    @staticmethod
    def set_jira_linking_fields(item, jira_key, jira_link):
        item.update({
            'JiraKey': jira_key,
            'JiraLink': jira_link
        })

    @staticmethod
    def set_parent(item, parent):
        if parent:
            item.update({
                'WorkProduct': parent.ref
            })

    def set_iteration(self, item, iteration):
        allowed_iterations = self.get_allowed_iterations()

        if not allowed_iterations:
            self.log.debug('RALLY: No Allowed Iterations found')
            return

        matching_iterations = [allowed_iteration for allowed_iteration in allowed_iterations
                               if allowed_iteration.Name == iteration]

        if not len(matching_iterations):
            self.log.debug(f'RALLY: Iteration {iteration} not in Allowed Iteration Values')
            return

        item.update({
            'Iteration': matching_iterations[0].ref
        })

    def set_owner(self, item, owner):
        owner = self.get_user(owner)
        if owner:
            item.update({
                'Owner': owner.ref
            })

    def set_submitted_by(self, item, submitter):
        submitter = self.get_user(submitter)
        if submitter:
            item.update({
                'SubmittedBy': submitter.ref
            })

    def create_item(self, item_type, item_data):
        if not self.is_testing:
            new_item = self.client.create(item_type, item_data)
            self.log.debug(f"RALLY CREATED {item_type}: {getattr(new_item, 'FormattedID', None)}")
        else:
            new_item = {
                'FormattedID': 'FAKE-123'
            }
            self.log.debug(f"RALLY CREATED {item_type}: {new_item['FormattedID']}")

        self.log.debug(f'    with values: {item_data}')
        return new_item

#   Requires DICT item_data:
#
#
#
    def create_user_story(self, item_data):
        return self.create_item(RALLY_ITEM_TYPES['UserStory'], item_data)

    def create_defect(self, item_data):
        return self.create_item(RALLY_ITEM_TYPES['Defect'], item_data)

    def create_task(self, item_data):
        return self.create_item(RALLY_ITEM_TYPES['Task'], item_data)

    def create_test_case(self, item_data):
        return self.create_item(RALLY_ITEM_TYPES['TestCase'], item_data)

    def create_test_case_result(self, item_data):
        return self.create_item(RALLY_ITEM_TYPES['TestCaseResult'], item_data)

    def update_item(self, item_type, item_data):
        if not self.is_testing:
            updated_item = self.client.update(item_type, item_data)
            self.log.debug(f"RALLY UPDATED {item_type}: {getattr(updated_item, 'FormattedID', None)}")
        else:
            updated_item = item_data
            self.log.debug(f"RALLY UPDATED {item_type}: {updated_item['FormattedID']}")

        self.log.debug(f'    with values: {item_data}')
        return updated_item

    def update_user_story(self, item_data):
        return self.update_item(RALLY_ITEM_TYPES['UserStory'], item_data)

    def update_defect(self, item_data):
        return self.update_item(RALLY_ITEM_TYPES['Defect'], item_data)

    def update_task(self, item_data):
        return self.update_item(RALLY_ITEM_TYPES['Task'], item_data)

    def add_milestones(self, item, milestones):
        allowed_milestones = self.get_allowed_milestones()

        valid_milestones = []
        for allowed_milestone in allowed_milestones:
            if allowed_milestone.Name in milestones:
                valid_milestones.append(allowed_milestone)

        if not self.is_testing:
            self.client.addCollectionItems(item, valid_milestones)

        self.log.debug(f'RALLY ADDING Milestones {valid_milestones}')

    def add_discussion(self, item, posts):
        oid = self.get_oid(item)

        for post in posts:
            discussion_data = {"Artifact": oid, "Text": post}
            if not self.is_testing:
                self.client.create('ConversationPost', discussion_data)

            self.log.debug(f'RALLY ADDING Discussion Post {post}')

    def add_attachment(self, item, attachment):
        # TODO (https://pyral.readthedocs.io/en/latest/interface.html#addAttachment)
        self.log.debug('RALLY ADDING Attachment')

#


