from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# Check our tools documentations for more information on how to use them
from crewai_tools import FileReadTool, DirectoryReadTool

@CrewBase
class CrewaiReadmeCreator():
	"""Crewai Readme Creator crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	folder = None

	def set_folder(self, folder):
		self.folder = folder

	@agent
	def senior_data_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_data_researcher'],
			verbose=True,
		)

	@agent
	def senior_dataresearcher(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_data_researcher'],
			verbose=True,
		)

	@agent
	def readme_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['readme_writer'],
			verbose=True,
		)

	@agent
	def readme_planner(self) -> Agent: 
		return Agent(
			config=self.agents_config['readme_planner'],
			verbose=True,
		)

	@agent
	def readme_reviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['readme_reviewer'],
			verbose=True,
		)

	# Tasks
	
	@task
	def folder_analizer_task(self) -> Task:
		return Task(
			config=self.tasks_config['folder_analizer_task'],
			agent=self.senior_data_researcher(),
			tools=[DirectoryReadTool(self.folder), FileReadTool()],
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.senior_data_researcher(),
			tools=[FileReadTool()],
		)

	@task
	def readme_planning_task(self) -> Task:  # Ensure this task is linked to the new agent
		return Task(
			config=self.tasks_config['readme_planning_task'],
			agent=self.readme_planner(), 
			# context=[self.research_task.output_json],  # Uncomment if needed
		)
	
	@task
	def readme_writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['readme_writing_task'],
			agent=self.readme_writer(),
			output_file='generated_readme.md'
		)
	
	@task
	def readme_review_task(self) -> Task:
		return Task(
			config=self.tasks_config['readme_review_task'],
			agent=self.readme_reviewer(),
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ProjectAnalyzer crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/,
			verbose=True,
			memory=True,
			# planning=True,
		)