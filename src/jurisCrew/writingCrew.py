from typing import List
from crewai import Agent, Crew, Process, Task
import crewai.project
import crewai
print("")
#print(dir(crewai))
#print(dir(crewai.project))
print(crewai.__version__)
print("")
from crewai.project import CrewBase, agent, crew, task, before_kickoff

#from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

import os
from dotenv import load_dotenv
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL_NAME")

@CrewBase
class WritingCrew:
    # this crew writes down information based on a given knowledge


    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff
    def before_kickoff_function(self, inputs):
        self.input = inputs
        return None

    # AGENTS
    @agent
    def writer(self) -> Agent:
        agent = Agent(
                config=self.agents_config['auxiliarJurWrite'],
                allow_delegation=False,
                verbose=True
                )
        agent.backstory += "Informações úteis: " + str(self.input)
        return agent

    # TASKS
    @task
    def write(self) -> Task:
        return Task(
                config=self.tasks_config['write_defense'],
                agent=self.writer(),
                verbose=True
                )

    @crew
    def crew(self) -> Crew:
        return Crew(
                agents=self.agents,  
                tasks=self.tasks,  
                process=Process.sequential,
                planning=True,
                verbose=True
                )