#from typing import List
#from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase#, agent, crew, task

#from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

from src.jurisCrew.extractorCrew import ExtractCrew
from src.jurisCrew.searchCrew import SearchCrew
from src.jurisCrew.monitoringCrew import MonitorCrew
from src.jurisCrew.writingCrew import WritingCrew
from src.jurisCrew.reviewCrew import ReviewCrew
from src.jurisCrew.summaryCrew import SummarizeCrew
from src.jurisCrew.updatingCrew import UpdateCrew

import sys
import os
import re
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)
import asyncio
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL"] = os.getenv("OPENAI_MODEL_NAME")

#@CrewBase
class JusaiCrew:
    #(SearchCrew, MonitorCrew, WritingCrew, ReviewCrew, SummarizeCrew):

    #agents_config = 'config/agents.yaml'
    #tasks_config = 'config/tasks.yaml'

    def __init__(self, input, e=True, s=True, m=False, w=True, r=False, z=False, u=False):

        self.flux  = [e,s,w,r,m,z,u] #search, write, revire, monitor, summarize, update
        self.input = input

        self.e, self.s, self.m, self.w, self.r, self.z, self.u = e, s, m, w, r, z, u

        if e: self.Ecrew = ExtractCrew()
        if s: self.Screw = SearchCrew()
        if w: self.Wcrew = WritingCrew()

        #if m: self.Mcrew = MonitorCrew()
        #if r: self.Rcrew = ReviewCrew()
        #if z: self.Zcrew = SummarizeCrew()
        #if u: self.Ucrew = UpdateCrew()

        #run when init it 
        asyncio.run(self.async_multiple_crews())
        #self.async_multiple_crews()

    #async def
    async def async_multiple_crews(self):
        #orchestrar chamadas
        #Wout  = self.Wcrew.kickoff_async(inputs=Sout)
        #Sout_ = await asyncio.gather(Sout)
        #Mout  = self.Mcrew.kickoff_async(inputs=Sout_[1])
        #Wout  = self.Wcrew.kickoff_async(inputs=Sout_[1])
        #Rout  = self.Rcrew.kickoff_async(inputs=Wout)
        #Zout  = self.Zcrew.kickoff_async(inputs=Sout_[1])
        #Uout  = self.Ucrew.kickoff_async(inputs=[Mout, Wout, Zout])

        Eout   = self.Ecrew.crew().kickoff(inputs=self.input)
        self.Ecrew.parser(content=Eout)
        input_conf = {"task_moduler": "Selecionar no máximo as 3 melhores jurisprudências do conjunto obtido"}
        self.Sout   = self.Screw.crew().kickoff(inputs=input_conf)
        self.Wcrew.before_kickoff_function(inputs=self.Sout.raw)
        
        Wout = self.Wcrew.crew().kickoff()
        return Wout.raw    
        
        #Wout   = self.Wcrew.before_kickoff_function(inputs=self.Sout.raw)
        #Wout   = self.Wcrew.crew().kickoff()

        #output = Wout.raw
        #print(output)
        #return output