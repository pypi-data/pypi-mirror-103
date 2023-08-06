import logging
logging.basicConfig(level=logging.INFO)

from jiraX import factories as factory
from pprint import pprint
from .base_entity import BaseEntity
from tqdm import tqdm

from sro_db.application import factories
from sro_db.model import factories as factories_model

from .user_story import user_story as etl_user_story
from .scrum_development_task import scrum_development_task as etl_scrum_development_task

""" Task """
class task_extra(BaseEntity):
	"""
	Class responsible for retrieve tasks from jira
	"""
	def create(self, data, jira_issue = None, jira_project = None):
		try:
			logging.info("Creating Task")

			if jira_issue is None:
				issue_id = data['content']['all']['issue']['id']
				issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)
				jira_issue = issue_apl.find_by_id(issue_id)
			
			if jira_project is None:
				project_id = data['content']['all']['issue']['fields']['project']['id']
				project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
				jira_project = project_apl.find_by_id(project_id)
			
			jira_issue.is_a_task = True
			jira_issue.raw['fields']['parent'] = {'id': jira_issue.id}

			user_story = etl_user_story()
			development_task = etl_scrum_development_task()
			user_story.config(self.data)
			development_task.config(self.data)
			atomic_user_story = user_story.create(None, jira_issue, jira_project)
			scrum_intended_development_task, scrum_performed_development_task = development_task.create(None, jira_issue, jira_project)

			logging.info("Task created")

			return atomic_user_story, scrum_intended_development_task, scrum_performed_development_task

		except Exception as e:
			pprint(e)
			logging.error("Failed to create Task")

	def update(self, data):
		try:
			logging.info("Updating Task")

			user_story = etl_user_story()
			development_task = etl_scrum_development_task()
			user_story.config(self.data)
			development_task.config(self.data)
			atomic_user_story = user_story.update(data, True)
			scrum_intended_development_task, scrum_performed_development_task = development_task.update(data, True)
			
			logging.info("Task updated")

			return atomic_user_story, scrum_intended_development_task, scrum_performed_development_task

		except Exception as e:
			pprint(e)
			logging.error("Failed to update Task")

	def delete(self, data):
		pass

	def do(self,data):
		"""Retrieve tasks from all projects

		Args:
			data (dict): With user, key and server to connect with jira
		"""
		try:
			logging.info("Task")
			self.config(data)

			project_apl = factory.ProjectFactory(user=self.user,apikey=self.key,server=self.url)
			issue_apl = factory.IssueFactory(user=self.user,apikey=self.key,server=self.url)

			atomic_user_story_application = factories.AtomicUserStoryFactory()
			# intended_task_application = factories.ScrumIntentedDevelopmentTaskFactory()

			projects = project_apl.find_all()
			for project in tqdm(projects, desc='Tasks'):
				stories = issue_apl.find_task_by_project(project.key)
				for story in stories:
					# if intended_task_application.retrive_by_external_uuid(story.id):
					if atomic_user_story_application.retrive_by_external_uuid(story.id): 
						continue
					self.create(None, story, project)

			logging.info("Successfully done Task")

		except Exception as e:
			pprint(e)
			logging.error("Failed to do Task")

	def update_by_time(self, data, time):
		pass
