from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL_NAME")

@CrewBase
class ReviewCrew:

    # This crew Review works

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # AGENTS
    @agent
    def cliente(self) -> Agent:
        return Agent(
            config=self.agents_config['cliente_1'],
            allow_delegation=False,
            verbose=False,
            #llm=llm
        )

    # TASKS
    @task
    def peticao_inicial(self) -> Task:
        return Task(
            config=self.tasks_config['peticao_inicial'],
            agent=self.advogado(),
            #llm=llm
        )