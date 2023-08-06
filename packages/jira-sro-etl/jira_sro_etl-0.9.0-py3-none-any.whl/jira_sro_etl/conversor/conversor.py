from jiraX import factories as factory
from sro_db.application import factories
from sro_db.model import factories as factories_model
from datetime import datetime
from functools import lru_cache
from pprint import pprint

class Conversor():

    def __init__(self, organization, data):
        self.organization = organization
        self.data = data
        self.issue_apl = factory.IssueFactory(user=data['user'], apikey=data['key'], server=data['url'])
        self.board_apl = factory.BoardFactory(user=data['user'], apikey=data['key'], server=data['url'])

    def date_formater(self, date_string):
        """Receive date in YYYY-MM-DD T HH:MM:SS and return datetime

        Can receive date with more details like hour, minute and second, but all info
        after day is ignored

		Args:
			date_string (str/NoneType): string YYYY-MM-DD T HH:MM:SS or None

		Returns:
			datetime/NoneType: Formated date or None if param was None
		"""
        if date_string:
            return datetime.strptime(date_string.split('.')[0], '%Y-%m-%dT%H:%M:%S')
        return None

    @lru_cache(maxsize=20)
    def __find_status_from_boardId(self, board_id):
        raw = self.board_apl.get_config(board_id)
        columns_list = raw['columnConfig']['columns']
        status_ids_list = [_dict['statuses'][0]['id'] for _dict in columns_list] 
        return status_ids_list

    def __find_on_changelog_list(self, ids_list, _list):
        result = [(None,None),(None,None),(None,None)]
        try:
            for changelog in _list:
                for item in changelog['items']:
                    try:
                        if(item['field'] == 'status' and item['to'] in ids_list):
                            result[ids_list.index(item['to'])] = (self.date_formater(changelog['created']), changelog['author']['accountId'])
                    except Exception as e:
                        pass   
        except Exception as e:
            pass
        return result

    def __find_on_changelog(self, issue, ids_list):
        first_try = self.__find_on_changelog_list(ids_list, issue.raw['changelog']['histories'])
        if len([x for x,y in first_try if x is not None]) == len(ids_list):
            return first_try
        second_try = self.__find_on_changelog_list(ids_list, self.issue_apl.get_changelog(issue.key)['values'])
        return second_try

    def find_activated_resolved_closed(self, issue):
        try:
            board_id = issue.raw['fields']['customfield_10018'][-1]['boardId']
            status_ids = self.__find_status_from_boardId(board_id)
            actual_status_index = status_ids.index(issue.raw['fields']['status']['id'])
            len_status = len(status_ids)
            desired_ids = filter(lambda x: x <= actual_status_index, [1, len_status-2, len_status-1]) # Segundo, penúltimo e último
            result_list = self.__find_on_changelog(issue, [status_ids[i] for i in desired_ids])
            return result_list
        except Exception as e:
            # Caso não esteja em um board
            return [(None,None),(None,None),(None,None)]

    def project(self, jira_project,
    ontology_scrum_atomic_project = None,
    ontology_scrum_process = None,
    ontology_product_backlog_definition = None,
    ontology_product_backlog = None):
    
        # Scrum atomic project
        if ontology_scrum_atomic_project is None:
            ontology_scrum_atomic_project = factories_model.ScrumAtomicProjectFactory()
        ontology_scrum_atomic_project.organization = self.organization
        ontology_scrum_atomic_project.name = jira_project.name
        ontology_scrum_atomic_project.index = jira_project.key
        
        # Scrum process
        if ontology_scrum_process is None:
            ontology_scrum_process = factories_model.ScrumProcessFactory()
        ontology_scrum_process.organization = self.organization
        ontology_scrum_process.name = jira_project.name
        ontology_scrum_process.scrum_project = ontology_scrum_atomic_project

        # Product backlog definition
        if ontology_product_backlog_definition is None:
            ontology_product_backlog_definition = factories_model.ProductBacklogDefinitionFactory()
        ontology_product_backlog_definition.name = jira_project.name
        ontology_product_backlog_definition.scrum_process = ontology_scrum_process
        
        #Product backlog
        if ontology_product_backlog is None:
           ontology_product_backlog = factories_model.ProductBacklogFactory()
        ontology_product_backlog.name = jira_project.name
        # ontology_product_backlog.product_backlog_definition = ontology_product_backlog_definition.id
        
        return ontology_scrum_atomic_project, ontology_scrum_process, ontology_product_backlog_definition, ontology_product_backlog

    def team_member(self, etl_user, etl_scrum_development_team,
    jira_user, jira_project,
    ontology_team_member = None):

        person_application = factories.PersonFactory()
        scrum_development_team_application = factories.DevelopmentTeamFactory()

        if ontology_team_member is None:
            ontology_team_member = factories_model.DeveloperFactory()
        ontology_team_member.team_role = 'developer'
        try:
            user_id = jira_user.accountId
            ontology_team_member.person = person_application.retrive_by_external_uuid(user_id)
            if ontology_team_member.person is None:
                raise Exception('Not found')
        except Exception as e:
            user = etl_user()
            user.config(self.data)
            data_to_create = {'content': {'all': {'user': {'accountId': user_id}}}}
            ontology_team_member.person = user.create(data_to_create)
        try:
            team_id = jira_project.id
            ontology_team_member.team = scrum_development_team_application.retrive_by_external_uuid(team_id)
            if ontology_team_member.team is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_development_team = etl_scrum_development_team()
            scrum_development_team.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': team_id}}}}
            ontology_team_member.team = scrum_development_team.create(data_to_create)

        return ontology_team_member

    def epic(self, etl_scrum_project, etl_team_member,
    jira_issue, jira_project,
    ontology_epic = None):

        team_member_application = factories.TeamMemberFactory()
        product_backlog_application = factories.ProductBacklogFactory()

        if ontology_epic is None:
            ontology_epic = factories_model.EpicFactory()
        ontology_epic.name = jira_issue.raw['fields']['summary']

        (activated_date, activated_id), (resolved_date, resolved_id), (closed_date, closed_id) = self.find_activated_resolved_closed(jira_issue)

        # Product Backlog
        try:
            project_id = jira_project.id
            ontology_epic.product_backlog = product_backlog_application.retrive_by_external_uuid(jira_project.id).id
            if ontology_epic.product_backlog is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            _, _, _, product_backlog = scrum_project.create(data_to_create)
            ontology_epic.product_backlog = product_backlog.id

        # Creator
        try:
            creator_id = jira_issue.raw['fields']['creator']['accountId']
            ontology_epic.created_by = team_member_application.retrive_by_external_id_and_project_name(creator_id, jira_project.name).id
            if ontology_epic.created_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.created_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': creator_id}
            ontology_epic.created_by = team_member.create(data_to_create, None, jira_project).id

        # Assignee
        try:
            assignee_id = jira_issue.raw['fields']['assignee']['accountId']
            ontology_epic.assigned_by = [team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project.name)]
            if ontology_epic.assigned_by == [None]:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.assigned_by = []
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': assignee_id}
            ontology_epic.assigned_by = [team_member.create(data_to_create, None, jira_project)]

        # Activated
        try:
            if activated_id is None:
                raise TypeError("Not activated")
            team_member_ = team_member_application.retrive_by_external_id_and_project_name(activated_id, jira_project.name)
            ontology_epic.activated_by = team_member_.id
            ontology_epic.activated_date = activated_date
            if ontology_epic.activated_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.activated_by = None
            ontology_epic.activated_date = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': activated_id}
            team_member_ = team_member.create(data_to_create, None, jira_project)
            ontology_epic.activated_by = team_member_.id
            ontology_epic.activated_date = activated_date

        # Resolved
        try:
            if resolved_id is None:
                raise TypeError("Not resolved")
            team_member_ = team_member_application.retrive_by_external_id_and_project_name(resolved_id, jira_project.name)
            ontology_epic.resolved_by = team_member_.id
            ontology_epic.resolved_date = resolved_date
            if ontology_epic.resolved_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.resolved_by = None
            ontology_epic.resolved_date = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': resolved_id}
            team_member_ = team_member.create(data_to_create, None, jira_project)
            ontology_epic.resolved_by = team_member_.id
            ontology_epic.resolved_date = resolved_date

        # Closed 
        try:
            if closed_id is None:
                raise TypeError("Not closed")
            team_member_ = team_member_application.retrive_by_external_id_and_project_name(closed_id, jira_project.name)
            ontology_epic.closed_by = team_member_.id
            ontology_epic.closed_date = closed_date
            if ontology_epic.closed_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_epic.closed_by = None
            ontology_epic.closed_date = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': closed_id}
            team_member_ = team_member.create(data_to_create, None, jira_project)
            ontology_epic.closed_by = team_member_.id
            ontology_epic.closed_date = closed_date
        
        try:
            ontology_epic.story_points = jira_issue.raw['fields']['customfield_10020']
        except Exception as e:
            ontology_epic.story_points = None
        try:
            ontology_epic.created_date = self.date_formater(jira_issue.raw['fields']['created'])
        except Exception as e:
            ontology_epic.created_date = None

        return ontology_epic

    def sprint(self, etl_scrum_project,
    jira_sprint, jira_project,
    ontology_sprint = None, ontology_sprint_backlog = None):
        
        scrum_process_application = factories.ScrumProcessFactory()

        # Sprint
        if ontology_sprint is None:
            ontology_sprint = factories_model.SprintFactory()
        ontology_sprint.organization = self.organization
        ontology_sprint.name = jira_sprint.name
        try:
            ontology_sprint.description = jira_sprint.goal
        except Exception as e:
            ontology_sprint.description = ''
        try:
            ontology_sprint.start_date = self.date_formater(jira_sprint.startDate)
        except Exception as e:
            ontology_sprint.start_date = None
        try:
            ontology_sprint.end_date = self.date_formater(jira_sprint.endDate)
        except Exception as e:
            ontology_sprint.end_date = None
        try:
            ontology_sprint.complete_date = self.date_formater(jira_sprint.completeDate)
        except Exception as e:
            ontology_sprint.complete_date = None
        try:
            project_id = jira_project.id
            ontology_sprint.scrum_process_id = scrum_process_application.retrive_by_external_uuid(project_id).id
            if ontology_sprint.scrum_process_id is None:
                raise Exception('Not found')
        except NameError:
            ontology_sprint.scrum_process_id = None
        except Exception as e:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            _, scrum_process, _, _ = scrum_project.create(data_to_create)
            ontology_sprint.scrum_process_id = scrum_process.id

        # Sprint Backlog
        if ontology_sprint_backlog is None:
            ontology_sprint_backlog = factories_model.SprintBacklogFactory()
        ontology_sprint_backlog.name = ontology_sprint.name
        # ontology_sprint_backlog.sprint = ontology_sprint.id

        return ontology_sprint, ontology_sprint_backlog

    def user_story(self, etl_scrum_project, etl_team_member, etl_sprint,
    jira_issue, jira_project,
    ontology_atomic_user_story = None):

        product_backlog_application = factories.ProductBacklogFactory()
        team_member_application = factories.TeamMemberFactory()
        sprint_backlog_application = factories.SprintBacklogFactory()

        if ontology_atomic_user_story is None:
            ontology_atomic_user_story = factories_model.AtomicUserStoryFactory()
        ontology_atomic_user_story.name = jira_issue.raw['fields']['summary']
        ontology_atomic_user_story.description = jira_issue.raw['fields'].get('description')

        (activated_date, activated_id), (resolved_date, resolved_id), (closed_date, closed_id) = self.find_activated_resolved_closed(jira_issue)

        # Product Backlog
        try:
            project_id = jira_project.id
            ontology_atomic_user_story.product_backlog = product_backlog_application.retrive_by_external_uuid(jira_project.id).id
            if ontology_atomic_user_story.product_backlog is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            _, _, _, product_backlog = scrum_project.create(data_to_create)
            ontology_atomic_user_story.product_backlog = product_backlog.id

        # Creator
        try:
            creator_id = jira_issue.raw['fields']['creator']['accountId']
            ontology_atomic_user_story.created_by = team_member_application.retrive_by_external_id_and_project_name(creator_id, jira_project.name).id
            if ontology_atomic_user_story.created_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.created_by = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': creator_id}
            ontology_atomic_user_story.created_by = team_member.create(data_to_create, None, jira_project).id

        # Assignee
        try:
            assignee_id = jira_issue.raw['fields']['assignee']['accountId']
            ontology_atomic_user_story.assigned_by = [team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project.name)]
            if ontology_atomic_user_story.assigned_by == [None]:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.assigned_by = []
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': assignee_id}
            ontology_atomic_user_story.assigned_by = [team_member.create(data_to_create, None, jira_project)]

        # Activated
        try:
            if activated_id is None:
                raise TypeError("Not activated")
            team_member_ = team_member_application.retrive_by_external_id_and_project_name(activated_id, jira_project.name)
            ontology_atomic_user_story.activated_by = team_member_.id
            ontology_atomic_user_story.activated_date = activated_date
            if ontology_atomic_user_story.activated_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.activated_by = None
            ontology_atomic_user_story.activated_date = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': activated_id}
            team_member_ = team_member.create(data_to_create, None, jira_project)
            ontology_atomic_user_story.activated_by = team_member_.id
            ontology_atomic_user_story.activated_date = activated_date

        # Resolved
        try:
            if resolved_id is None:
                raise TypeError("Not resolved")
            team_member_ = team_member_application.retrive_by_external_id_and_project_name(resolved_id, jira_project.name)
            ontology_atomic_user_story.resolved_by = team_member_.id
            ontology_atomic_user_story.resolved_date = resolved_date
            if ontology_atomic_user_story.resolved_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.resolved_by = None
            ontology_atomic_user_story.resolved_date = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': resolved_id}
            team_member_ = team_member.create(data_to_create, None, jira_project)
            ontology_atomic_user_story.resolved_by = team_member_.id
            ontology_atomic_user_story.resolved_date = resolved_date

        # Closed 
        try:
            if closed_id is None:
                raise TypeError("Not closed")
            team_member_ = team_member_application.retrive_by_external_id_and_project_name(closed_id, jira_project.name)
            ontology_atomic_user_story.closed_by = team_member_.id
            ontology_atomic_user_story.closed_date = closed_date
            if ontology_atomic_user_story.closed_by is None:
                raise Exception('Not found')
        except (NameError, TypeError):
            ontology_atomic_user_story.closed_by = None
            ontology_atomic_user_story.closed_date = None
        except Exception as e:
            team_member = etl_team_member()
            team_member.config(self.data)
            data_to_create = {'accountId': closed_id}
            team_member_ = team_member.create(data_to_create, None, jira_project)
            ontology_atomic_user_story.closed_by = team_member_.id
            ontology_atomic_user_story.closed_date = closed_date
        
        try:
            ontology_atomic_user_story.story_points = jira_issue.raw['fields']['customfield_10020']
        except Exception as e:
            ontology_atomic_user_story.story_points = None
        try:
            ontology_atomic_user_story.created_date = self.date_formater(jira_issue.raw['fields']['created'])
        except Exception as e:
            ontology_atomic_user_story.created_date = None

        # Sprint backlogs
        try:
            sprints = jira_issue.raw['fields']['customfield_10018']
            if not sprints: # Check if is None or []
                ontology_atomic_user_story.sprint_backlogs = []
            else:
                backlogs_list = []
                for sprint in sprints:
                    sprint_id = sprint['id']
                    board_id = sprint['boardId']
                    ontology_sprint_backlog = sprint_backlog_application.retrive_by_external_uuid(sprint_id)
                    if ontology_sprint_backlog is None:
                        sprint_backlog = etl_sprint()
                        sprint_backlog.config(self.data)
                        data_to_create = {'content': {'all': {'sprint': {'id': sprint_id, 'originBoardId': board_id}}}}
                        _, ontology_sprint_backlog = sprint_backlog.create(data_to_create)
                    backlogs_list.append(ontology_sprint_backlog)
                ontology_atomic_user_story.sprint_backlogs = backlogs_list
        except Exception as e:
            ontology_atomic_user_story.sprint_backlogs = []

        try:
            ontology_atomic_user_story.created_by_sro = jira_issue.is_a_task
        except Exception as e:
            ontology_atomic_user_story.created_by_sro = False

        return ontology_atomic_user_story

    def user(self, jira_user,
    ontology_user = None):

        if ontology_user is None:
            ontology_user = factories_model.PersonFactory()
        ontology_user.organization = self.organization
        ontology_user.name = jira_user.displayName
        if jira_user.emailAddress != '':
            ontology_user.email = jira_user.emailAddress

        return ontology_user

    def task(self, etl_team_member, etl_user_story, etl_sprint,
    jira_issue, jira_project,
    ontology_scrum_intended_development_task = None, ontology_scrum_performed_development_task = None):

        # Ontology scrum intended development task
        team_member_application = factories.TeamMemberFactory()
        priority_application = factories.PriorityFactory()
        atomic_user_story_application = factories.AtomicUserStoryFactory()
        sprint_application = factories.SprintFactory()
        sprint_backlog_application = factories.SprintBacklogFactory()
        development_task_type_application = factories.DevelopmentTaskTypeFactory()
        priority_dict = {'1': 'high', '2': 'high', '3': 'medium', '4': 'normal', '5': 'normal'}

        (activated_date, activated_id), (resolved_date, resolved_id), (closed_date, closed_id) = self.find_activated_resolved_closed(jira_issue)

        def _scrum_development_task(scrum_dev_task):
            scrum_dev_task.name = jira_issue.raw['fields']['summary']
            scrum_dev_task.description = jira_issue.raw['fields'].get('description')

            # Created date
            scrum_dev_task.created_date = self.date_formater(jira_issue.raw['fields']['created'])

            # Created by
            try:
                creator_id = jira_issue.raw['fields']['creator']['accountId']
                scrum_dev_task.created_by = team_member_application.retrive_by_external_id_and_project_name(creator_id, jira_project.name).id
                if scrum_dev_task.created_by is None:
                    raise Exception('Not found')
            except (NameError, TypeError):
                scrum_dev_task.created_by = None
            except Exception as e:    
                team_member = etl_team_member()
                team_member.config(self.data)
                data_to_create = {'accountId': creator_id}
                scrum_dev_task.created_by = team_member.create(data_to_create, None, jira_project).id
            
            # Assigned by
            try:
                assignee_id = jira_issue.raw['fields']['assignee']['accountId']
                scrum_dev_task.assigned_by = [team_member_application.retrive_by_external_id_and_project_name(assignee_id, jira_project.name)]
                if scrum_dev_task.assigned_by == [None]:
                    raise Exception('Not found')
            except (NameError, TypeError):
                scrum_dev_task.assigned_by = []
            except Exception as e:
                team_member = etl_team_member()
                team_member.config(self.data)
                data_to_create = {'accountId': assignee_id}
                scrum_dev_task.assigned_by = [team_member.create(data_to_create, None, jira_project)]

            # Story Points
            try:
                scrum_dev_task.story_points = jira_issue.raw['fields']['customfield_10020']
            except Exception as e:
                scrum_dev_task.story_points = None

            # Sprints & Sprint Backlogs
            sprints_list = []
            backlogs_list = []
            try:
                sprints = jira_issue.raw['fields']['customfield_10018']
                sprints.sort(key=lambda x: self.date_formater(x['startDate']))
                if not sprints: # Check if is None or []
                    scrum_dev_task.sprints = []
                    scrum_dev_task.sprint_backlogs = []
                else:
                    for sprint in sprints:
                        sprint_id = sprint['id']
                        board_id = sprint['boardId']
                        ontology_sprint = sprint_application.retrive_by_external_uuid(sprint_id)
                        ontology_sprint_backlog = sprint_backlog_application.retrive_by_external_uuid(sprint_id)
                        if ontology_sprint is None: # Se não existe sprint, tbm não existe sprint_backlog
                            sprint_backlog = etl_sprint()
                            sprint_backlog.config(self.data)
                            data_to_create = {'content': {'all': {'sprint': {'id': sprint_id, 'originBoardId': board_id}}}}
                            ontology_sprint, ontology_sprint_backlog = sprint_backlog.create(data_to_create)
                        if(closed_date is not None):
                            try:
                                if(ontology_sprint.start_date <= closed_date <= ontology_sprint.complete_date):
                                    sprints_list.append(ontology_sprint)
                                    backlogs_list.append(ontology_sprint_backlog)
                                    break
                            except Exception as e:
                                pass
                        sprints_list.append(ontology_sprint)
                        backlogs_list.append(ontology_sprint_backlog)
                    scrum_dev_task.sprints = sprints_list
                    scrum_dev_task.sprint_backlogs = backlogs_list
            except Exception as e:
                scrum_dev_task.sprints = []
                scrum_dev_task.sprint_backlogs = []

            # Atomic User Story
            try:
                parent_id = jira_issue.raw['fields']['parent']['id']
                scrum_dev_task.atomic_user_story = atomic_user_story_application.retrive_by_external_uuid(parent_id).id
                if scrum_dev_task.atomic_user_story is None:
                    raise Exception('Not found')
            except (NameError, TypeError):
                scrum_dev_task.atomic_user_story = None
            except Exception as e:
                atomic_user_story = etl_user_story()
                atomic_user_story.config(self.data)
                data_to_create = {"content": {"all": {"issue": {"id": parent_id } } } }
                scrum_dev_task.atomic_user_story = atomic_user_story.create(data_to_create, None, jira_project).id
        
        if ontology_scrum_intended_development_task is None:
            ontology_scrum_intended_development_task = factories_model.ScrumIntentedDevelopmentTaskFactory()
        
        _scrum_development_task(ontology_scrum_intended_development_task)
        
        # Type Activity
        try:
            task_type = jira_issue.raw['fields']['labels'][0].lower()
            ontology_development_task_type = development_task_type_application.retrive_by_name(task_type)
            if ontology_development_task_type is None:
                ontology_development_task_type = factories_model.DevelopmentTaskTypeFactory()
                ontology_development_task_type.name = task_type
                ontology_development_task_type.description = task_type
                development_task_type_application.create(ontology_development_task_type)
        except Exception as e:
            ontology_development_task_type = development_task_type_application.retrive_by_name("não definido")
        ontology_scrum_intended_development_task.type_activity = ontology_development_task_type.id

        # Priority
        try:
            ontology_scrum_intended_development_task.priority = priority_application.retrive_by_name(priority_dict[jira_issue.raw['fields']['priority']['id']]).id
        except Exception as e:
            ontology_scrum_intended_development_task.priority = None
            
        # Risk
        ontology_scrum_intended_development_task.risk = None

        # Time estimate
        ontology_scrum_intended_development_task.time_estimate = jira_issue.raw['fields']['timeoriginalestimate']

        # --------------------------

        # Performed
        if (jira_issue.raw['fields']['status']['statusCategory']['id'] == 3 # Itens concluídos
        or jira_issue.raw['fields']['status']['statusCategory']['id'] == 4): # Em andamento
            
            # Ontology scrum performed development task
            if ontology_scrum_performed_development_task is None:
                ontology_scrum_performed_development_task = factories_model.ScrumPerformedDevelopmentTaskFactory()
            
            _scrum_development_task(ontology_scrum_performed_development_task)

            # Closed Date & Closed By
            try:
                if closed_id is None:
                    raise TypeError("Not closed")
                team_member_ = team_member_application.retrive_by_external_id_and_project_name(closed_id, jira_project.name)
                ontology_scrum_performed_development_task.closed_by = team_member_.id
                ontology_scrum_performed_development_task.closed_date = closed_date
                if ontology_scrum_performed_development_task.closed_by is None:
                    raise Exception('Not found')
            except (NameError, TypeError):
                ontology_scrum_performed_development_task.closed_by = None
                ontology_scrum_performed_development_task.closed_date = None
            except Exception as e:
                team_member = etl_team_member()
                team_member.config(self.data)
                data_to_create = {'accountId': closed_id}
                team_member_ = team_member.create(data_to_create, None, jira_project)
                ontology_scrum_performed_development_task.closed_by = team_member_.id
                ontology_scrum_performed_development_task.closed_date = closed_date

            # Activated Date & Activated By
            try:
                if activated_id is None:
                    raise TypeError("Not activated")
                team_member_ = team_member_application.retrive_by_external_id_and_project_name(activated_id, jira_project.name)
                ontology_scrum_performed_development_task.activated_by = team_member_.id
                ontology_scrum_performed_development_task.activated_date = activated_date
                if ontology_scrum_performed_development_task.activated_by is None:
                    raise Exception('Not found')
            except (NameError, TypeError):
                ontology_scrum_performed_development_task.activated_by = None
                ontology_scrum_performed_development_task.activated_date = None
            except Exception as e:
                team_member = etl_team_member()
                team_member.config(self.data)
                data_to_create = {'accountId': activated_id}
                team_member_ = team_member.create(data_to_create, None, jira_project)
                ontology_scrum_performed_development_task.activated_by = team_member_.id
                ontology_scrum_performed_development_task.activated_date = activated_date

            # Resolved Date & Resolved By
            try:
                if resolved_id is None:
                    raise TypeError("Not resolved")
                team_member_ = team_member_application.retrive_by_external_id_and_project_name(resolved_id, jira_project.name)
                ontology_scrum_performed_development_task.resolved_by = team_member_.id
                ontology_scrum_performed_development_task.resolved_date = resolved_date
                if ontology_scrum_performed_development_task.resolved_by is None:
                    raise Exception('Not found')
            except (NameError, TypeError):
                ontology_scrum_performed_development_task.resolved_by = None
                ontology_scrum_performed_development_task.resolved_date = None
            except Exception as e:
                team_member = etl_team_member()
                team_member.config(self.data)
                data_to_create = {'accountId': resolved_id}
                team_member_ = team_member.create(data_to_create, None, jira_project)
                ontology_scrum_performed_development_task.resolved_by = team_member_.id
                ontology_scrum_performed_development_task.resolved_date = resolved_date

            # Caused By (É feito fora do conversor, porque depende do intended)
            # ontology_scrum_performed_development_task.caused_by = ontology_scrum_intended_development_task.id

            # Time Spent
            ontology_scrum_performed_development_task.time_spent = jira_issue.raw['fields']['timespent']

            return ontology_scrum_intended_development_task, ontology_scrum_performed_development_task

        return ontology_scrum_intended_development_task, None

    def development_team(self, etl_scrum_project_team,
    jira_project,
    ontology_scrum_development_team = None):

        scrum_team_application = factories.ScrumTeamFactory()

        if ontology_scrum_development_team is None:
            ontology_scrum_development_team = factories_model.DevelopmentTeamFactory()
        ontology_scrum_development_team.organization = self.organization
        ontology_scrum_development_team.name = f"{jira_project.key}_scrum_development_team"
        try:
            project_id = jira_project.id
            ontology_scrum_development_team.scrum_team_id = scrum_team_application.retrive_by_external_uuid(jira_project.id).id
            if ontology_scrum_development_team.scrum_team_id is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_project_team = etl_scrum_project_team()
            scrum_project_team.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            ontology_scrum_development_team.scrum_team_id = scrum_project_team.create(data_to_create).id

        return ontology_scrum_development_team

    def team(self, etl_scrum_project,
    jira_project,
    ontology_scrum_team = None):

        scrum_project_application = factories.ScrumAtomicProjectFactory()

        if ontology_scrum_team is None:
            ontology_scrum_team = factories_model.ScrumTeamFactory()
        ontology_scrum_team.name = f"{jira_project.key}_scrum_team"
        ontology_scrum_team.organization = self.organization
        try:
            project_id = jira_project.id
            ontology_scrum_team.scrum_project = scrum_project_application.retrive_by_external_uuid(jira_project.id).id
            if ontology_scrum_team.scrum_project is None:
                raise Exception('Not found')
        except Exception as e:
            scrum_project = etl_scrum_project()
            scrum_project.config(self.data)
            data_to_create = {'content': {'all': {'project': {'id': project_id}}}}
            scrum_project, _, _, _ = scrum_project.create(data_to_create)
            ontology_scrum_team.scrum_project = scrum_project.id

        return ontology_scrum_team

