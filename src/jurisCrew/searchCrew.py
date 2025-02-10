from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

import os
from dotenv import load_dotenv

from crewai_tools import SeleniumScrapingTool, WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool, SpiderTool
#from crewai_tools import FileReadTool
from src.jurisCrew.tools.scrape_tool import ScrapeTribunalTool

import sys
import os
import re
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL_NAME")
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

@CrewBase
class SearchCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def read_inputs(self, filename ='\scrape.dict') -> List[str]:
        filename = str(project_root)+"\src\jurisCrew\config" + filename
        with open(filename, 'r') as f:
            data = f.readlines()
        #clean_phrases = [re.sub(r'^\d+\.\s+', '', s).strip() for s in data if s.strip()]
        return data

    # AGENTS   
    @agent
    def searcher(self) -> Agent:
        #s2_tool = ScrapeWebsiteTool()

        urls     = self.read_inputs(filename ='\scrape.dict')
        keywords = self.read_inputs(filename ='\searchkeys.dict')
        tool     = ScrapeTribunalTool()



        agent =  Agent(
            config           = self.agents_config['auxiliarJurSearch'],
            allow_delegation = False,
            #tools            = tool_list,
            tools            = [tool],
            verbose          = True)
        
        agent.backstory += "urls: " + str(urls)
        agent.backstory += "keywords: " + str(keywords)

        return agent

    # TASKS
    @task
    def search(self) -> Task:

        return Task(
            config  = self.tasks_config['search_jurisp'],
            agent   = self.searcher(),
            verbose = True)

    @crew
    def crew(self) -> Crew:
        crew = Crew(
            agents  = self.agents,  
            tasks   = self.tasks,  
            process = Process.sequential,
            planning=True,
            verbose = True
        )
    
        return crew
    
