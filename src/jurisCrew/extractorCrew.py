from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

import os
from dotenv import load_dotenv
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)

#from crewai_tools import SeleniumScrapingTool, WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool, SpiderTool
from crewai_tools import FileWriterTool
from src.jurisCrew.tools.scrape_tool import ScrapeTribunalTool

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL_NAME")
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")

@CrewBase
class ExtractCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def parser(self, content, filename="\src\jurisCrew\config\searchkeys.dict"):
        #file_writer_tool = FileWriterTool()
        #file_writer_tool._run(content=content)
        #print("complete")
        #print("")
        filename = str(project_root)+filename
        f = open(filename, "w")
        f.write(content.raw)
        f.close()
        return None

    # AGENTS
    @agent
    def extractor(self) -> Agent:
        return Agent(
            config=self.agents_config['auxiliarJurReader'],
            allow_delegation=False,
            verbose=True)
    
    # TASKS
    @task
    def extract(self) -> Task:
        return Task(
            config=self.tasks_config['extract_keys'],
            agent=self.extractor(),
            verbose=True)

    @crew
    def crew(self) -> Crew:
        crew = Crew(
            agents=self.agents,  
            tasks=self.tasks,  
            process=Process.sequential,
            planning=True,
            verbose=True
        )
    
        return crew
    

#crew = Crew(tasks=[report_task])
#output = crew.execute()
#file_writer.write(output)