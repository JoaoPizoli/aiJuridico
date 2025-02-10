import sys
import os
import re
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_root)
from crewai_tools import FileReadTool
from src.jurisCrew.extractorCrew import ExtractCrew
from src.jurisCrew.searchCrew import SearchCrew
from src.jurisCrew.writingCrew import WritingCrew

input = {"topic"       : "consumidor", 
         "description" : "planos de saúde com reajustes anuais e faixa etária",  
         "num_keys"    : 5}

agents_config = 'config/agents.yaml'
tasks_config = 'config/tasks.yaml'

Ecrew = ExtractCrew()
Screw = SearchCrew()
Wcrew = WritingCrew()

Eout  = Ecrew.crew().kickoff(inputs=input)
Ecrew.parser(content=Eout)

input_conf = {"task_moduler": "selecionar no máximo as 5 melhores jurisprudências"}
Sout   = Screw.crew().kickoff(inputs=input_conf)
Wout   = Wcrew.before_kickoff_function(inputs=Sout.raw)
Wout   = Wcrew.crew().kickoff()



### implement anothe file writer